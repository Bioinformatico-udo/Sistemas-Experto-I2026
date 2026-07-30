/**
 * useAuth – Composable reactivo para gestionar el estado de autenticación.
 * Maneja la persistencia del token en localStorage, inicio de sesión, cierre de sesión y restauración de sesión.
 *
 * Uso:
 *   import { useAuth } from '@/composables/useAuth'
 *   const { isLoggedIn, userRole, login, logout, checkAuth } = useAuth()
 */

import { ref, computed } from 'vue';
import { loginRequest, getMeRequest, logoutRequest } from '@/services/authApi';

const STORAGE_KEY = 'crustacea_auth_token';

// ─── Estado reactivo compartido (singleton a nivel de módulo) ─────────────────
const token = ref(localStorage.getItem(STORAGE_KEY) || null);
const userRole = ref('GUEST');
const username = ref(null);
const isLoading = ref(false);
const authError = ref(null);

const isLoggedIn = computed(() => userRole.value === 'EXPERT');
const isExpert   = computed(() => userRole.value === 'EXPERT');

// ─── Fábrica del composable ───────────────────────────────────────────────────
export function useAuth() {

  /**
   * Intenta iniciar sesión con las credenciales proporcionadas.
   * En caso de éxito: almacena el token y actualiza el estado reactivo.
   * En caso de fallo: establece authError.
   */
  async function login(usernameInput, password) {
    authError.value = null;
    isLoading.value = true;

    try {
      const data = await loginRequest(usernameInput, password);

      token.value = data.access_token;
      userRole.value = data.user?.role ?? 'EXPERT';
      username.value = data.user?.username ?? usernameInput;

      localStorage.setItem(STORAGE_KEY, data.access_token);
    } catch (err) {
      authError.value = err.message || 'Error al iniciar sesión.';
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Limpia la sesión localmente y notifica al servidor.
   */
  async function logout() {
    await logoutRequest(token.value);

    token.value = null;
    userRole.value = 'GUEST';
    username.value = null;
    authError.value = null;

    localStorage.removeItem(STORAGE_KEY);
  }

  /**
   * Al montar la aplicación: restaura la sesión desde el token en localStorage validándolo con /me.
   */
  async function checkAuth() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) return;

    try {
      const data = await getMeRequest(stored);

      if (data.authenticated && data.role === 'EXPERT') {
        token.value = stored;
        userRole.value = data.role;
        username.value = data.username;
      } else {
        // Token expirado o inválido – limpieza silenciosa
        localStorage.removeItem(STORAGE_KEY);
        token.value = null;
        userRole.value = 'GUEST';
        username.value = null;
      }
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }

  function clearError() {
    authError.value = null;
  }

  return {
    // Estado
    token,
    userRole,
    username,
    isLoggedIn,
    isExpert,
    isLoading,
    authError,
    // Acciones
    login,
    logout,
    checkAuth,
    clearError,
  };
}

