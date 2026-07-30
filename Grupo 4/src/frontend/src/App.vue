<script setup>
import { ref, onMounted } from 'vue';
import { useDiagnosisStore } from './stores/diagnosisStore';
import { useAuth } from './composables/useAuth';
import HomeView from './views/HomeView.vue';
import DiagnosisView from './views/DiagnosisView.vue';
import ResultView from './views/ResultView.vue';
import LoginModal from './components/common/LoginModal.vue';
import AddSpeciesModal from './components/common/AddSpeciesModal.vue';

const store = useDiagnosisStore();
const { isLoggedIn, isExpert, userRole, username, logout, checkAuth } = useAuth();

const currentView = ref('home');
const showLoginModal = ref(false);
const showAddSpeciesModal = ref(false);

onMounted(async () => {
  await checkAuth();          // Restaurar sesión desde localStorage
  await store.loadQuestions();
});

const startDiagnosis = () => { currentView.value = 'diagnosis'; };
const showResult      = () => { currentView.value = 'result'; };
const cancelDiagnosis = () => { currentView.value = 'home'; };
const restartDiagnosis = async () => { currentView.value = 'home'; };

async function handleLogout() {
  await logout();
  currentView.value = 'home';
}
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col justify-between selection:bg-teal-500/30 selection:text-teal-200 relative overflow-hidden">

    <!-- Gradientes de fondo -->
    <div class="absolute top-[-20%] left-[-20%] w-[60%] aspect-square rounded-full bg-cyan-900/10 blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-[-20%] right-[-20%] w-[60%] aspect-square rounded-full bg-emerald-900/10 blur-[120px] pointer-events-none"></div>

    <!-- ═══════════════════════════════════════════════════════
         ENCABEZADO / BARRA DE NAVEGACIÓN
         ═══════════════════════════════════════════════════════ -->
    <header class="relative z-10 w-full border-b border-slate-900 bg-slate-950/80 backdrop-blur-md px-6 py-4">
      <div class="max-w-6xl mx-auto flex justify-between items-center gap-4">

        <!-- Logo -->
        <button
          id="nav-logo-btn"
          @click="currentView = 'home'"
          class="flex items-center gap-2.5 font-display font-extrabold text-lg text-slate-100 tracking-tight cursor-pointer shrink-0"
        >
          <span class="p-1.5 rounded-lg bg-gradient-to-br from-cyan-500 to-emerald-500 text-slate-950">
            <svg class="w-5 h-5 stroke-[2.5]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
          </span>
          CRUSTACEA <span class="text-teal-400 font-normal text-sm font-mono tracking-normal">SE v1.0</span>
        </button>

        <!-- Controles del lado derecho -->
        <div class="flex items-center gap-3 flex-wrap justify-end">

          <!-- Indicador de estado del motor -->
          <div class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800/80 text-xs font-mono text-slate-400">
            <span :class="['w-2 h-2 rounded-full', store.error ? 'bg-rose-500' : 'bg-emerald-500 animate-pulse']"></span>
            {{ store.error ? 'ERROR' : 'MOTOR ONLINE' }}
          </div>

          <!-- ─── MODO INVITADO ───────────────────────────── -->
          <template v-if="!isLoggedIn">
            <!-- Insignia de invitado -->
            <div
              id="nav-guest-badge"
              class="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-800 border border-slate-700 text-slate-400"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
              </svg>
              Modo Invitado
            </div>

            <!-- Botón de inicio de sesión -->
            <button
              id="nav-login-btn"
              @click="showLoginModal = true"
              class="flex items-center gap-1.5 px-4 py-1.5 rounded-xl text-xs font-semibold
                     border border-cyan-500/40 text-cyan-400 bg-cyan-950/30
                     hover:bg-cyan-500/15 hover:border-cyan-400/70 hover:text-cyan-300
                     transition-all duration-200"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
              </svg>
              Iniciar Sesión (Experto)
            </button>
          </template>

          <!-- ─── MODO EXPERTO ────────────────────────────── -->
          <template v-else>
            <!-- Insignia de experto -->
            <div
              id="nav-expert-badge"
              class="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold
                     bg-gradient-to-r from-teal-900/60 to-emerald-900/60
                     border border-teal-500/40 text-teal-300"
            >
              <svg class="w-3 h-3 text-teal-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.403 12.652a3 3 0 000-5.304 3 3 0 00-3.75-3.751 3 3 0 00-5.305 0 3 3 0 00-3.751 3.75 3 3 0 000 5.305 3 3 0 003.75 3.751 3 3 0 005.305 0 3 3 0 003.751-3.75zm-2.546-4.46a.75.75 0 00-1.214-.883l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
              </svg>
              Modo Experto
            </div>

            <!-- Botón activo para agregar especie -->
            <button
              id="nav-add-species-btn"
              @click="showAddSpeciesModal = true"
              title="Agregar nueva especie a la Base de Conocimiento"
              class="flex items-center gap-1.5 px-4 py-1.5 rounded-xl text-xs font-semibold
                     border border-emerald-500/50 text-emerald-300 bg-emerald-950/40
                     hover:bg-emerald-500/20 hover:border-emerald-400 hover:text-emerald-200
                     transition-all duration-200 shadow-md shadow-emerald-950/30"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
              + Agregar Especie
            </button>

            <!-- Cerrar sesión -->
            <button
              id="nav-logout-btn"
              @click="handleLogout"
              class="flex items-center gap-1.5 px-4 py-1.5 rounded-xl text-xs font-semibold
                     border border-rose-500/30 text-rose-400 bg-rose-950/20
                     hover:bg-rose-500/15 hover:border-rose-400/60 hover:text-rose-300
                     transition-all duration-200"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.25 9V5.25A2.25 2.25 0 0110.5 3h6a2.25 2.25 0 012.25 2.25v13.5A2.25 2.25 0 0116.5 21h-6a2.25 2.25 0 01-2.25-2.25V15M12 9l3 3m0 0l-3 3m3-3H2.25" />
              </svg>
              Cerrar Sesión
            </button>
          </template>

        </div>
      </div>
    </header>

    <!-- ═══════════════════════════════════════════════════════
         CONTENIDO PRINCIPAL
         ═══════════════════════════════════════════════════════ -->
    <main class="relative z-10 flex-1 w-full max-w-6xl mx-auto flex items-center justify-center py-12 px-6">
      <!-- Cargador inicial -->
      <div v-if="store.loading && store.questions.length === 0" class="flex flex-col items-center gap-3 text-slate-400 font-mono text-sm">
        <svg class="animate-spin h-8 w-8 text-teal-400" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Cargando base de conocimiento...
      </div>

      <div v-else-if="store.error && store.questions.length === 0" class="text-center p-8 bg-rose-950/20 border border-rose-500/30 rounded-3xl max-w-md">
        <h3 class="font-display font-bold text-rose-400 text-lg mb-2">Error de Inicialización</h3>
        <p class="text-sm text-slate-400 mb-4">{{ store.error }}</p>
        <button
          class="px-4 py-2 rounded-xl text-sm font-semibold bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 transition-colors"
          @click="store.loadQuestions()"
        >
          Reintentar Carga
        </button>
      </div>

      <Transition v-else name="slide-fade" mode="out-in">
        <div :key="currentView" class="w-full flex justify-center">
          <HomeView     v-if="currentView === 'home'"      @start="startDiagnosis" />
          <DiagnosisView v-else-if="currentView === 'diagnosis'" @complete="showResult" @cancel="cancelDiagnosis" />
          <ResultView   v-else-if="currentView === 'result'" @restart="restartDiagnosis" />
        </div>
      </Transition>
    </main>

    <!-- ═══════════════════════════════════════════════════════
         PIE DE PÁGINA
         ═══════════════════════════════════════════════════════ -->
    <footer class="relative z-10 w-full border-t border-slate-900 bg-slate-950/60 backdrop-blur px-6 py-4 text-center text-xs text-slate-600">
      <div class="max-w-6xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-2">
        <p>© 2026 - Sistemas Expertos I-2026. Grupo 4.</p>
        <p>Modelado bajo Metodología Buchanan e Inferencia Hexagonal.</p>
      </div>
    </footer>

    <!-- ═══════════════════════════════════════════════════════
         VENTANAS MODALES
         ═══════════════════════════════════════════════════════ -->
    <Transition name="modal-fade">
      <LoginModal v-if="showLoginModal" @close="showLoginModal = false" />
    </Transition>

    <Transition name="modal-fade">
      <AddSpeciesModal v-if="showAddSpeciesModal" @close="showAddSpeciesModal = false" />
    </Transition>

  </div>
</template>

<style>
/* Animación slide-fade para transiciones entre vistas */
.slide-fade-enter-active { transition: all 0.3s cubic-bezier(0.4,0,0.2,1); }
.slide-fade-leave-active { transition: all 0.2s cubic-bezier(0.4,0,0.2,1); }
.slide-fade-enter-from  { opacity: 0; transform: translateY(10px); }
.slide-fade-leave-to    { opacity: 0; transform: translateY(-8px); }

/* Transición de desvanecimiento para el fondo modal */
.modal-fade-enter-active,
.modal-fade-leave-active { transition: opacity 0.2s ease; }
.modal-fade-enter-from,
.modal-fade-leave-to     { opacity: 0; }
</style>

