<script setup>
import { ref, watch } from 'vue';
import { useAuth } from '@/composables/useAuth';

const { login, isLoggedIn, isLoading, authError, clearError } = useAuth();
const emit = defineEmits(['close']);

// ── Estado del formulario ─────────────────────────────────────
const usernameInput = ref('');
const passwordInput = ref('');
const showPassword   = ref(false);

// ── Validación ────────────────────────────────────────────────
const usernameError = ref('');
const passwordError = ref('');

function validateForm() {
  let valid = true;
  usernameError.value = '';
  passwordError.value = '';

  if (!usernameInput.value.trim()) {
    usernameError.value = 'El nombre de usuario es requerido.';
    valid = false;
  }
  if (!passwordInput.value) {
    passwordError.value = 'La contraseña es requerida.';
    valid = false;
  }
  return valid;
}

// Cerrar modal después de un inicio de sesión exitoso
watch(isLoggedIn, (val) => {
  if (val) emit('close');
});

async function handleSubmit() {
  clearError();
  if (!validateForm()) return;
  await login(usernameInput.value.trim(), passwordInput.value);
}

function handleClose() {
  clearError();
  usernameError.value = '';
  passwordError.value = '';
  emit('close');
}
</script>

<template>
  <!-- Fondo oscuro (Backdrop) -->
  <Teleport to="body">
    <div
      id="login-modal-backdrop"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm"
      @click.self="handleClose"
    >
      <!-- Panel del modal -->
      <div
        id="login-modal-panel"
        class="relative w-full max-w-md rounded-2xl border border-slate-700/60 bg-slate-900/95 shadow-2xl shadow-cyan-950/40 backdrop-blur-xl overflow-hidden"
        role="dialog"
        aria-modal="true"
        aria-labelledby="login-title"
      >
        <!-- Barra de acento superior -->
        <div class="h-1 w-full bg-gradient-to-r from-cyan-500 via-teal-400 to-emerald-500"></div>

        <!-- Encabezado -->
        <div class="px-7 pt-7 pb-4 flex justify-between items-start">
          <div>
            <h2 id="login-title" class="text-xl font-extrabold text-slate-100 tracking-tight">
              Iniciar Sesión
            </h2>
            <p class="text-sm text-slate-400 mt-1">
              Accede como <span class="text-teal-400 font-semibold">Experto Taxónomo</span> para gestionar la base de conocimiento.
            </p>
          </div>
          <button
            id="login-close-btn"
            @click="handleClose"
            class="text-slate-500 hover:text-slate-300 transition-colors p-1 rounded-lg hover:bg-slate-800"
            aria-label="Cerrar modal"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Formulario -->
        <form @submit.prevent="handleSubmit" class="px-7 pb-7 space-y-5" novalidate>

          <!-- Alerta de error del servidor -->
          <Transition name="fade">
            <div
              v-if="authError"
              id="login-error-alert"
              class="flex items-start gap-3 p-3.5 rounded-xl bg-rose-950/40 border border-rose-500/40 text-rose-300 text-sm"
            >
              <svg class="w-5 h-5 mt-0.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
              </svg>
              <span>{{ authError }}</span>
            </div>
          </Transition>

          <!-- Nombre de usuario -->
          <div class="space-y-1.5">
            <label for="login-username" class="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Usuario
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </span>
              <input
                id="login-username"
                v-model="usernameInput"
                type="text"
                autocomplete="username"
                placeholder="Ingresa tu usuario"
                :class="[
                  'w-full pl-10 pr-4 py-2.5 rounded-xl text-sm text-slate-100 placeholder-slate-600',
                  'bg-slate-800/70 border transition-all outline-none',
                  usernameError
                    ? 'border-rose-500/60 focus:border-rose-400 focus:ring-1 focus:ring-rose-400/30'
                    : 'border-slate-700/60 focus:border-teal-500 focus:ring-1 focus:ring-teal-500/30'
                ]"
              />
            </div>
            <p v-if="usernameError" class="text-xs text-rose-400 pl-1">{{ usernameError }}</p>
          </div>

          <!-- Contraseña -->
          <div class="space-y-1.5">
            <label for="login-password" class="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Contraseña
            </label>
            <div class="relative">
              <span class="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-500">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                </svg>
              </span>
              <input
                id="login-password"
                v-model="passwordInput"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                placeholder="••••••••••"
                :class="[
                  'w-full pl-10 pr-12 py-2.5 rounded-xl text-sm text-slate-100 placeholder-slate-600',
                  'bg-slate-800/70 border transition-all outline-none',
                  passwordError
                    ? 'border-rose-500/60 focus:border-rose-400 focus:ring-1 focus:ring-rose-400/30'
                    : 'border-slate-700/60 focus:border-teal-500 focus:ring-1 focus:ring-teal-500/30'
                ]"
              />
              <!-- Alternar mostrar/ocultar contraseña -->
              <button
                type="button"
                id="login-toggle-password"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors"
                :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
              >
                <svg v-if="showPassword" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                </svg>
                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
            </div>
            <p v-if="passwordError" class="text-xs text-rose-400 pl-1">{{ passwordError }}</p>
          </div>

          <!-- Enviar -->
          <button
            id="login-submit-btn"
            type="submit"
            :disabled="isLoading"
            class="w-full flex items-center justify-center gap-2 py-2.5 px-5 rounded-xl font-semibold text-sm
                   bg-gradient-to-r from-cyan-500 to-emerald-500 text-slate-950
                   hover:from-cyan-400 hover:to-emerald-400
                   disabled:opacity-60 disabled:cursor-not-allowed
                   transition-all duration-200 shadow-lg shadow-cyan-900/30"
          >
            <svg v-if="isLoading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
            </svg>
            {{ isLoading ? 'Verificando...' : 'Entrar como Experto' }}
          </button>

        </form>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>


<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
