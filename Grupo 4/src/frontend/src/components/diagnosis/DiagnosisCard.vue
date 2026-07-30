<script setup>
import { computed } from 'vue';
import { useDiagnosisStore } from '../../stores/diagnosisStore';
import BaseButton from '../common/BaseButton.vue';

const store = useDiagnosisStore();

// Obtener la pregunta activa del store
const question = computed(() => store.currentQuestion);

// Enviar la respuesta seleccionada al store
const handleSelectOption = async (value) => {
  if (store.loading) return;
  await store.answerQuestion(question.value.fact, value);
};
</script>

<template>
  <div v-if="question" class="w-full max-w-2xl bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
    <!-- Indicador de Categoría -->
    <div class="flex justify-between items-center mb-6">
      <span class="px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-teal-500/10 text-teal-400 border border-teal-500/20">
        {{ question.category || 'Categoría General' }}
      </span>
      <span class="text-xs font-mono text-slate-500">
        Paso {{ store.currentStepIndex + 1 }}
      </span>
    </div>

    <!-- Enunciado de la Pregunta -->
    <h2 class="font-display font-bold text-xl md:text-2xl text-slate-100 mb-8 leading-snug">
      {{ question.question }}
    </h2>

    <!-- Opciones de Respuesta -->
    <div class="grid grid-cols-1 gap-4 mb-8">
      <button
        v-for="opt in question.options"
        :key="opt.value"
        @click="handleSelectOption(opt.value)"
        :disabled="store.loading"
        class="w-full text-left p-5 rounded-2xl bg-slate-800/40 border border-slate-800 hover:border-teal-500/40 hover:bg-slate-800/80 transition-all duration-300 transform active:scale-[0.99] group relative cursor-pointer disabled:opacity-50 disabled:pointer-events-none"
      >
        <div class="flex items-center justify-between">
          <span class="font-medium text-slate-200 group-hover:text-slate-100 transition-colors">
            {{ opt.label }}
          </span>
          <div class="w-5 h-5 rounded-full border-2 border-slate-700 group-hover:border-teal-400 flex items-center justify-center transition-colors">
            <div class="w-2.5 h-2.5 rounded-full bg-teal-400 scale-0 group-hover:scale-100 transition-transform"></div>
          </div>
        </div>
      </button>
    </div>

    <!-- Controles Inferiores (Atrás) -->
    <div class="flex justify-start items-center border-t border-slate-800/60 pt-6">
      <BaseButton
        variant="secondary"
        @click="store.goBack()"
        :disabled="!store.canGoBack || store.loading"
        class="flex items-center gap-2"
      >
        <!-- Icono Atrás SVG -->
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Atrás
      </BaseButton>
    </div>
  </div>
</template>
