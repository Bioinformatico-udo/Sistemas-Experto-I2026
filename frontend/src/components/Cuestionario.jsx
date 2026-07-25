import React, { useState, useEffect } from 'react';
import { ArrowLeft, RotateCcw, CheckCircle2, AlertTriangle, ShieldCheck, Info, Sparkles, Filter } from 'lucide-react';

export default function Cuestionario({ apiBase }) {
  const [respuestas, setRespuestas] = useState({});
  const [historial, setHistorial] = useState([]);
  const [preguntaActual, setPreguntaActual] = useState(null);
  const [resultadoFinal, setResultadoFinal] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState(null);

  // Lista de especies para la columna derecha de filtrado dinámico
  const [todasLasEspecies, setTodasLasEspecies] = useState([]);

  const totalPasosEstimados = 8;

  useEffect(() => {
    // Cargar especies completas para el panel de filtrado en vivo
    async function fetchEspecies() {
      try {
        const res = await fetch(`${apiBase}/especies`);
        const data = await res.json();
        setTodasLasEspecies(data);
      } catch (err) {
        console.error('Error cargando especies para filtrado:', err);
      }
    }
    fetchEspecies();
    cargarSiguientePaso({});
  }, [apiBase]);

  const cargarSiguientePaso = async (respuestasActuales) => {
    setCargando(true);
    setError(null);
    try {
      const res = await fetch(`${apiBase}/inferencia/paso`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ respuestas: respuestasActuales }),
      });
      if (!res.ok) throw new Error('Error al conectar con el motor de inferencia');
      const data = await res.json();

      if (data.estado === 'pregunta') {
        setPreguntaActual(data.pregunta_detalle);
        setResultadoFinal(null);
      } else {
        setResultadoFinal(data);
        setPreguntaActual(null);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  const seleccionarOpcion = (valor) => {
    if (!preguntaActual) return;
    const nuevasRespuestas = { ...respuestas, [preguntaActual.id]: valor };
    setHistorial([...historial, { pregunta: preguntaActual, respuestasPrevias: respuestas }]);
    setRespuestas(nuevasRespuestas);
    cargarSiguientePaso(nuevasRespuestas);
  };

  const retrocederPaso = () => {
    if (historial.length === 0) return;
    const ultimoPaso = historial[historial.length - 1];
    setHistorial(historial.slice(0, -1));
    setRespuestas(ultimoPaso.respuestasPrevias);
    setPreguntaActual(ultimoPaso.pregunta);
    setResultadoFinal(null);
  };

  const reiniciar = () => {
    setRespuestas({});
    setHistorial([]);
    setResultadoFinal(null);
    setPreguntaActual(null);
    cargarSiguientePaso({});
  };

  const pasoNumero = historial.length + 1;
  const progresoPorcentaje = Math.min(100, Math.round((historial.length / totalPasosEstimados) * 100));

  // Filtrado dinámico de especies candidatas según las respuestas acumuladas
  const especiesCompatibles = todasLasEspecies.filter((esp) => {
    if (resultadoFinal && resultadoFinal.success) {
      return (
        esp.nombre_cientifico.toLowerCase() === resultadoFinal.especie?.toLowerCase() ||
        esp.id === resultadoFinal.especie_id
      );
    }

    // Filtrado por p1 (Presencia de coralitos / Hidrocorales)
    if (respuestas.p1 === 'no') {
      if (esp.tipo !== 'Hidrocoral' && esp.caracteristicas?.tiene_coralitos !== false) return false;
    } else if (respuestas.p1 === 'si') {
      if (esp.tipo === 'Hidrocoral' || esp.caracteristicas?.tiene_coralitos === false) return false;
    }

    return true;
  });

  return (
    <div className="animate-fade-in" style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* ── SECCIÓN EN 2 COLUMNAS ── */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 360px', gap: '24px', alignItems: 'start' }}>
        
        {/* ── COLUMNA IZQUIERDA: PREGUNTAS / RESULTADOS ── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* Header Compacto + Barra de Progreso */}
          <div className="liquid-glass" style={{ padding: '20px 24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: preguntaActual ? '12px' : 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <h2 style={{ fontSize: '1.35rem', fontWeight: 800, letterSpacing: '-0.5px' }}>
                  Diagnóstico Guiado Dicotómico
                </h2>
                <span className="badge badge-cyan" style={{ fontSize: '0.7rem' }}>
                  Paso {pasoNumero}
                </span>
              </div>

              {historial.length > 0 && (
                <button onClick={reiniciar} className="btn-secondary" style={{ padding: '6px 14px', fontSize: '0.82rem' }}>
                  <RotateCcw size={14} /> Reiniciar
                </button>
              )}
            </div>

            {preguntaActual && (
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  <span>Progreso de inferencia</span>
                  <span style={{ fontWeight: 700, color: 'var(--accent-primary)' }}>{progresoPorcentaje}%</span>
                </div>
                <div className="progress-track" style={{ height: '5px' }}>
                  <div className="progress-fill" style={{ width: `${progresoPorcentaje}%` }} />
                </div>
              </div>
            )}
          </div>

          {/* Estado de Carga */}
          {cargando && (
            <div className="liquid-glass" style={{ padding: '40px', textAlign: 'center', color: 'var(--text-secondary)' }}>
              <div className="pulse-glow" style={{ display: 'inline-block', padding: '14px 28px', borderRadius: 'var(--radius-md)' }}>
                Recorriendo árbol dicotómico...
              </div>
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="liquid-glass liquid-glass-coral" style={{ padding: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: 'var(--accent-coral)' }}>
                <AlertTriangle size={20} />
                <h3 style={{ margin: 0, fontSize: '1rem' }}>Error de Inferencia</h3>
              </div>
              <p style={{ marginTop: '6px', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>{error}</p>
              <button onClick={reiniciar} className="btn-primary" style={{ marginTop: '14px', padding: '8px 18px', fontSize: '0.85rem' }}>Reintentar</button>
            </div>
          )}

          {/* Pregunta Actual */}
          {!cargando && preguntaActual && (
            <div className="liquid-glass animate-fade-in" style={{ padding: '28px' }}>
              <div style={{ marginBottom: '20px' }}>
                <span style={{ color: 'var(--accent-primary)', fontWeight: 700, fontSize: '0.75rem', letterSpacing: '0.5px', textTransform: 'uppercase' }}>
                  Pregunta {preguntaActual.id.toUpperCase()}
                </span>
                <h3 style={{ fontSize: '1.25rem', fontWeight: 700, marginTop: '4px', lineHeight: 1.35 }}>
                  {preguntaActual.texto}
                </h3>
                {preguntaActual.descripcion && (
                  <p style={{ color: 'var(--text-secondary)', marginTop: '8px', fontSize: '0.88rem', display: 'flex', alignItems: 'flex-start', gap: '8px', lineHeight: 1.5 }}>
                    <Info size={15} color="var(--accent-primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
                    {preguntaActual.descripcion}
                  </p>
                )}
              </div>

              {/* Botones de Opciones */}
              <div style={{ display: 'grid', gap: '10px', marginBottom: '20px' }}>
                {preguntaActual.opciones.map((opcion, idx) => (
                  <button
                    key={idx}
                    onClick={() => seleccionarOpcion(opcion.valor)}
                    className="liquid-glass liquid-glass-interactive"
                    style={{
                      padding: '16px 18px',
                      textAlign: 'left',
                      color: 'var(--text-primary)',
                      fontSize: '0.95rem',
                      fontWeight: 500,
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      borderLeft: opcion.principal ? '3px solid var(--accent-primary)' : '3px solid transparent',
                      fontFamily: 'inherit'
                    }}
                  >
                    <span style={{ position: 'relative', zIndex: 2 }}>{opcion.label}</span>
                    <span style={{ fontSize: '0.78rem', opacity: 0.6, color: 'var(--accent-primary)', position: 'relative', zIndex: 2 }}>Seleccionar →</span>
                  </button>
                ))}
              </div>

              {historial.length > 0 && (
                <button onClick={retrocederPaso} className="btn-secondary" style={{ fontSize: '0.85rem', padding: '8px 16px' }}>
                  <ArrowLeft size={15} /> Pregunta anterior
                </button>
              )}
            </div>
          )}

          {/* Resultado Final de la Inferencia */}
          {!cargando && resultadoFinal && (
            <div className={`liquid-glass animate-fade-in ${resultadoFinal.success ? 'liquid-glass-accent' : ''}`} style={{ padding: '28px', borderLeftWidth: resultadoFinal.success ? '4px' : undefined }}>
              {resultadoFinal.success ? (
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '16px', flexWrap: 'wrap' }}>
                    {/* Recuadro Estilizado para la Fotografía de la Especie */}
                    <div style={{ width: '110px', height: '110px', borderRadius: 'var(--radius-md)', overflow: 'hidden', flexShrink: 0, border: '2px solid var(--accent-primary)', boxShadow: '0 8px 24px rgba(62, 207, 180, 0.25)', position: 'relative', background: 'rgba(0,0,0,0.4)' }}>
                      <img
                        src={`${apiBase}/imagenes/${(resultadoFinal.especie_id || resultadoFinal.especie?.toLowerCase().replace(/ /g, '_'))}.jpg`}
                        alt={resultadoFinal.especie}
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                        onError={(e) => {
                          e.target.onerror = null;
                          e.target.parentElement.style.display = 'none';
                        }}
                      />
                    </div>

                    <div style={{ flex: 1, minWidth: '180px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                        <CheckCircle2 size={18} color="var(--accent-primary)" />
                        <span className="badge badge-cyan" style={{ fontSize: '0.68rem' }}>Identificación Confirmada</span>
                      </div>
                      <h2 style={{ fontSize: '1.55rem', fontWeight: 800, marginTop: '2px', lineHeight: 1.2 }}>
                        {resultadoFinal.especie}
                      </h2>
                      <p style={{ color: 'var(--accent-primary)', fontSize: '0.95rem', fontWeight: 600, marginTop: '2px' }}>
                        "{resultadoFinal.nombre_comun}"
                      </p>
                    </div>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px', background: 'rgba(0,0,0,0.15)', padding: '14px', borderRadius: 'var(--radius-md)', margin: '16px 0' }}>
                    <div>
                      <div style={{ color: 'var(--text-tertiary)', fontSize: '0.7rem', textTransform: 'uppercase' }}>Familia</div>
                      <div style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-secondary)', marginTop: '2px' }}>{resultadoFinal.familia}</div>
                    </div>
                    <div>
                      <div style={{ color: 'var(--text-tertiary)', fontSize: '0.7rem', textTransform: 'uppercase' }}>Orden</div>
                      <div style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--text-secondary)', marginTop: '2px' }}>{resultadoFinal.orden}</div>
                    </div>
                    <div>
                      <div style={{ color: 'var(--text-tertiary)', fontSize: '0.7rem', textTransform: 'uppercase' }}>Origen</div>
                      <div style={{ fontSize: '0.92rem', fontWeight: 600, color: 'var(--accent-primary)', marginTop: '2px' }}>Los Roques</div>
                    </div>
                  </div>

                  <div className="liquid-glass" style={{ padding: '14px 16px', marginBottom: '20px', borderLeft: '3px solid var(--accent-primary)' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-primary)', fontWeight: 600, marginBottom: '2px', fontSize: '0.85rem' }}>
                      <ShieldCheck size={15} /> Verificación Taxonómica
                    </div>
                    <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5, position: 'relative', zIndex: 2 }}>
                      Especie validada a través de la clave dicotómica de corales autóctonos del Parque Nacional Archipiélago de Los Roques.
                    </p>
                  </div>
                </div>
              ) : (
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '14px' }}>
                    <AlertTriangle size={28} color="var(--accent-amber)" />
                    <div>
                      <span className="badge badge-amber" style={{ fontSize: '0.68rem' }}>Sin Coincidencia Directa</span>
                      <h2 style={{ fontSize: '1.4rem', fontWeight: 700, marginTop: '2px' }}>{resultadoFinal.especie}</h2>
                    </div>
                  </div>
                  <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', marginBottom: '14px', lineHeight: 1.5 }}>
                    {resultadoFinal.mensaje}
                  </p>
                </div>
              )}

              <div style={{ display: 'flex', gap: '10px' }}>
                <button onClick={reiniciar} className="btn-primary" style={{ padding: '8px 20px', fontSize: '0.88rem' }}>
                  <RotateCcw size={15} /> Nuevo Diagnóstico
                </button>
                {historial.length > 0 && (
                  <button onClick={retrocederPaso} className="btn-secondary" style={{ padding: '8px 16px', fontSize: '0.85rem' }}>
                    <ArrowLeft size={15} /> Cambiar Respuestas
                  </button>
                )}
              </div>
            </div>
          )}
        </div>

        {/* ── COLUMNA DERECHA: CANDIDATOS COMPATIBLES EN VIVO ── */}
        <div className="liquid-glass" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '14px', position: 'sticky', top: '90px' }}>
          {/* Header de Candidatos */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--liquid-border)', paddingBottom: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Filter size={16} color="var(--accent-primary)" />
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                Especies Candidatas
              </h3>
            </div>
            <span className="badge badge-cyan" style={{ fontSize: '0.7rem' }}>
              {especiesCompatibles.length} compatibles
            </span>
          </div>

          <p style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)', lineHeight: 1.4 }}>
            A medida que respondes las preguntas, el motor filtra en vivo las especies compatibles de la base de conocimiento:
          </p>

          {/* Listado Vertical de Candidatos Mas Espaciosos */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '68vh', overflowY: 'auto', paddingRight: '4px' }}>
            {especiesCompatibles.length === 0 ? (
              <div style={{ padding: '24px 12px', textAlign: 'center', color: 'var(--text-tertiary)', fontSize: '0.85rem' }}>
                No hay especies que coincidan con esta combinación de respuestas.
              </div>
            ) : (
              especiesCompatibles.map((esp) => {
                const esResultadoGanador = resultadoFinal?.success && (
                  esp.nombre_cientifico.toLowerCase() === resultadoFinal.especie?.toLowerCase()
                );

                return (
                  <div
                    key={esp.id}
                    className="liquid-glass"
                    style={{
                      padding: '14px 18px',
                      minHeight: '64px',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      gap: '14px',
                      borderRadius: 'var(--radius-md)',
                      background: esResultadoGanador ? 'rgba(62, 207, 180, 0.18)' : 'rgba(255, 255, 255, 0.03)',
                      border: esResultadoGanador ? '1.5px solid var(--accent-primary)' : '1px solid var(--liquid-border)',
                      transition: 'all 0.25s ease'
                    }}
                  >
                    <div style={{ flex: 1, overflow: 'hidden' }}>
                      <h4 style={{ fontSize: '0.98rem', fontWeight: 700, fontStyle: 'italic', color: 'var(--text-primary)', lineHeight: 1.3, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {esp.nombre_cientifico}
                      </h4>
                      <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--accent-primary)', marginTop: '4px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        "{esp.nombre_comun}"
                      </div>
                    </div>

                    <span className="badge badge-cyan" style={{ fontSize: '0.72rem', padding: '5px 10px', flexShrink: 0 }}>
                      {esp.familia}
                    </span>
                  </div>
                );
              })
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
