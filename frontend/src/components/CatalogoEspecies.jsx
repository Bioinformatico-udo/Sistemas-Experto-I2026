import React, { useState, useEffect, useRef } from 'react';
import { Search, BookOpen, ImageOff, ChevronDown, Plus } from 'lucide-react';
import ModalDetalleCoral from './ModalDetalleCoral';
import ModalAgregarEspecie from './ModalAgregarEspecie';

/* ─── Tarjeta Compacta de Coral con Carga Procedural y Click Event ─── */
function CoralCard({ esp, apiBase, onSelect }) {
  const [imageStatus, setImageStatus] = useState('loading'); // 'loading' | 'loaded' | 'error'
  const imageUrl = `${apiBase}/imagenes/${esp.id}.jpg`;

  return (
    <div
      onClick={() => onSelect(esp)}
      className="liquid-glass liquid-glass-interactive animate-fade-in"
      style={{
        padding: 0,
        display: 'flex',
        flexDirection: 'column',
        borderRadius: 'var(--radius-lg)',
        overflow: 'hidden',
        cursor: 'pointer'
      }}
    >
      {/* Contenedor de Imagen con Esqueleto Procedural */}
      <div style={{ position: 'relative', height: '170px', width: '100%', background: 'rgba(0,0,0,0.3)', overflow: 'hidden' }}>
        {/* Esqueleto Shimmer mientras se descarga la imagen */}
        {imageStatus === 'loading' && (
          <div className="skeleton-loader" style={{ position: 'absolute', inset: 0, zIndex: 1 }} />
        )}

        {/* Imagen Real con Carga Perezosa (Lazy) */}
        {imageStatus !== 'error' && (
          <img
            src={imageUrl}
            alt={esp.nombre_cientifico}
            loading="lazy"
            onLoad={() => setImageStatus('loaded')}
            onError={() => setImageStatus('error')}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              opacity: imageStatus === 'loaded' ? 1 : 0,
              transition: 'opacity 0.4s ease-in-out',
              position: 'relative',
              zIndex: 2
            }}
          />
        )}

        {/* Fallback si no existe la imagen */}
        {imageStatus === 'error' && (
          <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, rgba(62,207,180,0.12), rgba(91,156,246,0.12))', flexDirection: 'column', gap: '8px', color: 'var(--text-tertiary)' }}>
            <ImageOff size={28} color="var(--accent-primary)" />
            <span style={{ fontSize: '0.72rem' }}>{esp.nombre_cientifico}</span>
          </div>
        )}

        {/* Badge Familia superpuesta */}
        <div style={{ position: 'absolute', top: '10px', right: '10px', zIndex: 4 }}>
          <span className="badge badge-cyan" style={{ backdropFilter: 'blur(10px)', background: 'rgba(13, 17, 23, 0.8)', border: '1px solid rgba(62,207,180,0.3)', fontSize: '0.65rem' }}>
            {esp.familia}
          </span>
        </div>
      </div>

      {/* Contenido Texto Compacto */}
      <div style={{ padding: '16px 18px 20px', display: 'flex', flexDirection: 'column', gap: '4px', flex: 1, position: 'relative', zIndex: 2 }}>
        <h3 style={{ fontSize: '1.05rem', fontWeight: 700, fontStyle: 'italic', color: 'var(--text-primary)', lineHeight: 1.3 }}>
          {esp.nombre_cientifico}
        </h3>
        <h4 style={{ fontSize: '0.88rem', fontWeight: 600, color: 'var(--accent-primary)', lineHeight: 1.3 }}>
          "{esp.nombre_comun}"
        </h4>
      </div>
    </div>
  );
}

/* ─── Tarjeta Esqueleto para Estado de Carga ─── */
function SkeletonCard() {
  return (
    <div className="liquid-glass" style={{ padding: 0, borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
      <div className="skeleton-loader" style={{ height: '170px', width: '100%' }} />
      <div style={{ padding: '16px 18px 20px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <div className="skeleton-loader" style={{ height: '18px', width: '75%', borderRadius: '4px' }} />
        <div className="skeleton-loader" style={{ height: '14px', width: '50%', borderRadius: '4px' }} />
      </div>
    </div>
  );
}

/* ─── Componente Principal de Catálogo ─── */
export default function CatalogoEspecies({ apiBase }) {
  const [especies, setEspecies] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [busqueda, setBusqueda] = useState('');
  const [familiaFiltro, setFamiliaFiltro] = useState('TODAS');
  const [coralSeleccionado, setCoralSeleccionado] = useState(null);
  const [mostrarModalAgregar, setMostrarModalAgregar] = useState(false);
  
  // Estado para la Carga Procedural por Lotes
  const LOTE_INICIAL = 12;
  const INCREMENTO_LOTE = 8;
  const [limiteLote, setLimiteLote] = useState(LOTE_INICIAL);

  const cargarEspecies = async () => {
    try {
      const res = await fetch(`${apiBase}/especies`);
      const data = await res.json();
      setEspecies(data);
    } catch (err) {
      console.error('Error al cargar catálogo:', err);
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarEspecies();
  }, [apiBase]);

  // Resetear el límite al buscar o filtrar
  useEffect(() => {
    setLimiteLote(LOTE_INICIAL);
  }, [busqueda, familiaFiltro]);

  const familiasDisponibles = ['TODAS', ...new Set(especies.map((e) => e.familia))];

  const especiesFiltradas = especies.filter((e) => {
    const coincideTexto =
      e.nombre_cientifico.toLowerCase().includes(busqueda.toLowerCase()) ||
      e.nombre_comun.toLowerCase().includes(busqueda.toLowerCase());
    const coincideFamilia = familiaFiltro === 'TODAS' || e.familia === familiaFiltro;
    return coincideTexto && coincideFamilia;
  });

  const especiesProcedurales = especiesFiltradas.slice(0, limiteLote);
  const hayMasEspecies = limiteLote < especiesFiltradas.length;

  const cargarMas = () => {
    setLimiteLote((prev) => prev + INCREMENTO_LOTE);
  };

  return (
    <div className="animate-fade-in" style={{ maxWidth: '1200px', margin: '0 auto' }}>
      {/* Barra Control Top Bar Compacta */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', marginBottom: '24px' }}>
        {/* Título Compacto */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <h2 style={{ fontSize: '1.4rem', fontWeight: 800, letterSpacing: '-0.5px' }}>
            Catálogo de Corales
          </h2>
          <span className="badge badge-cyan" style={{ fontSize: '0.72rem', padding: '4px 10px' }}>
            {cargando ? '...' : `${especiesFiltradas.length} especies`}
          </span>
        </div>

        {/* Buscador, Filtro y Botón Agregar Especie */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          {/* Buscador */}
          <div style={{ position: 'relative', width: '240px' }}>
            <Search size={16} color="var(--text-tertiary)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)' }} />
            <input
              type="text"
              placeholder="Buscar coral..."
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
              className="input-glass"
              style={{ padding: '8px 14px 8px 36px', fontSize: '0.85rem', height: '38px', borderRadius: 'var(--radius-pill)' }}
            />
          </div>

          {/* Filtro Familia */}
          <select
            value={familiaFiltro}
            onChange={(e) => setFamiliaFiltro(e.target.value)}
            className="input-glass"
            style={{
              width: 'auto',
              height: '38px',
              padding: '0 16px',
              fontSize: '0.85rem',
              borderRadius: 'var(--radius-pill)',
              color: 'var(--accent-primary)',
              fontWeight: 600,
              cursor: 'pointer'
            }}
          >
            {familiasDisponibles.map((f, i) => (
              <option key={i} value={f} style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)' }}>
                {f === 'TODAS' ? 'Todas las familias' : f}
              </option>
            ))}
          </select>

          {/* Botón Agregar Nueva Especie */}
          <button
            onClick={() => setMostrarModalAgregar(true)}
            className="btn-primary"
            style={{ height: '38px', padding: '0 18px', fontSize: '0.85rem' }}
          >
            <Plus size={16} /> Agregar Especie
          </button>
        </div>
      </div>

      {/* Grid de Tarjetas o Skeletons */}
      {cargando ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '20px' }}>
          {Array.from({ length: 12 }).map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      ) : (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: '20px' }}>
            {especiesProcedurales.map((esp) => (
              <CoralCard
                key={esp.id}
                esp={esp}
                apiBase={apiBase}
                onSelect={(selected) => setCoralSeleccionado(selected)}
              />
            ))}
          </div>

          {/* Botón de Carga Procedural / Ver Más */}
          {hayMasEspecies && (
            <div style={{ textAlign: 'center', marginTop: '36px', marginBottom: '20px' }}>
              <button
                onClick={cargarMas}
                className="btn-secondary"
                style={{ padding: '12px 32px', fontSize: '0.95rem' }}
              >
                Cargar más corales ({especiesFiltradas.length - limiteLote} restantes) <ChevronDown size={18} />
              </button>
            </div>
          )}
        </>
      )}

      {/* Modal Informativo de Detalle del Coral */}
      {coralSeleccionado && (
        <ModalDetalleCoral
          esp={coralSeleccionado}
          apiBase={apiBase}
          onClose={() => setCoralSeleccionado(null)}
        />
      )}

      {/* Modal Formulario para Agregar Nueva Especie */}
      {mostrarModalAgregar && (
        <ModalAgregarEspecie
          apiBase={apiBase}
          onClose={() => setMostrarModalAgregar(false)}
          onEspecieCreada={() => cargarEspecies()}
        />
      )}
    </div>
  );
}
