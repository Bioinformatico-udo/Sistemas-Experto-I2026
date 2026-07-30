import React, { useState } from 'react';
import { Shield, LogIn, AlertCircle, Waves, Shell, Brain, ClipboardList, Sparkles } from 'lucide-react';
import logoImg from '../assets/logo.png';

// ─── Credenciales de acceso (mock) ───
const MOCK_USER = 'admin';
const MOCK_PASS = 'admin123';

export default function LoginScreen({ onLoginSuccess }) {
  const [usuario, setUsuario] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [error, setError] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [loginExitoso, setLoginExitoso] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setError(null);

    if (!usuario.trim() || !contrasena.trim()) {
      setError('Por favor completa todos los campos.');
      return;
    }

    if (usuario !== MOCK_USER || contrasena !== MOCK_PASS) {
      setError('Credenciales incorrectas. Verifica tu usuario y contraseña.');
      return;
    }

    setCargando(true);

    // Simular breve delay de autenticación
    setTimeout(() => {
      setCargando(false);
      setLoginExitoso(true);

      // Esperar la animación de salida antes de navegar
      setTimeout(() => {
        onLoginSuccess();
      }, 600);
    }, 800);
  };

  return (
    <div className={`login-screen ${loginExitoso ? 'login-fade-out' : ''}`}>

      {/* ── PANEL IZQUIERDO: BRANDING ── */}
      <div className="login-brand-panel">
        {/* Orbes ambientales */}
        <div className="login-orb login-orb-1" />
        <div className="login-orb login-orb-2" />
        <div className="login-orb login-orb-3" />

        <div className="login-brand-content">
          <img
            src={logoImg}
            alt="CoraAI Logo"
            style={{
              height: '100px',
              width: 'auto',
              maxWidth: '360px',
              objectFit: 'contain',
              marginBottom: '24px',
              filter: 'drop-shadow(0 8px 32px rgba(62, 207, 180, 0.3))'
            }}
          />

          <h1 style={{ fontSize: '2.2rem', fontWeight: 800, lineHeight: 1.15, letterSpacing: '-1px', marginBottom: '12px' }}>
            <span className="gradient-text">Sistema Experto</span>
            <br />
            <span style={{ color: 'var(--text-primary)' }}>Taxonómico de Corales</span>
          </h1>

          <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: 1.7, maxWidth: '380px', marginBottom: '32px' }}>
            Plataforma de identificación, clasificación y análisis pedagógico-científico de corales del Parque Nacional Los Roques, Venezuela.
          </p>

          {/* Feature badges */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '36px' }}>
            {[
              { icon: <ClipboardList size={16} />, text: 'Clave Taxonómica Dicotómica', color: 'var(--accent-primary)' },
              { icon: <Brain size={16} />, text: 'Diagnóstico IA en Lenguaje Natural', color: 'var(--accent-purple)' },
              { icon: <Shell size={16} />, text: '41+ Especies de Los Roques', color: 'var(--accent-coral)' },
            ].map((feat, idx) => (
              <div key={idx} style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <div style={{
                  width: '32px', height: '32px', borderRadius: '10px',
                  background: `${feat.color}15`, border: `1px solid ${feat.color}30`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  color: feat.color, flexShrink: 0
                }}>
                  {feat.icon}
                </div>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
                  {feat.text}
                </span>
              </div>
            ))}
          </div>

          {/* Créditos */}
          <div style={{ fontSize: '0.78rem', color: 'var(--text-tertiary)', lineHeight: 1.6 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
              <Waves size={13} color="var(--accent-primary)" />
              Grupo 8 — Sistemas Expertos I-2026
            </div>
            <div>Universidad de Oriente</div>
          </div>
        </div>
      </div>

      {/* ── PANEL DERECHO: FORMULARIO ── */}
      <div className="login-form-panel">
        {/* Burbujas decorativas */}
        <div className="ocean-bubble" style={{ width: '14px', height: '14px', bottom: '15%', left: '12%', animationDelay: '0s' }} />
        <div className="ocean-bubble" style={{ width: '10px', height: '10px', bottom: '25%', right: '18%', animationDelay: '1.5s' }} />
        <div className="ocean-bubble" style={{ width: '8px', height: '8px', bottom: '10%', left: '60%', animationDelay: '3s' }} />
        <div className="ocean-bubble" style={{ width: '12px', height: '12px', bottom: '30%', right: '8%', animationDelay: '4.5s' }} />

        <div className="login-form-wrapper animate-fade-in">
          <div className="liquid-glass" style={{ padding: '40px 36px', maxWidth: '420px', width: '100%', position: 'relative', overflow: 'visible' }}>

            {/* Header del formulario */}
            <div style={{ textAlign: 'center', marginBottom: '32px' }}>
              <div className="icon-circle icon-circle-teal" style={{ width: '64px', height: '64px', margin: '0 auto 16px', borderRadius: '20px' }}>
                <Shield size={30} />
              </div>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 800, letterSpacing: '-0.5px', marginBottom: '6px' }}>
                Iniciar Sesión
              </h2>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)' }}>
                Accede al panel de análisis taxonómico
              </p>
            </div>

            {/* Formulario */}
            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Usuario
                </label>
                <input
                  type="text"
                  className="input-glass"
                  placeholder="Ingresa tu usuario"
                  value={usuario}
                  onChange={(e) => { setUsuario(e.target.value); setError(null); }}
                  autoComplete="username"
                  style={{ fontSize: '0.95rem' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Contraseña
                </label>
                <input
                  type="password"
                  className="input-glass"
                  placeholder="Ingresa tu contraseña"
                  value={contrasena}
                  onChange={(e) => { setContrasena(e.target.value); setError(null); }}
                  autoComplete="current-password"
                  style={{ fontSize: '0.95rem' }}
                />
              </div>

              {/* Mensaje de error */}
              {error && (
                <div style={{
                  display: 'flex', alignItems: 'center', gap: '8px',
                  padding: '10px 14px', borderRadius: 'var(--radius-sm)',
                  background: 'rgba(255, 107, 157, 0.08)',
                  border: '1px solid rgba(255, 107, 157, 0.2)',
                  color: 'var(--accent-coral)', fontSize: '0.84rem', fontWeight: 500
                }}>
                  <AlertCircle size={16} style={{ flexShrink: 0 }} />
                  {error}
                </div>
              )}

              {/* Botón de login */}
              <button
                type="submit"
                className="btn-primary"
                disabled={cargando}
                style={{
                  width: '100%', justifyContent: 'center',
                  padding: '14px 28px', fontSize: '1rem',
                  marginTop: '6px'
                }}
              >
                {cargando ? (
                  <>
                    <Sparkles size={18} className="pulse-glow" /> Verificando...
                  </>
                ) : (
                  <>
                    <LogIn size={18} /> Iniciar Sesión
                  </>
                )}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
