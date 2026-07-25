import React, { useState, useEffect } from 'react';
import { Compass } from 'lucide-react';

export default function GuiaTaxonomica({ apiBase }) {
  const [guia, setGuia] = useState(null);

  useEffect(() => {
    async function cargar() {
      try {
        const res = await fetch(`${apiBase}/guia`);
        const data = await res.json();
        setGuia(data);
      } catch (err) {
        console.error('Error al cargar la guía:', err);
      }
    }
    cargar();
  }, [apiBase]);

  return (
    <div className="animate-fade-in" style={{ maxWidth: '900px', margin: '0 auto' }}>
      {/* Header */}
      <div className="liquid-glass" style={{ padding: '28px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '8px' }}>
          <div className="icon-circle icon-circle-teal">
            <Compass size={24} />
          </div>
          <div>
            <span className="badge badge-cyan">Clave Taxonómica del Atlántico</span>
            <h2 style={{ fontSize: '1.6rem', fontWeight: 700, marginTop: '4px' }}>
              Guía didáctica de identificación
            </h2>
          </div>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', lineHeight: 1.6, marginTop: '12px' }}>
          Aprende a reconocer las microestructuras clave y patrones morfométricos para clasificar corales duros del Archipiélago de Los Roques.
        </p>
      </div>

      {guia && guia.pasos_fundamentales && (
        <div className="stagger-children" style={{ display: 'grid', gap: '16px' }}>
          {guia.pasos_fundamentales.map((item) => (
            <div
              key={item.paso}
              className="liquid-glass liquid-glass-accent animate-fade-in"
              style={{
                padding: '24px 28px',
                display: 'grid',
                gridTemplateColumns: 'auto 1fr',
                gap: '20px',
                alignItems: 'flex-start',
                opacity: 0
              }}
            >
              <div style={{
                background: 'linear-gradient(135deg, var(--accent-secondary), var(--accent-primary))',
                color: 'var(--text-on-accent)',
                width: '48px',
                height: '48px',
                borderRadius: '14px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 800,
                fontSize: '1.2rem',
                flexShrink: 0,
                boxShadow: '0 4px 16px rgba(62, 207, 180, 0.2)',
                position: 'relative',
                zIndex: 2
              }}>
                {item.paso}
              </div>

              <div style={{ position: 'relative', zIndex: 2 }}>
                <h3 style={{ fontSize: '1.15rem', fontWeight: 700, marginBottom: '8px' }}>
                  {item.concepto}
                </h3>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.65 }}>
                  {item.detalle}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
