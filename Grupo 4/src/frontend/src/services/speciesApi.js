/**
 * speciesApi.js – Funciones del cliente API para la gestión de especies.
 * Se dirige al endpoint /api/v1/species protegido por autenticación de Experto.
 */

const API_BASE = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1`;

/**
 * Envía una petición POST a /api/v1/species para crear una nueva especie y actualizar la base de conocimientos.
 * @param {Object} speciesPayload - Datos de CreateSpeciesRequest
 * @param {string} token - Token bearer JWT del usuario experto
 * @returns {Promise<Object>} Objeto JSON CreateSpeciesResponse
 */
export async function createSpecies(speciesPayload, token) {
  const headers = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}/species`, {
    method: 'POST',
    headers,
    body: JSON.stringify(speciesPayload),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || data.message || 'Error al crear la especie en la base de conocimientos.');
  }

  return data;
}

