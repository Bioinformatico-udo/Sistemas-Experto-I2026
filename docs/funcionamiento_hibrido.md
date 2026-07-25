# 🧠 Motor Híbrido CoraAI: Simbólico + Subsimbólico

El núcleo de inteligencia artificial de **CoraAI** combina dos paradigmas fundamentales de la ciencia de la computación: la **IA Simbólica** (Reglas y Árboles Dicotómicos) y la **IA Subsimbólica** (Redes Neuronales de Aprendizaje Profundo y Ponderación Semántica).

---

## 📐 1. Componente Simbólico (Árbol Dicotómico de Inferencia)

- **Fundamento**: Basado en las claves taxonómicas tradicionales de la biología marina para el orden *Scleractinia*.
- **Módulo**: `src/motor_inferencia.py` & `data/reglas.json`.
- **Funcionamiento**:
  - Cada nodo representa una pregunta sobre un carácter morfológico clave (ej. *presencia de cresta tecal*, *morfología de la colonia*, *diámetro de coralitos*).
  - Las respuestas del usuario navegan determinísticamente por las ramas del árbol hasta llegar a una hoja que identifica la especie con certidumbre absoluta del 100%.

---

## ⚡ 2. Componente Subsimbólico (Red Neuronal + Ponderación Semántica)

- **Fundamento**: Capacidad de procesar lenguaje natural no estructurado donde el usuario describe un espécimen con sus propias palabras.
- **Módulos**: `src/modelo_hibrido.py` & `src/motor_ponderacion.py`.
- **Red Neuronal (TensorFlow/Keras)**:
  - Arquitectura entrenada sobre el dataset morfológico (`data/dataset_entrenamiento.csv`).
  - Tokeniza y procesa el texto del usuario extraendo vectores de características biológicas.
- **Motor de Ponderación Semántica**:
  - Analiza coincidencias parciales y calcula pesos ponderados según la rareza y especificidad de cada rasgo morfológico dentro de la fauna del Archipiélago de Los Roques.

---

## 🤝 3. Integración Híbrida y Matriz de Confianza

Cuando el usuario ejecuta un diagnóstico por lenguaje natural:
1. La **Red Neuronal** extrae las características clave deducidas.
2. El **Motor de Inferencia Simbólico** evalúa cuáles reglas del árbol dicotómico son satisfechas por dichas características.
3. El **Motor de Ponderación** fusiona ambos puntajes mediante una ecuación ponderada:
   $$\text{Score Final} = \alpha \cdot \text{Similitud Ponderada} + \beta \cdot \text{Coincidencia Reglas Dicotómicas}$$
4. El sistema genera un ranking ordenado de candidatos y expone la justificación algorítmica completa a través del **Modal de Explicación IA (XAI)**.
