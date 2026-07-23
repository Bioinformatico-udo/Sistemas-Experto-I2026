<script setup>
import { useDiagnosisStore } from '../stores/diagnosisStore';
import BaseButton from '../components/common/BaseButton.vue';
import DeveloperGrid from '../components/portfolio/DeveloperGrid.vue';

const emit = defineEmits(['start']);
const store = useDiagnosisStore();

const handleStart = async () => {
  await store.startNewDiagnosis();
  emit('start');
};
</script>

<template>
  <div class="w-full flex flex-col items-center">
    
    <!-- Hero / Introducción -->
    <div class="text-center max-w-3xl mt-8 mb-16 px-4">
      <!-- Icono animado del crustáceo / Logo de bioingeniería -->
      <div class="inline-flex p-4 rounded-3xl bg-teal-500/10 border border-teal-500/20 mb-6 text-teal-400 animate-pulse">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 017.843 4.582M12 3a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-.778.099-1.533.284-2.253" />
        </svg>
      </div>

      <h1 class="font-display font-extrabold text-4xl sm:text-5xl lg:text-6xl text-slate-100 tracking-tight leading-none bg-gradient-to-r from-cyan-400 via-teal-400 to-emerald-400 bg-clip-text text-transparent mb-6">
        Clasificador de Crustáceos
      </h1>
      
      <p class="text-lg text-slate-300 leading-relaxed mb-8">
        Sistema Experto basado en reglas morfológicas desarrollado bajo la metodología de <strong class="text-teal-400">Buchanan</strong>. Identifica si un espécimen pertenece al subfilo <strong class="text-teal-400">Crustacea</strong> y clasifica su especie en la familia <strong class="text-teal-400">Porcellanidae</strong> mediante encadenamiento hacia adelante.
      </p>

      <div class="flex flex-col sm:flex-row justify-center gap-4">
        <BaseButton
          variant="primary"
          @click="handleStart"
          :disabled="store.loading"
          class="text-md py-3.5 px-8 font-extrabold flex items-center gap-2"
        >
          Iniciar Clasificación
          <!-- Flecha Derecha SVG -->
          <svg class="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </BaseButton>
      </div>
    </div>

    <!-- Sección Metodología / Ficha Técnica -->
    <div class="w-full max-w-4xl grid grid-cols-1 md:grid-cols-3 gap-6 mb-20 px-4">
      <div class="bg-slate-900/30 border border-slate-800 rounded-2xl p-6 shadow-md">
        <div class="text-teal-400 mb-4">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <h3 class="font-display font-bold text-lg text-slate-100 mb-2">Ingeniería del Conocimiento</h3>
        <p class="text-sm text-slate-400 leading-relaxed">
          Diseñado bajo la metodología de Buchanan estructurando el conocimiento morfológico a través de la identificación, conceptualización, formalización e implementación.
        </p>
      </div>
      
      <div class="bg-slate-900/30 border border-slate-800 rounded-2xl p-6 shadow-md">
        <div class="text-teal-400 mb-4">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h3 class="font-display font-bold text-lg text-slate-100 mb-2">Motor Forward Chaining</h3>
        <p class="text-sm text-slate-400 leading-relaxed">
          El backend en FastAPI evalúa las reglas taxonómicas en tiempo de ejecución disparando consecuencias basándose en la memoria de trabajo incremental.
        </p>
      </div>

      <div class="bg-slate-900/30 border border-slate-800 rounded-2xl p-6 shadow-md">
        <div class="text-teal-400 mb-4">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <h3 class="font-display font-bold text-lg text-slate-100 mb-2">Explicabilidad Completa</h3>
        <p class="text-sm text-slate-400 leading-relaxed">
          Cada conclusión final provee una traza lógica interactiva, permitiendo auditar qué reglas específicas se dispararon y por qué el sistema tomó dicha decisión.
        </p>
      </div>
    </div>

    <!-- Sección de Créditos del Equipo -->
    <div class="w-full max-w-6xl border-t border-slate-800/80 pt-16 px-4">
      <DeveloperGrid />
    </div>

  </div>
</template>
