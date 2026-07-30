/**
 * Servicio API de Autenticación – Métodos del cliente HTTP para los endpoints de autenticación.
 * Todas las llamadas se dirigen a /api/v1/auth y utilizan fetch (sin dependencias adicionales).
 */

const AUTH_BASE = `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/auth`;

/**
 * Envía credenciales de inicio de sesión como datos de formulario OAuth2.
 * Retorna { access_token, token_type, expires_in, user } en caso de éxito.
 * Lanza un Error con el mensaje del servidor en caso de fallo.
 */
export async function loginRequest(username, password) {
  const body = new URLSearchParams({ username, password });

  const response = await fetch(`${AUTH_BASE}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || 'Error al iniciar sesión.');
  }

  return data;
}

/**
 * Llama a GET /auth/me con el token Bearer almacenado.
 * Retorna { authenticated, username, role } – siempre resuelve (sin lanzar errores para invitados).
 */
export async function getMeRequest(token) {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  const response = await fetch(`${AUTH_BASE}/me`, { headers });

  if (!response.ok) {
    return { authenticated: false, username: null, role: 'GUEST' };
  }

  return response.json();
}

/**
 * Llama a POST /auth/logout para confirmar el fin de sesión en el servidor.
 * La eliminación del token del almacenamiento la maneja el composable.
 */
export async function logoutRequest(token) {
  const headers = token ? { Authorization: `Bearer ${token}` } : {};

  await fetch(`${AUTH_BASE}/logout`, { method: 'POST', headers }).catch(() => {});
}

