<script setup>
import { ref, onMounted } from 'vue';
import { useDiagnosisStore } from './stores/diagnosisStore';
import HomeView from './views/HomeView.vue';
import DiagnosisView from './views/DiagnosisView.vue';
import ResultView from './views/ResultView.vue';

const store = useDiagnosisStore();
const currentView = ref('home'); // 'home', 'diagnosis', 'result'

onMounted(async () => {
  await store.loadQuestions();
});

const startDiagnosis = () => {
  currentView.value = 'diagnosis';
};

const showResult = () => {
  currentView.value = 'result';
};

const cancelDiagnosis = () => {
  currentView.value = 'home';
};

const restartDiagnosis = async () => {
  currentView.value = 'home';
};
</script>

<template>
  <div class="min-h-screen bg-slate-950 text-slate-100 font-sans flex flex-col justify-between selection:bg-teal-500/30 selection:text-teal-200 relative overflow-hidden">
    
    <!-- Efecto de gradiente radial de fondo (Atmósfera abisal) -->
    <div class="absolute top-[-20%] left-[-20%] w-[60%] aspect-square rounded-full bg-cyan-900/10 blur-[120px] pointer-events-none"></div>
    <div class="absolute bottom-[-20%] right-[-20%] w-[60%] aspect-square rounded-full bg-emerald-900/10 blur-[120px] pointer-events-none"></div>

    <!-- Barra de Navegación Header -->
    <header class="relative z-10 w-full border-b border-slate-900 bg-slate-950/80 backdrop-blur-md px-6 py-4">
      <div class="max-w-6xl mx-auto flex justify-between items-center">
        <!-- Logo -->
        <button @click="currentView = 'home'" class="flex items-center gap-2.5 font-display font-extrabold text-lg text-slate-100 tracking-tight cursor-pointer">
          <span class="p-1.5 rounded-lg bg-gradient-to-br from-cyan-500 to-emerald-500 text-slate-950">
            <!-- Icono científico SVG -->
            <svg class="w-5 h-5 stroke-[2.5]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
            </svg>
          </span>
          CRUSTACEA <span class="text-teal-400 font-normal text-sm font-mono tracking-normal">SE v1.0</span>
        </button>

        <!-- Indicador de Estado del Motor -->
        <div class="flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800/80 text-xs font-mono text-slate-400">
          <span :class="['w-2 h-2 rounded-full', store.error ? 'bg-rose-500' : 'bg-emerald-500 animate-pulse']"></span>
          {{ store.error ? 'ERROR' : 'MOTOR ONLINE' }}
        </div>
      </div>
    </header>

    <!-- Contenido Principal con Transiciones -->
    <main class="relative z-10 flex-1 w-full max-w-6xl mx-auto flex items-center justify-center py-12 px-6">
      <!-- Loader de arranque -->
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
        <BaseButton variant="secondary" @click="store.loadQuestions()">Reintentar Carga</BaseButton>
      </div>

      <Transition v-else name="slide-fade" mode="out-in">
        <div :key="currentView" class="w-full flex justify-center">
          <HomeView
            v-if="currentView === 'home'"
            @start="startDiagnosis"
          />
          <DiagnosisView
            v-else-if="currentView === 'diagnosis'"
            @complete="showResult"
            @cancel="cancelDiagnosis"
          />
          <ResultView
            v-else-if="currentView === 'result'"
            @restart="restartDiagnosis"
          />
        </div>
      </Transition>
    </main>

    <!-- Footer -->
    <footer class="relative z-10 w-full border-t border-slate-900 bg-slate-950/60 backdrop-blur px-6 py-4 text-center text-xs text-slate-600">
      <div class="max-w-6xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-2">
        <p>© 2026 - Sistemas Expertos I-2026. Grupo 4.</p>
        <p>Modelado bajo Metodología Buchanan e Inferencia Hexagonal.</p>
      </div>
    </footer>

  </div>
</template>
