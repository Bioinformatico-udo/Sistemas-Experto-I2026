import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { X, Plus, Upload, CheckCircle2, AlertCircle, Sparkles } from 'lucide-react';

export default function ModalAgregarEspecie({ apiBase, onClose, onEspecieCreada }) {
  const [formData, setFormData] = useState({
    nombre_cientifico: '',
    nombre_comun: '',
    familia: 'Acroporidae',
    orden: 'Scleractinia',
    tipo: 'Escleractinio',
    habitat: 'Parque Nacional Archipiélago de Los Roques, Venezuela',
    descripcion: '',
    forma: 'ramificada',
    color: 'marrón',
    superficie: 'copas',
    tiene_coralitos: true,
    urticante: false
  });

  const [imagenPreview, setImagenPreview] = useState(null);
  const [imagenBase64, setImagenBase64] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [mensajeExito, setMensajeExito] = useState(null);
  const [error, setError] = useState(null);

  const familiasComunes = [
    'Acroporidae', 'Milleporidae', 'Montastraeidae', 'Poritidae',
    'Siderastreidae', 'Faviidae', 'Meandrinidae', 'Agariciidae',
    'Mussidae', 'Merulinidae', 'Pocilloporidae', 'Stylasteridae'
  ];

  // Cerrar con la tecla Escape
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  // Prevenir scroll en body
  useEffect(() => {
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleImagenChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      setError('La imagen no debe superar los 5 MB.');
      return;
    }

    const reader = new FileReader();
    reader.onloadend = () => {
      setImagenPreview(reader.result);
      setImagenBase64(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.nombre_cientifico.trim() || !formData.nombre_comun.trim()) {
      setError('Por favor completa el nombre científico y el nombre común.');
      return;
    }

    setCargando(true);
    setError(null);

    const payload = {
      nombre_cientifico: formData.nombre_cientifico.trim(),
      nombre_comun: formData.nombre_comun.trim(),
      familia: formData.familia,
      orden: formData.orden,
      tipo: formData.tipo,
      habitat: formData.habitat.trim(),
      descripcion: formData.descripcion.trim(),
      caracteristicas: {
        forma: formData.forma,
        color: formData.color,
        superficie: formData.superficie,
        tiene_coralitos: formData.tiene_coralitos,
        urticante: formData.urticante
      },
      imagen_base64: imagenBase64
    };

    try {
      const res = await fetch(`${apiBase}/especies`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Error al guardar la especie');
      }

      const data = await res.json();
      setMensajeExito(data.mensaje || 'Especie registrada exitosamente en especies.json');
      
      setTimeout(() => {
        if (onEspecieCreada) onEspecieCreada(data.especie);
        onClose();
      }, 1400);
    } catch (err) {
      setError(err.message);
    } finally {
      setCargando(false);
    }
  };

  const modalContent = (
    <div
      style={{
        position: 'fixed',
        inset: 0,
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
      {/* Contenedor del Formulario Modal */}
      <div
        className="liquid-glass animate-scale-in"
        style={{
          width: '100%',
          maxWidth: '620px',
          maxHeight: '88vh',
          overflowY: 'auto',
          borderRadius: 'var(--radius-xl)',
          border: '1px solid rgba(62, 207, 180, 0.3)',
          boxShadow: '0 24px 64px rgba(0, 0, 0, 0.7)',
          position: 'relative',
          background: 'rgba(22, 27, 34, 0.96)',
          padding: '28px'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Botón Cerrar */}
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '16px',
            right: '16px',
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
            transition: 'all 0.2s ease'
          }}
        >
          <X size={18} />
        </button>

        {/* Encabezado */}
        <div style={{ marginBottom: '20px' }}>
          <span className="badge badge-cyan" style={{ fontSize: '0.7rem' }}>
            Registro Biológico
          </span>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, marginTop: '4px' }}>
            Agregar Nueva Especie de Coral
          </h2>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Completa la ficha técnica para añadir el registro a <code>especies.json</code> y guardar su fotografía.
          </p>
        </div>

        {mensajeExito ? (
          <div className="liquid-glass" style={{ padding: '24px', textAlign: 'center', borderLeft: '4px solid var(--accent-primary)' }}>
            <CheckCircle2 size={36} color="var(--accent-primary)" style={{ margin: '0 auto 12px' }} />
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-primary)' }}>{mensajeExito}</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginTop: '6px' }}>Actualizando catálogo en vivo...</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {error && (
              <div style={{ padding: '10px 14px', borderRadius: 'var(--radius-md)', background: 'rgba(255, 107, 157, 0.12)', border: '1px solid rgba(255, 107, 157, 0.3)', color: 'var(--accent-coral)', fontSize: '0.85rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <AlertCircle size={16} /> {error}
              </div>
            )}

            {/* Fila 1: Nombre Científico & Nombre Común */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '4px' }}>
                  Nombre Científico *
                </label>
                <input
                  type="text"
                  name="nombre_cientifico"
                  value={formData.nombre_cientifico}
                  onChange={handleChange}
                  placeholder="ej. Acropora palmata"
                  required
                  className="input-glass"
                  style={{ padding: '10px 14px', fontSize: '0.9rem' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '4px' }}>
                  Nombre Común / Vernáculo *
                </label>
                <input
                  type="text"
                  name="nombre_comun"
                  value={formData.nombre_comun}
                  onChange={handleChange}
                  placeholder="ej. Coral Cuerno de Alce"
                  required
                  className="input-glass"
                  style={{ padding: '10px 14px', fontSize: '0.9rem' }}
                />
              </div>
            </div>

            {/* Fila 2: Familia, Orden y Tipo */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '12px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '4px' }}>
                  Familia Taxonómica
                </label>
                <select
                  name="familia"
                  value={formData.familia}
                  onChange={handleChange}
                  className="input-glass"
                  style={{ padding: '10px 10px', fontSize: '0.85rem', cursor: 'pointer' }}
                >
                  {familiasComunes.map((fam, idx) => (
                    <option key={idx} value={fam} style={{ background: 'var(--bg-surface)' }}>{fam}</option>
                  ))}
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '4px' }}>
                  Orden
                </label>
                <select
                  name="orden"
                  value={formData.orden}
                  onChange={handleChange}
                  className="input-glass"
                  style={{ padding: '10px 10px', fontSize: '0.85rem', cursor: 'pointer' }}
                >
                  <option value="Scleractinia" style={{ background: 'var(--bg-surface)' }}>Scleractinia</option>
                  <option value="Anthoathecata" style={{ background: 'var(--bg-surface)' }}>Anthoathecata</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '4px' }}>
                  Tipo
                </label>
                <select
                  name="tipo"
                  value={formData.tipo}
                  onChange={handleChange}
                  className="input-glass"
                  style={{ padding: '10px 10px', fontSize: '0.85rem', cursor: 'pointer' }}
                >
                  <option value="Escleractinio" style={{ background: 'var(--bg-surface)' }}>Escleractinio</option>
                  <option value="Hidrocoral" style={{ background: 'var(--bg-surface)' }}>Hidrocoral</option>
                </select>
              </div>
            </div>

            {/* Fila 3: Hábitat */}
            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '4px' }}>
                Hábitat Registrado
              </label>
              <input
                type="text"
                name="habitat"
                value={formData.habitat}
                onChange={handleChange}
                placeholder="ej. Zonas someras (1-10m) con fuerte oleaje en Los Roques"
                className="input-glass"
                style={{ padding: '10px 14px', fontSize: '0.88rem' }}
              />
            </div>

            {/* Fila 4: Descripción */}
            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '4px' }}>
                Descripción Taxonómica Breve
              </label>
              <textarea
                name="descripcion"
                rows={2}
                value={formData.descripcion}
                onChange={handleChange}
                placeholder="Descripción morfológica breve de la colonia..."
                className="input-glass"
                style={{ resize: 'none', padding: '10px 14px', fontSize: '0.88rem' }}
              />
            </div>

            {/* Fila 5: Características Diagnósticas */}
            <div style={{ background: 'rgba(0,0,0,0.2)', padding: '14px', borderRadius: 'var(--radius-md)', border: '1px solid var(--liquid-border)' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--accent-primary)', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.5px', display: 'block', marginBottom: '10px' }}>
                Características Diagnósticas
              </span>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '10px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>Forma</label>
                  <input type="text" name="forma" value={formData.forma} onChange={handleChange} placeholder="ramificada, masiva..." className="input-glass" style={{ padding: '6px 10px', fontSize: '0.82rem' }} />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>Color</label>
                  <input type="text" name="color" value={formData.color} onChange={handleChange} placeholder="marrón, verde..." className="input-glass" style={{ padding: '6px 10px', fontSize: '0.82rem' }} />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-tertiary)' }}>Superficie</label>
                  <input type="text" name="superficie" value={formData.superficie} onChange={handleChange} placeholder="copas, porosa..." className="input-glass" style={{ padding: '6px 10px', fontSize: '0.82rem' }} />
                </div>
              </div>

              <div style={{ display: 'flex', gap: '20px', marginTop: '12px' }}>
                <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                  <input type="checkbox" name="tiene_coralitos" checked={formData.tiene_coralitos} onChange={handleChange} />
                  ¿Tiene Coralitos Visibles?
                </label>
                <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                  <input type="checkbox" name="urticante" checked={formData.urticante} onChange={handleChange} />
                  ¿Producen Urticación?
                </label>
              </div>
            </div>

            {/* Fila 6: Fotografía del Coral */}
            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', fontWeight: 600, marginBottom: '6px' }}>
                Fotografía de la Especie (.jpg / .png)
              </label>

              <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                <label
                  className="btn-secondary"
                  style={{ cursor: 'pointer', fontSize: '0.85rem', padding: '8px 16px' }}
                >
                  <Upload size={16} /> Seleccionar Imagen
                  <input type="file" accept="image/*" onChange={handleImagenChange} style={{ display: 'none' }} />
                </label>

                {imagenPreview && (
                  <div style={{ width: '48px', height: '48px', borderRadius: '10px', overflow: 'hidden', border: '1px solid var(--accent-primary)', flexShrink: 0 }}>
                    <img src={imagenPreview} alt="Vista previa" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
                  </div>
                )}
              </div>
            </div>

            {/* Botones de Acción */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '12px' }}>
              <button type="button" onClick={onClose} className="btn-secondary" disabled={cargando}>
                Cancelar
              </button>
              <button type="submit" className="btn-primary" disabled={cargando}>
                {cargando ? 'Guardando...' : <><Plus size={16} /> Guardar Especie</>}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );

  return ReactDOM.createPortal(modalContent, document.body);
}
