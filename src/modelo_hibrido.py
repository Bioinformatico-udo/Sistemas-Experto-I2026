# src/modelo_hibrido.py
"""
Modelo Híbrido para Identificación de Corales - VERSIÓN FINAL
Arquitectura: Predice CARACTERÍSTICAS TAXONÓMICAS, no la especie directamente.
Las características predichas se pasan al motor de inferencia para obtener la especie final.
Integrado con Motor de Ponderación Inteligente (motor_ponderacion.py).
"""

import sys
from pathlib import Path

# Configurar el paquete y el sys.path si se ejecuta directamente
if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    __package__ = "src"

import json
import numpy as np
import pandas as pd
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from .motor_ponderacion import PonderadorCaracteristicas

# ─── CONFIGURACIÓN ───
RUTA_DATASET = "data/dataset_entrenamiento.csv"
RUTA_MODELO = "models/modelo_corales.keras"
RUTA_TOKENIZER = "models/tokenizer.pickle"
RUTA_ENCODERS = "models/label_encoders.pickle"
RUTA_ESPECIES = "data/especies.json"
MAX_VOCAB_SIZE = 500
MAX_SEQUENCE_LENGTH = 60
EMBEDDING_DIM = 256
EPOCHS = 100
BATCH_SIZE = 8

# Las preguntas que queremos que el modelo aprenda a predecir
PREGUNTAS_A_PREDECIR = [
    "p1", "p4", "p6", "p7", "p10", "p11", "p13", "p14",
    "p19", "p20", "p22", "p23", "p24",
    "p30", "p31", "p33", "p34", "p35", "p36", "p40", "p42",
    "p48", "p49", "p53", "p54", "p55", "p62", "p63",
]


class ModeloHibridoCorales:
    """Red neuronal que predice características taxonómicas desde texto"""
    
    def __init__(self):
        self.tokenizer = None
        self.label_encoders = {}
        self.modelo = None
        
    def cargar_datos(self):
        print("\n📂 Cargando dataset...")
        df = pd.read_csv(RUTA_DATASET, encoding="utf-8")
        print(f"   Registros: {len(df)}")
        return df
    
    def preparar_datos(self, df):
        print("\n🔤 Tokenizando descripciones...")
        
        self.tokenizer = keras.preprocessing.text.Tokenizer(
            num_words=MAX_VOCAB_SIZE,
            oov_token="<OOV>"
        )
        self.tokenizer.fit_on_texts(df["descripcion"].values)
        
        secuencias = self.tokenizer.texts_to_sequences(df["descripcion"].values)
        X = keras.preprocessing.sequence.pad_sequences(
            secuencias, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post"
        )
        
        respuestas_lista = df["respuestas_cuestionario"].apply(json.loads)
        
        y_dict = {}
        for pregunta_id in PREGUNTAS_A_PREDECIR:
            valores = []
            for resp in respuestas_lista:
                valores.append(resp.get(pregunta_id, "desconocido"))
            
            le = LabelEncoder()
            y_codificado = le.fit_transform(valores)
            y_dict[pregunta_id] = {
                "encoder": le,
                "valores": y_codificado,
                "num_clases": len(le.classes_)
            }
            print(f"   {pregunta_id}: {len(le.classes_)} clases -> {le.classes_.tolist()}")
        
        self.label_encoders = {pid: info["encoder"] for pid, info in y_dict.items()}
        
        print(f"   Forma de X: {X.shape}")
        print(f"   Preguntas a predecir: {len(PREGUNTAS_A_PREDECIR)}")
        
        return X, y_dict
    
    def construir_modelo(self, y_dict):
        print("\n🏗️  Construyendo arquitectura del modelo...")
        
        entrada = layers.Input(shape=(MAX_SEQUENCE_LENGTH,), name="texto_descripcion")
        
        x = layers.Embedding(
            input_dim=min(MAX_VOCAB_SIZE, len(self.tokenizer.word_index) + 1),
            output_dim=EMBEDDING_DIM,
            embeddings_regularizer=keras.regularizers.l2(1e-4),
            name="embedding_taxonomico"
        )(entrada)
        
        attention_output = layers.MultiHeadAttention(
            num_heads=4,
            key_dim=64,
            name="self_attention"
        )(x, x, x)
        
        x = layers.GlobalMaxPooling1D(name="max_pool")(attention_output)
        x = layers.Dense(64, activation="relu", name="dense_shared_1")(x)
        x = layers.Dropout(0.4)(x)
        x = layers.Dense(32, activation="relu", name="dense_shared_2")(x)
        x = layers.Dropout(0.3)(x)
        
        salidas = {}
        for pregunta_id in PREGUNTAS_A_PREDECIR:
            num_clases = y_dict[pregunta_id]["num_clases"]
            nombre_salida = f"salida_{pregunta_id}"
            if num_clases == 2:
                salidas[nombre_salida] = layers.Dense(1, activation="sigmoid", name=nombre_salida)(x)
            else:
                salidas[nombre_salida] = layers.Dense(num_clases, activation="softmax", name=nombre_salida)(x)
        
        self.modelo = keras.Model(inputs=entrada, outputs=salidas, name="CoralFeaturePredictor")
        
        losses = {}
        metrics = {}
        for pregunta_id in PREGUNTAS_A_PREDECIR:
            nombre_salida = f"salida_{pregunta_id}"
            num_clases = y_dict[pregunta_id]["num_clases"]
            if num_clases == 2:
                losses[nombre_salida] = "binary_crossentropy"
            else:
                losses[nombre_salida] = "sparse_categorical_crossentropy"
            metrics[nombre_salida] = ["accuracy"]
        
        self.modelo.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss=losses,
            metrics=metrics
        )
        
        print(self.modelo.summary())
        return self.modelo
    
    def entrenar(self, X, y_dict):
        print("\n🚀 Iniciando entrenamiento...")
        
        y_outputs = {}
        for pregunta_id in PREGUNTAS_A_PREDECIR:
            nombre_salida = f"salida_{pregunta_id}"
            y_outputs[nombre_salida] = np.array(y_dict[pregunta_id]["valores"])
        
        indices = np.arange(len(X))
        train_idx, val_idx = train_test_split(indices, test_size=0.3, random_state=42)
        
        X_train, X_val = X[train_idx], X[val_idx]
        y_train = {k: v[train_idx] for k, v in y_outputs.items()}
        y_val = {k: v[val_idx] for k, v in y_outputs.items()}
        
        print(f"   Train: {len(train_idx)} muestras")
        print(f"   Validation: {len(val_idx)} muestras")
        
        early_stopping = keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=20,
            restore_best_weights=True,
            verbose=1
        )
        
        historia = self.modelo.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            callbacks=[early_stopping],
            verbose=1
        )
        
        print("\n📊 Evaluación en validación:")
        for pregunta_id in PREGUNTAS_A_PREDECIR:
            nombre_salida = f"salida_{pregunta_id}"
            y_true = y_val[nombre_salida]
            y_pred = self.modelo.predict(X_val, verbose=0)
            y_pred = y_pred[nombre_salida]
            
            if y_dict[pregunta_id]["num_clases"] == 2:
                y_pred_clases = (y_pred > 0.5).astype(int).flatten()
            else:
                y_pred_clases = np.argmax(y_pred, axis=1)
            
            accuracy = np.mean(y_true == y_pred_clases)
            print(f"   {pregunta_id}: accuracy = {accuracy:.2%}")
        
        return historia
    
    def guardar(self):
        print("\n💾 Guardando modelo y artefactos...")
        os.makedirs("models", exist_ok=True)
        self.modelo.save(RUTA_MODELO)
        with open(RUTA_TOKENIZER, "wb") as f:
            pickle.dump(self.tokenizer, f)
        with open(RUTA_ENCODERS, "wb") as f:
            pickle.dump(self.label_encoders, f)
        print(f"   Modelo: {RUTA_MODELO}")
        print(f"   Tokenizer: {RUTA_TOKENIZER}")
        print(f"   Label Encoders: {RUTA_ENCODERS}")
    
    def ejecutar_pipeline(self):
        df = self.cargar_datos()
        X, y_dict = self.preparar_datos(df)
        self.construir_modelo(y_dict)
        self.entrenar(X, y_dict)
        self.guardar()
        return self


def _norm(w: str) -> str:
    w = w.lower().strip()
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u")]:
        w = w.replace(a, b)
    if len(w) > 3 and w.endswith("s"):
        w = w[:-1]
    return w


class PredictorCorales:
    """Carga el modelo entrenado y predice características desde texto.
       Integrado con PonderadorCaracteristicas para análisis taxonómico preciso."""
    
    def __init__(self):
        self.modelo = None
        self.tokenizer = None
        self.label_encoders = {}
        self.ponderador = PonderadorCaracteristicas()
        
        if os.path.exists(RUTA_MODELO):
            self.modelo = keras.models.load_model(RUTA_MODELO)
        if os.path.exists(RUTA_TOKENIZER):
            with open(RUTA_TOKENIZER, "rb") as f:
                self.tokenizer = pickle.load(f)
        if os.path.exists(RUTA_ENCODERS):
            with open(RUTA_ENCODERS, "rb") as f:
                self.label_encoders = pickle.load(f)
    
    def esta_cargado(self):
        return self.modelo is not None and self.tokenizer is not None
    
    def predecir_caracteristicas(self, texto):
        if not self.esta_cargado():
            return {"success": False, "error": "Modelo no cargado."}
        
        secuencia = self.tokenizer.texts_to_sequences([texto])
        secuencia_padded = keras.preprocessing.sequence.pad_sequences(
            secuencia, maxlen=MAX_SEQUENCE_LENGTH, padding="post", truncating="post"
        )
        
        predicciones = self.modelo.predict(secuencia_padded, verbose=0)
        
        respuestas = {}
        confianzas = []
        for pregunta_id in PREGUNTAS_A_PREDECIR:
            nombre_salida = f"salida_{pregunta_id}"
            pred = predicciones[nombre_salida][0]
            encoder = self.label_encoders[pregunta_id]
            
            if len(encoder.classes_) == 2:
                prob = pred[0]
                conf = max(prob, 1.0 - prob)
                valor_idx = int(prob > 0.5)
            else:
                conf = np.max(pred)
                valor_idx = int(np.argmax(pred))
            
            valor = encoder.classes_[valor_idx]
            
            if valor == "desconocido":
                confianzas.append(0.0)
            else:
                confianzas.append(conf)
                respuestas[pregunta_id] = valor
        
        confianza_promedio = float(np.mean(confianzas)) if confianzas else 0.0
        baja_confianza = (confianza_promedio < 0.5) or (len(respuestas) < 3)
        
        return {
            "success": True,
            "respuestas": respuestas,
            "texto_analizado": texto,
            "baja_confianza": baja_confianza,
            "confianza_promedio": confianza_promedio,
        }

    def predecir_con_ponderacion(self, texto: str) -> dict:
        """
        Predicción combinada: red neuronal (características) + ponderación taxonómica (ranking).
        """
        resultado_red = self.predecir_caracteristicas(texto)
        respuestas_predichas = resultado_red.get("respuestas", {})
        
        # Obtener las 5 especies sugeridas por el ponderador taxonómico unificado
        diagnostico = self.ponderador.diagnosticar(texto)
        top_especies = diagnostico.get("top_especies", [])
        
        # Mapear cada elemento al formato que espera la interfaz Flet
        especies_db = self.ponderador.especies
        dict_especies = {e["id"]: e for e in especies_db}
        
        try:
            from src.generador_dataset import caracteristicas_a_respuestas
        except ImportError:
            try:
                from .generador_dataset import caracteristicas_a_respuestas
            except ImportError:
                caracteristicas_a_respuestas = None
                
        ranking = []
        for item in top_especies:
            esp_id = item["id"]
            esp = dict_especies.get(esp_id)
            if not esp:
                continue
                
            # Construir desglose de coincidencias para la UI
            respuestas_esp = {}
            if caracteristicas_a_respuestas:
                respuestas_esp = caracteristicas_a_respuestas(esp_id, esp.get("caracteristicas", {}))
                
            coincidencias = {}
            claves_ranking = ["p1", "p4", "p6", "p7", "p10", "p11", "p19", "p20", "p22", "p30"]
            for k in claves_ranking:
                v_usuario = respuestas_predichas.get(k)
                if v_usuario and v_usuario != "desconocido":
                    v_esp = respuestas_esp.get(k)
                    is_match = (v_esp == v_usuario)
                    coincidencias[k] = {
                        "match": is_match,
                        "predicho": v_usuario,
                        "especie": v_esp
                    }
                    
            ranking.append({
                "especie": esp,
                "score": item["score"],
                "tax_score": item["score"],
                "text_score": item["score"],
                "coincidencias": coincidencias
            })
            
        return {
            "success": resultado_red.get("success", False),
            "respuestas_red": respuestas_predichas,
            "baja_confianza": resultado_red.get("baja_confianza", True),
            "confianza_ponderacion": diagnostico.get("confianza", "BAJA"),
            "categorias_detectadas": diagnostico["evidencias"].get("evidencias_por_categoria", {}),
            "ranking": ranking,
            "texto_analizado": texto,
        }


# ─── EJECUCIÓN DIRECTA ───
if __name__ == "__main__":
    print("=" * 60)
    print("🪸 CORAL FEATURE PREDICTOR - ENTRENAMIENTO")
    print("=" * 60)
    
    modelo = ModeloHibridoCorales()
    modelo.ejecutar_pipeline()
    
    print("\n" + "=" * 60)
    print("✅ Pipeline completado. Modelo listo para usar.")
    print("=" * 60)

