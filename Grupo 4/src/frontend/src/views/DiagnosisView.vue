<script setup>
import { computed } from 'vue';
import { useDiagnosisStore } from '../stores/diagnosisStore';
import ProgressBar from '../components/common/ProgressBar.vue';
import DiagnosisCard from '../components/diagnosis/DiagnosisCard.vue';
import ExplanabilityPanel from '../components/diagnosis/ExplanabilityPanel.vue';
import BaseButton from '../components/common/BaseButton.vue';

const emit = defineEmits(['cancel', 'complete']);
const store = useDiagnosisStore();

// Cuando se detecte una especie (o se terminen las preguntas), transicionar a resultados
const isComplete = computed(() => {
  return store.detectedSpecies !== null || (!store.nextRecommendedFact && !store.loading);
});

// Vigilar si la inferencia terminó para emitir el evento
import { watch } from 'vue';
watch(isComplete, (newValue) => {
  if (newValue) {
    emit('complete');
  }
});
</script>

<template>
  <div class="w-full max-w-4xl flex flex-col items-center px-4">
    <!-- Header del flujo -->
    <div class="w-full flex justify-between items-center mb-8 pb-4 border-b border-slate-800/60">
      <h2 class="font-display font-bold text-lg text-slate-200 flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-teal-400 animate-pulse"></span>
        Diagnóstico Morfológico Activo
      </h2>
      <BaseButton variant="danger" @click="emit('cancel')">
        Cancelar
      </BaseButton>
    </div>

    <!-- Barra de progreso general -->
    <div class="w-full max-w-2xl mb-8">
      <ProgressBar :progress="store.progressPercentage" />
    </div>

    <!-- Contenedor del diagnóstico con transiciones -->
    <div class="w-full flex justify-center">
      <Transition name="slide-fade" mode="out-in">
        <div :key="store.nextRecommendedFact" class="w-full flex justify-center">
          <DiagnosisCard />
        </div>
      </Transition>
    </div>

    <!-- Loader de Inferencia -->
    <div v-if="store.loading" class="mt-6 flex items-center gap-2 text-teal-400 font-mono text-sm">
      <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      Consultando motor experto...
    </div>

    <!-- Panel de Explicabilidad en tiempo real -->
    <div class="w-full max-w-2xl mt-8">
      <ExplanabilityPanel />
    </div>
  </div>
</template>
