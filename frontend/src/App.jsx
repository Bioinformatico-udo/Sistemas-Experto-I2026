import React, { useState, useEffect } from 'react';
import LoginScreen from './components/LoginScreen';
import Cuestionario from './components/Cuestionario';
import DiagnosticoIA from './components/DiagnosticoIA';
import CatalogoEspecies from './components/CatalogoEspecies';
import GuiaTaxonomica from './components/GuiaTaxonomica';
import logoImg from './assets/logo.png';
import {
  Waves, Sparkles, ClipboardList, MessageSquareText,
  BookOpen, Compass, MapPin, Users, Shell,
  Brain, GitFork, Cpu, Scale, ArrowRight, ChevronRight, LogOut
} from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

/* ─── Página de Inicio ─── */
function PantallaInicio({ onNavigate }) {
  const [especiesCount, setEspeciesCount] = useState(41);
  const [preguntasCount, setPreguntasCount] = useState(60);

  useEffect(() => {
    fetch(`${API_BASE}/especies`)
      .then(r => r.json())
      .then(data => {
        if (Array.isArray(data) && data.length > 0) setEspeciesCount(data.length);
      })
      .catch(() => { });

    fetch(`${API_BASE}/preguntas`)
      .then(r => r.json())
      .then(data => {
        if (Array.isArray(data) && data.length > 0) setPreguntasCount(data.length);
      })
      .catch(() => { });
  }, []);

  const familiasCount = 15;

  return (
    <div className="animate-fade-in">
      {/* ── HERO ── */}
      <section style={{ padding: '60px 0 40px', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px', alignItems: 'center' }}>
        {/* Left: Bienvenida */}
        <div>
          <h2 style={{ fontSize: '2.8rem', fontWeight: 800, lineHeight: 1.15, marginBottom: '16px', letterSpacing: '-1px' }}>
            Bienvenido experto
          </h2>
          <p style={{ fontSize: '1.1rem', color: 'var(--text-secondary)', lineHeight: 1.7, maxWidth: '460px', marginBottom: '28px' }}>
            Tu asistente inteligente para el análisis, diagnóstico y registro de especies del orden Scleractinia,
            halladas en el Parque Nacional Los Roques, Venezuela.
          </p>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: 'rgba(62,207,180,0.12)', border: '1px solid rgba(62,207,180,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Shell size={18} color="var(--accent-primary)" />
            </div>
            <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: 'rgba(91,156,246,0.12)', border: '1px solid rgba(91,156,246,0.2)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Waves size={18} color="var(--accent-blue)" />
            </div>
          </div>
        </div>

        {/* Right: CTA Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
          {/* Card 1: Cuestionario Dicotómico */}
          <div
            className="liquid-glass liquid-glass-interactive"
            onClick={() => onNavigate('cuestionario')}
            style={{
              padding: '32px 24px',
              textAlign: 'center',
              position: 'relative',
              overflow: 'hidden',
              background: 'linear-gradient(135deg, rgba(53, 150, 147, 0.5) 0%, rgba(22, 27, 34, 0.85) 100%)',
              backdropFilter: 'blur(20px)',
              WebkitBackdropFilter: 'blur(20px)',
              border: '1px solid rgba(62, 207, 180, 0.35)',
              boxShadow: '0 20px 48px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.25)',
              borderRadius: 'var(--radius-xl)'
            }}
          >
            {/* Ambient Glowing Orbs */}
            <div style={{ position: 'absolute', top: '-40px', right: '-40px', width: '160px', height: '160px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(62, 207, 180, 0.45) 0%, transparent 70%)', filter: 'blur(15px)', pointerEvents: 'none', zIndex: 1 }} />
            <div style={{ position: 'absolute', bottom: '-40px', left: '-40px', width: '120px', height: '120px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(53, 150, 147, 0.35) 0%, transparent 70%)', filter: 'blur(15px)', pointerEvents: 'none', zIndex: 1 }} />

            {/* Content */}
            <div style={{ position: 'relative', zIndex: 2 }}>
              <div style={{ width: '56px', height: '56px', borderRadius: '18px', background: 'rgba(13, 17, 23, 0.65)', border: '1px solid rgba(62, 207, 180, 0.4)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 18px', backdropFilter: 'blur(10px)', boxShadow: '0 8px 20px rgba(0,0,0,0.3)' }}>
                <ClipboardList size={26} color="var(--accent-primary)" />
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '8px' }}>
                Clave Taxonómica
              </h3>
              <p style={{ fontSize: '0.88rem', color: 'rgba(230, 237, 243, 0.85)', lineHeight: 1.55, marginBottom: '22px' }}>
                Secuencia de preguntas dicotómicas guiadas para determinar la especie exacta.
              </p>
              <button className="btn-outline" style={{ width: '100%', justifyContent: 'center', background: 'rgba(62, 207, 180, 0.12)', borderColor: 'rgba(62, 207, 180, 0.5)', color: '#ffffff' }}>
                Empieza ya <ArrowRight size={16} />
              </button>
            </div>
          </div>

          {/* Card 2: Asistente IA */}
          <div
            className="liquid-glass liquid-glass-interactive"
            onClick={() => onNavigate('ia')}
            style={{
              padding: '32px 24px',
              textAlign: 'center',
              position: 'relative',
              overflow: 'hidden',
              background: 'linear-gradient(135deg, rgba(93, 53, 150, 0.5) 0%, rgba(22, 27, 34, 0.85) 100%)',
              backdropFilter: 'blur(20px)',
              WebkitBackdropFilter: 'blur(20px)',
              border: '1px solid rgba(167, 139, 250, 0.35)',
              boxShadow: '0 20px 48px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.25)',
              borderRadius: 'var(--radius-xl)'
            }}
          >
            {/* Ambient Glowing Orbs */}
            <div style={{ position: 'absolute', top: '-40px', right: '-40px', width: '160px', height: '160px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(167, 139, 250, 0.45) 0%, transparent 70%)', filter: 'blur(15px)', pointerEvents: 'none', zIndex: 1 }} />
            <div style={{ position: 'absolute', bottom: '-40px', left: '-40px', width: '120px', height: '120px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(255, 107, 157, 0.3) 0%, transparent 70%)', filter: 'blur(15px)', pointerEvents: 'none', zIndex: 1 }} />

            {/* Content */}
            <div style={{ position: 'relative', zIndex: 2 }}>
              <div style={{ width: '56px', height: '56px', borderRadius: '18px', background: 'rgba(13, 17, 23, 0.65)', border: '1px solid rgba(167, 139, 250, 0.4)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 18px', backdropFilter: 'blur(10px)', boxShadow: '0 8px 20px rgba(0,0,0,0.3)' }}>
                <MessageSquareText size={26} color="var(--accent-purple)" />
              </div>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '8px' }}>
                Asistente IA
              </h3>
              <p style={{ fontSize: '0.88rem', color: 'rgba(230, 237, 243, 0.85)', lineHeight: 1.55, marginBottom: '22px' }}>
                Describe las características del coral en tus propias palabras para el modelo de IA.
              </p>
              <button className="btn-outline" style={{ width: '100%', justifyContent: 'center', background: 'rgba(167, 139, 250, 0.12)', borderColor: 'rgba(167, 139, 250, 0.5)', color: '#ffffff' }}>
                Empieza ya <ArrowRight size={16} />
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* ── STATS BAND ── */}
      <section className="section-band">
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 24px', display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '40px', alignItems: 'center' }}>
          {/* Coral stats */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
            <div style={{ width: '76px', height: '76px', borderRadius: '18px', background: 'rgba(0, 0, 0, 0.2)', border: '1px solid rgba(255, 255, 255, 0.25)', backdropFilter: 'blur(10px)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Shell size={38} color="#ffffff" strokeWidth={1.5} />
            </div>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '4px' }}>
              <li style={{ fontSize: '0.95rem', color: '#ffffff', fontWeight: 600 }}>
                • <span style={{ color: '#ffffff', fontWeight: 900, fontSize: '1.05rem' }}>{especiesCount || '40'}</span> especies
              </li>
              <li style={{ fontSize: '0.95rem', color: '#ffffff', fontWeight: 600 }}>
                • <span style={{ color: '#ffffff', fontWeight: 900, fontSize: '1.05rem' }}>{familiasCount}</span> Familias
              </li>
              <li style={{ fontSize: '0.95rem', color: '#ffffff', fontWeight: 600 }}>
                • <span style={{ color: '#ffffff', fontWeight: 900, fontSize: '1.05rem' }}>{preguntasCount}</span> preguntas
              </li>
            </ul>
          </div>

          {/* Description Card */}
          <div className="liquid-glass" style={{ padding: '24px 28px', display: 'flex', alignItems: 'center', gap: '24px', background: 'rgba(0, 0, 0, 0.22)', border: '1px solid rgba(255, 255, 255, 0.25)' }}>
            <div className="icon-circle icon-circle-blue" style={{ flexShrink: 0, background: 'rgba(255, 255, 255, 0.15)', color: '#ffffff' }}>
              <BookOpen size={24} color="#ffffff" />
            </div>
            <div style={{ flex: 1 }}>
              <p style={{ fontSize: '0.9rem', color: '#ffffff', lineHeight: 1.6, position: 'relative', zIndex: 2 }}>
                Accede a una base de conocimientos actualizada con fichas detalladas de cada coral registrado.
                ¿Encontraste una especie no documentada? Contribuye registrando nuevos hallazgos para expandir
                la base de datos del sistema.
              </p>
            </div>
            <button className="btn-outline" onClick={() => onNavigate('catalogo')} style={{ flexShrink: 0, position: 'relative', zIndex: 2, color: '#ffffff', borderColor: 'rgba(255, 255, 255, 0.5)' }}>
              Revisar catálogo <ChevronRight size={16} />
            </button>
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section style={{ padding: '60px 0 40px' }}>
        <h3 style={{ textAlign: 'center', fontSize: '2rem', fontWeight: 800, marginBottom: '8px', letterSpacing: '-0.5px' }}>
          ¿Cómo funciona Cora<span className="gradient-text">AI</span>?
        </h3>
        <p style={{ textAlign: 'center', color: 'var(--text-secondary)', marginBottom: '40px', fontSize: '1rem' }}>
          Cuatro pilares coexistentes que combinan IA simbólica y subsimbólica
        </p>

        <div className="stagger-children" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '20px' }}>
          {[
            {
              icon: <Brain size={28} />,
              iconClass: 'icon-circle-coral',
              title: 'Red Neuronal',
              desc: 'La red no predice la especie directamente, sino que predice las características taxonómicas que se deducen a partir de la descripción textual libre escrita por el usuario.'
            },
            {
              icon: <GitFork size={28} />,
              iconClass: 'icon-circle-teal',
              title: 'Árbol de Decisiones Taxonómicas',
              desc: 'Es el mapa formal del conocimiento científico botánico/zoológico. Representa la clave dicotómica estructurada que conduce a especies clasificadas.'
            },
            {
              icon: <Cpu size={28} />,
              iconClass: 'icon-circle-blue',
              title: 'Motor de Inferencia',
              desc: 'Ejecutar el razonamiento lógico formal sobre el árbol de decisiones. Recibe características estructuradas y recorre el árbol.'
            },
            {
              icon: <Scale size={28} />,
              iconClass: 'icon-circle-amber',
              title: 'Motor de Ponderación Inteligente',
              desc: 'Evaluar la similitud textual y semántica directa. Analiza la descripción libre en busca de términos específicos usando normalización y sinónimos biológicos/coloquiales.'
            }
          ].map((item, idx) => (
            <div key={idx} className="liquid-glass liquid-glass-interactive animate-fade-in" style={{ padding: '28px 24px', textAlign: 'center', opacity: 0 }}>
              <div className={`icon-circle ${item.iconClass}`} style={{ margin: '0 auto 16px' }}>
                {item.icon}
              </div>
              <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '12px', color: 'var(--text-primary)' }}>
                {item.title}
              </h4>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

/* ─── App Principal ─── */
export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [tabActiva, setTabActiva] = useState('inicio');

  // Si no está logueado, mostrar la pantalla de Login
  if (!isLoggedIn) {
    return <LoginScreen onLoginSuccess={() => setIsLoggedIn(true)} />;
  }

  const navItems = [
    { id: 'inicio', label: 'Inicio' },
    { id: 'cuestionario', label: 'Cuestionario' },
    { id: 'ia', label: 'Asistente IA' },
    { id: 'catalogo', label: 'Catálogo' },
  ];

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* ── HEADER ── */}
      <header style={{
        position: 'sticky',
        top: 0,
        zIndex: 100,
        background: 'rgba(0, 0, 0, 0.7)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)',
        borderBottom: 'none'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          padding: '6px 24px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: '24px'
        }}>
          {/* Logo */}
          <div
            style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}
            onClick={() => setTabActiva('inicio')}
          >
            <img
              src={logoImg}
              alt="CoraAI Logo"
              style={{
                height: '80px',
                width: 'auto',
                maxWidth: '320px',
                objectFit: 'contain',
                transition: 'transform 0.2s ease'
              }}
            />
          </div>

          {/* Navigation */}
          <nav style={{
            display: 'flex',
            gap: '4px',
            background: '#3d3d3d',
            padding: '4px',
            borderRadius: 'var(--radius-pill)',
            border: '1px solid var(--liquid-border)'
          }}>
            {navItems.map(item => (
              <button
                key={item.id}
                className={`nav-tab ${tabActiva === item.id ? 'active' : ''}`}
                onClick={() => setTabActiva(item.id)}
              >
                {item.label}
              </button>
            ))}
          </nav>

          {/* Cerrar Sesión */}
          <button
            onClick={() => { setIsLoggedIn(false); setTabActiva('inicio'); }}
            className="btn-outline"
            style={{
              padding: '8px 16px',
              fontSize: '0.82rem',
              gap: '6px',
              color: 'var(--text-secondary)',
              borderColor: 'rgba(255, 107, 157, 0.25)'
            }}
          >
            <LogOut size={14} /> Cerrar Sesión
          </button>
        </div>
      </header>

      {/* ── MAIN ── */}
      <main style={{ flex: 1, maxWidth: '1200px', width: '100%', margin: '0 auto', padding: '32px 24px' }}>
        {tabActiva === 'inicio' && <PantallaInicio onNavigate={setTabActiva} />}
        {tabActiva === 'cuestionario' && <Cuestionario apiBase={API_BASE} />}
        {tabActiva === 'ia' && <DiagnosticoIA apiBase={API_BASE} />}
        {tabActiva === 'catalogo' && <CatalogoEspecies apiBase={API_BASE} />}
        {tabActiva === 'guia' && <GuiaTaxonomica apiBase={API_BASE} />}
      </main>

      {/* ── FOOTER ── */}
      <footer style={{
        background: 'rgba(34, 34, 34, 0.95)',
        borderTop: '1px solid var(--liquid-border)',
        padding: '24px',
        width: '100%'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '12px',
          color: 'var(--text-secondary)',
          fontSize: '0.875rem'
        }}>
          <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '36px', flexWrap: 'wrap' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <MapPin size={15} color="var(--accent-primary)" />
              Parque Nacional Archipiélago de Los Roques, Venezuela
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Shell size={15} color="var(--accent-primary)" />
              41 Especies Registradas
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Users size={15} color="var(--accent-primary)" />
              Grupo 8 — Sistemas Expertos I-2026
            </div>
          </div>

          <div style={{ fontSize: '0.8rem', color: 'var(--text-tertiary)', textAlign: 'center' }}>
            CoraAI — Sistema Experto Híbrido Coexistente (IA Simbólica + TensorFlow Deep Learning + Motor de Ponderación)
          </div>
        </div>
      </footer>
    </div>
  );
}
