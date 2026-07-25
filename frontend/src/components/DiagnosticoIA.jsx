import React, { useState } from 'react';
import { Sparkles, Brain, Cpu, Award, Layers, Tag, CheckCircle2, ImageOff, Lightbulb, Info } from 'lucide-react';
import ModalExplicacionIA from './ModalExplicacionIA';

export default function DiagnosticoIA({ apiBase }) {
  const [texto, setTexto] = useState('');
  const [cargando, setCargando] = useState(false);
  const [resultado, setResultado] = useState(null);
  const [error, setError] = useState(null);
  const [candidatoExplicar, setCandidatoExplicar] = useState(null);

  // Chips/Pills recomendadores visuales para guiar la redacción del usuario
  const ejemplos = [
    { titulo: 'Cuerno de Alce', texto: 'Coral con ramas aplanadas grandes como paletas de color marrón claro en zona de oleaje somera' },
    { titulo: 'Coral Cerebro', texto: 'Coral grande redondo masivo con surcos profundos continuos como cerebro de color gris verdoso' },
    { titulo: 'Coral de Fuego', texto: 'Coral incrustante ramificado de superficie lisa sin hoyitos visibles de color amarillo mostaza' }
  ];

  const agregarPalabraClave = (palabra) => {
    setTexto((prev) => {
      if (!prev.trim()) return palabra;
      if (prev.toLowerCase().includes(palabra.toLowerCase())) return prev;
      return `${prev}, ${palabra}`;
    });
  };

  const ejecutarDiagnostico = async (promptTexto) => {
    const textoAProcesar = promptTexto || texto;
    if (!textoAProcesar || textoAProcesar.trim().length < 3) {
      setError('Por favor introduce una descripción más detallada del coral.');
      return;
    }

    setCargando(true);
    setError(null);
    try {
      const res = await fetch(`${apiBase}/ia/diagnostico`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto: textoAProcesar }),
      });
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Error al procesar el diagnóstico con la IA');
      }
      const data = await res.json();
      setResultado(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="animate-fade-in" style={{ maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* ── SECCIÓN PRINCIPAL EN 2 COLUMNAS ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', alignItems: 'start' }}>
        
        {/* ── COLUMNA IZQUIERDA: INPUT + RECOMENDADORES VISUALES ── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* Header Compacto */}
          <div className="liquid-glass" style={{ padding: '20px 24px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div className="icon-circle icon-circle-coral" style={{ width: '40px', height: '40px' }}>
                <Sparkles size={20} />
              </div>
              <div>
                <span className="badge badge-coral" style={{ fontSize: '0.68rem' }}>Deep Learning + Ponderación</span>
                <h2 style={{ fontSize: '1.35rem', fontWeight: 800, marginTop: '2px', letterSpacing: '-0.5px' }}>
                  Diagnóstico por Lenguaje Natural
                </h2>
              </div>
            </div>
          </div>

          {/* Formulario de Entrada */}
          <div className="liquid-glass" style={{ padding: '24px' }}>
            <label style={{ display: 'block', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '8px', fontSize: '0.9rem' }}>
              Describe la apariencia y características del coral:
            </label>
            <textarea
              rows={4}
              value={texto}
              onChange={(e) => setTexto(e.target.value)}
              placeholder="Ejemplo: Observé un coral de color marrón claro en zona somera con ramas grandes aplanadas como paletas..."
              className="input-glass"
              style={{ resize: 'none', fontSize: '0.9rem', lineHeight: 1.5, position: 'relative', zIndex: 2 }}
            />

            {/* SUGERENCIAS SIMPLES EN 1 SOLA LÍNEA */}
            <div style={{ marginTop: '10px', display: 'flex', alignItems: 'center', gap: '6px', flexWrap: 'wrap' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px', flexShrink: 0 }}>
                <Lightbulb size={13} color="var(--accent-primary)" /> Sugerencias:
              </span>
              {['marrón', 'ramificada', 'masiva', 'copas', 'lisa', 'somera', 'coralitos'].map((tag, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => agregarPalabraClave(tag)}
                  style={{
                    background: 'rgba(62, 207, 180, 0.08)',
                    border: '1px solid rgba(62, 207, 180, 0.2)',
                    borderRadius: 'var(--radius-pill)',
                    padding: '3px 10px',
                    color: 'var(--text-secondary)',
                    fontSize: '0.74rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => { e.currentTarget.style.borderColor = 'var(--accent-primary)'; e.currentTarget.style.color = 'var(--accent-primary)'; }}
                  onMouseOut={(e) => { e.currentTarget.style.borderColor = 'rgba(62, 207, 180, 0.2)'; e.currentTarget.style.color = 'var(--text-secondary)'; }}
                >
                  + {tag}
                </button>
              ))}
            </div>

            {/* Ejemplos Rápida Demostración */}
            <div style={{ marginTop: '14px', display: 'flex', gap: '6px', flexWrap: 'wrap', alignItems: 'center' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-tertiary)' }}>Prueba:</span>
              {ejemplos.map((ex, idx) => (
                <button
                  key={idx}
                  onClick={() => { setTexto(ex.texto); ejecutarDiagnostico(ex.texto); }}
                  style={{
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid var(--liquid-border)',
                    borderRadius: 'var(--radius-pill)',
                    padding: '4px 12px',
                    color: 'var(--text-secondary)',
                    fontSize: '0.75rem',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                  onMouseOver={(e) => { e.currentTarget.style.borderColor = 'var(--accent-primary)'; e.currentTarget.style.color = 'var(--accent-primary)'; }}
                  onMouseOut={(e) => { e.currentTarget.style.borderColor = 'var(--liquid-border)'; e.currentTarget.style.color = 'var(--text-secondary)'; }}
                >
                  ⚡ {ex.titulo}
                </button>
              ))}
            </div>

            {/* Botón Diagnosticar */}
            <div style={{ marginTop: '18px', display: 'flex', justifyContent: 'flex-end' }}>
              <button onClick={() => ejecutarDiagnostico()} disabled={cargando} className="btn-primary" style={{ padding: '10px 24px', fontSize: '0.9rem' }}>
                {cargando ? 'Procesando Red Neuronal...' : <><Sparkles size={16} /> Ejecutar Diagnóstico IA</>}
              </button>
            </div>

            {error && (
              <div style={{ marginTop: '12px', color: 'var(--accent-coral)', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '6px' }}>
                ⚠️ {error}
              </div>
            )}
          </div>
        </div>

        {/* ── COLUMNA DERECHA: RESULTADO CORRECTO + CANDIDATOS SIMILARES ── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* Placeholder cuando aún no se ha ejecutado un diagnóstico */}
          {!resultado && !cargando && (
            <div className="liquid-glass" style={{ padding: '48px 28px', textAlign: 'center', color: 'var(--text-tertiary)', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '14px' }}>
              <div className="icon-circle icon-circle-cyan" style={{ width: '54px', height: '54px' }}>
                <Brain size={28} />
              </div>
              <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-secondary)' }}>
                Esperando descripción taxonómica
              </h3>
              <p style={{ fontSize: '0.85rem', maxWidth: '340px', lineHeight: 1.5 }}>
                Escribe las características del coral a la izquierda o haz clic en uno de los ejemplos para visualizar el resultado y las especies similares aquí.
              </p>
            </div>
          )}

          {/* Loader de IA */}
          {cargando && (
            <div className="liquid-glass" style={{ padding: '48px 28px', textAlign: 'center', color: 'var(--text-secondary)' }}>
              <div className="pulse-glow" style={{ display: 'inline-block', padding: '16px 32px', borderRadius: 'var(--radius-md)' }}>
                Clasificando con Red Neuronal TensorFlow y Motor de Ponderación...
              </div>
            </div>
          )}

          {/* RESULTADO IA (ESPECIE CORRECTA + SIMILARES) */}
          {resultado && !cargando && (
            <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              
              {/* 🏆 TARJETA DE RESPUESTA CORRECTA (TOP #1) CLICKABLE */}
              <div
                className="liquid-glass liquid-glass-accent liquid-glass-interactive"
                onClick={() => setCandidatoExplicar(resultado.top_candidatos[0] || resultado.especie_ganadora)}
                style={{ padding: '24px', cursor: 'pointer' }}
              >
                <div style={{ display: 'flex', gap: '16px', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap' }}>
                  
                  {/* Recuadro Fotografía de la Especie */}
                  <div style={{ width: '110px', height: '110px', borderRadius: 'var(--radius-md)', overflow: 'hidden', flexShrink: 0, border: '2px solid var(--accent-primary)', boxShadow: '0 8px 24px rgba(62, 207, 180, 0.25)', position: 'relative', background: 'rgba(0,0,0,0.4)' }}>
                    <img
                      src={`${apiBase}/imagenes/${resultado.especie_ganadora.especie?.toLowerCase().replace(/ /g, '_')}.jpg`}
                      alt={resultado.especie_ganadora.especie}
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                      onError={(e) => {
                        e.target.onerror = null;
                        e.target.parentElement.style.display = 'none';
                      }}
                    />
                  </div>

                  {/* Nombre e Identificación */}
                  <div style={{ flex: 1, minWidth: '180px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                      <CheckCircle2 size={16} color="var(--accent-primary)" />
                      <span className="badge badge-cyan" style={{ fontSize: '0.68rem' }}>Mejor Coincidencia IA</span>
                    </div>
                    <h3 style={{ fontSize: '1.5rem', fontWeight: 800, lineHeight: 1.2 }}>
                      {resultado.especie_ganadora.especie}
                    </h3>
                    <p style={{ color: 'var(--accent-primary)', fontSize: '0.95rem', fontWeight: 600, marginTop: '2px' }}>
                      "{resultado.especie_ganadora.nombre_comun}"
                    </p>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)', marginTop: '4px' }}>
                      Familia: <strong style={{ color: 'var(--text-secondary)' }}>{resultado.especie_ganadora.familia}</strong>
                    </div>
                  </div>

                  {/* Puntuación % */}
                  <div style={{ textAlign: 'center', background: 'rgba(62,207,180,0.1)', padding: '12px 18px', borderRadius: 'var(--radius-md)', border: '1px solid rgba(62,207,180,0.3)', flexShrink: 0 }}>
                    <div style={{ fontSize: '0.68rem', textTransform: 'uppercase', color: 'var(--text-tertiary)' }}>Similitud IA</div>
                    <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--accent-primary)' }}>
                      {(resultado.especie_ganadora.score * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>

                {/* Sub-panel Deducido con Botón Ver Justificación */}
                <div style={{ background: 'rgba(0,0,0,0.18)', padding: '12px 16px', borderRadius: 'var(--radius-md)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--text-secondary)' }}>
                    <Brain size={14} color="var(--accent-coral)" />
                    Atributos Red Neuronal: <strong>{Object.keys(resultado.respuestas_deducidas).length}</strong>
                  </div>
                  <span style={{ fontSize: '0.78rem', color: 'var(--accent-primary)', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Info size={14} /> Ver Explicación Algorítmica →
                  </span>
                </div>
              </div>

              {/* 📋 LISTADO DE CANDIDATOS SIMILARES CLICKABLES */}
              <div className="liquid-glass" style={{ padding: '20px' }}>
                <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Award size={18} color="var(--accent-amber)" /> Especies Similares (Haz clic para ver explicación)
                </h3>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {resultado.top_candidatos.slice(1).map((cand, idx) => (
                    <div
                      key={idx}
                      className="liquid-glass liquid-glass-interactive"
                      onClick={() => setCandidatoExplicar(cand)}
                      style={{
                        padding: '14px 18px',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        gap: '12px',
                        borderRadius: 'var(--radius-md)',
                        cursor: 'pointer'
                      }}
                    >
                      <div style={{ flex: 1, overflow: 'hidden' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <span style={{ fontSize: '0.75rem', fontWeight: 800, color: 'var(--accent-primary)' }}>#{idx + 2}</span>
                          <h4 style={{ fontSize: '0.95rem', fontWeight: 700, fontStyle: 'italic', color: 'var(--text-primary)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                            {cand.especie}
                          </h4>
                        </div>
                        <div style={{ fontSize: '0.82rem', color: 'var(--accent-primary)', marginTop: '2px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                          "{cand.nombre_comun}" — <span style={{ color: 'var(--text-tertiary)' }}>{cand.familia}</span>
                        </div>
                      </div>

                      <div style={{ textAlign: 'right', flexShrink: 0 }}>
                        <span className="badge badge-cyan" style={{ fontSize: '0.78rem', fontWeight: 700, padding: '4px 10px' }}>
                          {(cand.score_final * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          )}

        </div>

      </div>

      {/* Modal Explicativo de Justificación Algorítmica IA */}
      {candidatoExplicar && (
        <ModalExplicacionIA
          candidato={candidatoExplicar}
          desgloseGeneral={resultado?.desglose_explicativo}
          respuestasDeducidas={resultado?.respuestas_deducidas}
          apiBase={apiBase}
          onClose={() => setCandidatoExplicar(null)}
        />
      )}
    </div>
  );
}
