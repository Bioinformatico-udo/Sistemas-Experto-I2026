import React, { useEffect } from 'react';
import ReactDOM from 'react-dom';
import { X, MapPin, Info, ImageOff, Tag } from 'lucide-react';

export default function ModalDetalleCoral({ esp, apiBase, onClose }) {
  if (!esp) return null;

  const imageUrl = `${apiBase}/imagenes/${esp.id}.jpg`;

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
        background: 'rgba(11, 15, 23, 0.85)',
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
          border: '1px solid rgba(62, 207, 180, 0.3)',
          boxShadow: '0 24px 64px rgba(0, 0, 0, 0.7)',
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

        {/* ── COLUMNA IZQUIERDA: Fotografía del Coral & Badges ── */}
        <div style={{ position: 'relative', height: '100%', minHeight: '360px', background: 'rgba(0,0,0,0.4)', overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
          <img
            src={imageUrl}
            alt={esp.nombre_cientifico}
            style={{ width: '100%', height: '100%', objectFit: 'cover', position: 'absolute', inset: 0 }}
            onError={(e) => {
              e.target.onerror = null;
              e.target.style.display = 'none';
              if (e.target.nextSibling) {
                e.target.nextSibling.style.display = 'flex';
              }
            }}
          />
          {/* Fallback si la imagen no carga */}
          <div style={{ display: 'none', width: '100%', height: '100%', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, rgba(62,207,180,0.2), rgba(91,156,246,0.2))', flexDirection: 'column', gap: '8px', color: 'var(--text-tertiary)' }}>
            <ImageOff size={36} color="var(--accent-primary)" />
            <span style={{ fontSize: '0.8rem' }}>{esp.nombre_cientifico}</span>
          </div>

          {/* Degradado inferior */}
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(to top, rgba(22, 27, 34, 0.95) 0%, transparent 60%)' }} />

          {/* Badges Flotantes sobre la Imagen */}
          <div style={{ position: 'absolute', bottom: '16px', left: '16px', right: '16px', display: 'flex', gap: '6px', flexWrap: 'wrap', zIndex: 3 }}>
            <span className="badge badge-cyan" style={{ fontSize: '0.68rem', backdropFilter: 'blur(8px)', background: 'rgba(13, 17, 23, 0.8)', padding: '4px 10px' }}>
              Familia: {esp.familia}
            </span>
            {esp.orden && (
              <span className="badge badge-blue" style={{ fontSize: '0.68rem', backdropFilter: 'blur(8px)', background: 'rgba(13, 17, 23, 0.8)', padding: '4px 10px' }}>
                Orden: {esp.orden}
              </span>
            )}
            {esp.tipo && (
              <span className="badge badge-amber" style={{ fontSize: '0.68rem', backdropFilter: 'blur(8px)', background: 'rgba(13, 17, 23, 0.8)', padding: '4px 10px' }}>
                {esp.tipo}
              </span>
            )}
          </div>
        </div>

        {/* ── COLUMNA DERECHA: Información Detallada y Características ── */}
        <div style={{ padding: '24px 28px 24px 20px', display: 'flex', flexDirection: 'column', gap: '14px', overflowY: 'auto', maxHeight: '85vh' }}>
          {/* Títulos Nombres */}
          <div style={{ paddingRight: '28px' }}>
            <h2 style={{ fontSize: '1.45rem', fontWeight: 800, fontStyle: 'italic', color: 'var(--text-primary)', lineHeight: 1.25 }}>
              {esp.nombre_cientifico}
            </h2>
            <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--accent-primary)', marginTop: '3px' }}>
              "{esp.nombre_comun}"
            </h3>
          </div>

          {/* Sección Hábitat */}
          {esp.habitat && (
            <div className="liquid-glass" style={{ padding: '10px 14px', display: 'flex', alignItems: 'flex-start', gap: '10px', background: 'rgba(255, 255, 255, 0.02)' }}>
              <MapPin size={16} color="var(--accent-primary)" style={{ flexShrink: 0, marginTop: '2px' }} />
              <div>
                <span style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', fontWeight: 700 }}>
                  Hábitat Registrado
                </span>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '1px', lineHeight: 1.4, position: 'relative', zIndex: 2 }}>
                  {esp.habitat}
                </p>
              </div>
            </div>
          )}

          {/* Sección Descripción */}
          {esp.descripcion && (
            <div>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '4px' }}>
                <Info size={13} color="var(--accent-primary)" /> Descripción Taxonómica
              </span>
              <p style={{ fontSize: '0.86rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                {esp.descripcion}
              </p>
            </div>
          )}

          {/* Fila de Botones Visuales con Características */}
          {esp.caracteristicas && Object.keys(esp.caracteristicas).length > 0 && (
            <div>
              <span style={{ fontSize: '0.68rem', color: 'var(--text-tertiary)', textTransform: 'uppercase', letterSpacing: '0.5px', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '4px', marginBottom: '8px' }}>
                <Tag size={13} color="var(--accent-primary)" /> Características Diagnósticas
              </span>

              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {Object.entries(esp.caracteristicas).map(([k, v], idx) => {
                  let formattedValue = String(v);
                  if (typeof v === 'boolean') {
                    formattedValue = v ? 'Sí' : 'No';
                  }

                  return (
                    <div
                      key={idx}
                      className="liquid-glass"
                      style={{
                        padding: '5px 10px',
                        borderRadius: 'var(--radius-pill)',
                        background: 'rgba(62, 207, 180, 0.06)',
                        border: '1px solid rgba(62, 207, 180, 0.2)',
                        fontSize: '0.75rem',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px',
                        color: 'var(--text-primary)',
                        cursor: 'default'
                      }}
                    >
                      <span style={{ color: 'var(--text-tertiary)', fontWeight: 600, textTransform: 'capitalize' }}>
                        {k.replace(/_/g, ' ')}:
                      </span>
                      <span style={{ color: 'var(--accent-primary)', fontWeight: 700 }}>
                        {formattedValue}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  return ReactDOM.createPortal(modalContent, document.body);
}
