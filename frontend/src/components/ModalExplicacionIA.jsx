import React, { useEffect } from 'react';
import ReactDOM from 'react-dom';
import { X, Brain, Cpu, ShieldCheck, CheckCircle2, Award, Info, Layers, Tag } from 'lucide-react';

export default function ModalExplicacionIA({ candidato, desgloseGeneral, respuestasDeducidas, apiBase, onClose }) {
  if (!candidato) return null;

  const especieId = candidato.especie_id || candidato.especie?.toLowerCase().replace(/ /g, '_');
  const imageUrl = `${apiBase}/imagenes/${especieId}.jpg`;

  // Cerrar al presionar la tecla Escape
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  // Prevenir scroll en body mientras el modal está abierto
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, []);

  const scorePorcentaje = (candidato.score_final * 100).toFixed(1);

  const modalContent = (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        zIndex: 99999,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '20px',
        background: 'rgba(11, 15, 23, 0.86)',
        backdropFilter: 'blur(16px)',
        WebkitBackdropFilter: 'blur(16px)'
      }}
      onClick={onClose}
    >
      {/* Contenedor del Modal Horizontal en 2 Columnas */}
      <div
        className="liquid-glass animate-scale-in"
        style={{
          width: '100%',
          maxWidth: '780px',
          maxHeight: '85vh',
          overflow: 'hidden',
          borderRadius: 'var(--radius-xl)',
          border: '1px solid rgba(167, 139, 250, 0.35)',
          boxShadow: '0 24px 64px rgba(0, 0, 0, 0.75)',
          position: 'relative',
          background: 'rgba(22, 27, 34, 0.96)',
          display: 'grid',
          gridTemplateColumns: '310px 1fr'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Botón Cerrar */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '14px',
            right: '14px',
            zIndex: 10,
            width: '32px',
            height: '32px',
            borderRadius: '50%',
            background: 'rgba(13, 17, 23, 0.8)',
            border: '1px solid var(--liquid-border)',
            color: 'var(--text-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            backdropFilter: 'blur(8px)'
          }}
          onMouseOver={(e) => { e.currentTarget.style.borderColor = 'var(--accent-coral)'; e.currentTarget.style.color = 'var(--accent-coral)'; }}
          onMouseOut={(e) => { e.currentTarget.style.borderColor = 'var(--liquid-border)'; e.currentTarget.style.color = 'var(--text-primary)'; }}
        >
          <X size={18} />
        </button>

        {/* ── COLUMNA IZQUIERDA: Fotografía & Identificación de la Especie ── */}
        <div style={{ position: 'relative', height: '100%', minHeight: '360px', background: 'rgba(0,0,0,0.4)', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          <img
            src={imageUrl}
            alt={candidato.especie}
            style={{ width: '100%', height: '100%', objectFit: 'cover', position: 'absolute', inset: 0 }}
            onError={(e) => {
              e.target.onerror = null;
              e.target.style.display = 'none';
            }}
          />
          {/* Degradado inferior */}
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(22, 27, 34, 0.95) 0%, transparent 60%)' }} />

          {/* Badges Flotantes sobre la Imagen */}
          <div style={{ position: 'absolute', bottom: '16px', left: '16px', right: '16px', display: 'flex', gap: '6px', flexWrap: 'wrap', zIndex: 3 }}>
            <span className="badge badge-purple" style={{ fontSize: '0.72rem', backdropFilter: 'blur(8px)', background: 'rgba(13, 17, 23, 0.85)', padding: '5px 12px', border: '1px solid rgba(167, 139, 250, 0.4)' }}>
              ⚡ Coincidencia IA: {scorePorcentaje}%
            </span>
            <span className="badge badge-cyan" style={{ fontSize: '0.68rem', backdropFilter: 'blur(8px)', background: 'rgba(13, 17, 23, 0.8)', padding: '4px 10px' }}>
              Familia: {candidato.familia}
            </span>
          </div>
        </div>

        {/* ── COLUMNA DERECHA: EXPLICACIÓN DEL RANKING Y JUSTIFICACIÓN IA (XAI) ── */}
        <div style={{ padding: '24px 28px 24px 20px', display: 'flex', flexDirection: 'column', gap: '16px', overflowY: 'auto', maxHeight: '85vh' }}>
          
          {/* Encabezado Nombres */}
          <div style={{ paddingRight: '28px' }}>
            <span className="badge badge-cyan" style={{ fontSize: '0.68rem', marginBottom: '4px' }}>
              Justificación Algorítmica (XAI)
            </span>
            <h2 style={{ fontSize: '1.45rem', fontWeight: 800, fontStyle: 'italic', color: 'var(--text-primary)', lineHeight: 1.25 }}>
              {candidato.especie}
            </h2>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--accent-primary)', marginTop: '3px' }}>
              "{candidato.nombre_comun}"
            </h3>
          </div>

          {/* Bloque Desglose de Puntuación (Score Breakdown) */}
          <div className="liquid-glass" style={{ padding: '14px 16px', background: 'rgba(0, 0, 0, 0.18)', border: '1px solid rgba(167, 139, 250, 0.25)' }}>
            <span style={{ fontSize: '0.72rem', color: 'var(--accent-purple)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '10px' }}>
              <Layers size={14} /> Desglose del Ranking Híbrido
            </span>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
              <div className="liquid-glass" style={{ padding: '10px 12px' }}>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <Cpu size={13} color="var(--accent-primary)" /> Similitud Ponderada
                </div>
                <div style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--accent-primary)', marginTop: '2px' }}>
                  {candidato.similitud_ponderada || scorePorcentaje}%
                </div>
              </div>

              <div className="liquid-glass" style={{ padding: '10px 12px' }}>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-tertiary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <Brain size={13} color="var(--accent-coral)" /> Árbol Dicotómico
                </div>
                <div style={{ fontSize: '1.15rem', fontWeight: 800, color: 'var(--accent-coral)', marginTop: '2px' }}>
                  {candidato.coincidencia_arbol || scorePorcentaje}%
                </div>
              </div>
            </div>
          </div>

          {/* Coincidencias Clave Deducidas por la Red Neuronal */}
          {candidato.coincidencias_clave && candidato.coincidencias_clave.length > 0 && (
            <div>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '8px' }}>
                <CheckCircle2 size={14} color="var(--accent-primary)" /> Coincidencias Taxonómicas Encontradas
              </span>

              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {candidato.coincidencias_clave.map((match, idx) => (
                  <span key={idx} className="badge badge-cyan" style={{ fontSize: '0.75rem', padding: '4px 10px' }}>
                    ✓ {match}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Características Deducidas del Texto del Usuario */}
          {respuestasDeducidas && Object.keys(respuestasDeducidas).length > 0 && (
            <div>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '8px' }}>
                <Tag size={13} color="var(--accent-purple)" /> Atributos Extraídos por NLP / TensorFlow
              </span>

              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {Object.entries(respuestasDeducidas).map(([k, v], idx) => (
                  <div
                    key={idx}
                    className="liquid-glass"
                    style={{
                      padding: '4px 10px',
                      borderRadius: 'var(--radius-pill)',
                      background: 'rgba(167, 139, 250, 0.08)',
                      border: '1px solid rgba(167, 139, 250, 0.25)',
                      fontSize: '0.75rem',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '4px'
                    }}
                  >
                    <span style={{ color: 'var(--text-tertiary)', fontWeight: 600 }}>{k}:</span>
                    <span style={{ color: 'var(--accent-purple)', fontWeight: 700 }}>{String(v)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Razonamiento Explicativo Híbrido */}
          <div className="liquid-glass" style={{ padding: '12px 14px', borderLeft: '3px solid var(--accent-primary)', background: 'rgba(255, 255, 255, 0.02)' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-primary)', fontWeight: 700, fontSize: '0.82rem', marginBottom: '4px' }}>
              <ShieldCheck size={15} /> ¿Por qué ocupa esta posición en el ranking?
            </div>
            <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', lineHeight: 1.5, position: 'relative', zIndex: 2 }}>
              Esta especie alcanzó un puntaje de similitud del <strong>{scorePorcentaje}%</strong> debido a la alta correlación entre la morfología descrita en tu observación (forma de la colonia, color y patrón de superficie) y las reglas dicotómicas registradas para la familia <strong>{candidato.familia}</strong> en Los Roques.
            </p>
          </div>

        </div>
      </div>
    </div>
  );

  return ReactDOM.createPortal(modalContent, document.body);
}
