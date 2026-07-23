<script setup>
import { computed } from 'vue';
import { useDiagnosisStore } from '../stores/diagnosisStore';
import BaseButton from '../components/common/BaseButton.vue';
import ExplanabilityPanel from '../components/diagnosis/ExplanabilityPanel.vue';

const emit = defineEmits(['restart']);
const store = useDiagnosisStore();

const species = computed(() => store.detectedSpecies);

const handleRestart = () => {
  emit('restart');
};
</script>

<template>
  <div class="w-full max-w-4xl flex flex-col items-center px-4">
    
    <!-- Título de Finalización -->
    <div class="text-center mb-8">
      <div class="inline-flex p-3 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 mb-4">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h2 class="font-display font-extrabold text-3xl text-slate-100">Diagnóstico Concluido</h2>
      <p class="text-sm text-slate-400 mt-2">El motor de inferencia ha finalizado el análisis morfológico</p>
    </div>

    <!-- Ficha Técnica de la Especie -->
    <div class="w-full max-w-2xl bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-3xl overflow-hidden shadow-2xl mb-8">
      
      <!-- Cabecera de la Ficha -->
      <div class="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-900 p-6 border-b border-slate-800/80">
        <span class="text-xs font-semibold uppercase tracking-wider text-teal-400 block mb-1">Especie Identificada</span>
        <h1 class="font-display font-extrabold text-2xl md:text-3xl text-slate-100 italic">
          {{ species?.name || 'Clasificación Desconocida' }}
        </h1>
      </div>

      <!-- Contenido de la Ficha -->
      <div class="p-8">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
          
          <!-- Información Textual -->
          <div class="space-y-6">
            <div>
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Descripción</h3>
              <p class="text-sm text-slate-300 leading-relaxed">
                {{ species?.description || 'El espécimen no pudo clasificarse dentro de las reglas del motor o no se han cargado datos.' }}
              </p>
            </div>

            <div>
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Hábitat Natural</h3>
              <p class="text-sm text-slate-300 leading-relaxed">
                {{ species?.habitat || 'Desconocido' }}
              </p>
            </div>

            <div v-if="species?.field_characteristics && species.field_characteristics.length > 0">
              <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Características Clave en Campo</h3>
              <ul class="space-y-2">
                <li
                  v-for="(char, idx) in species.field_characteristics"
                  :key="idx"
                  class="text-sm text-slate-300 flex items-start gap-2.5"
                >
                  <span class="inline-block w-1.5 h-1.5 rounded-full bg-teal-400 mt-2"></span>
                  {{ char }}
                </li>
              </ul>
            </div>
          </div>

          <!-- Imagen / Visualización -->
          <div class="flex flex-col items-center justify-center">
            <div class="w-full aspect-square rounded-2xl bg-slate-950/60 border border-slate-800 flex items-center justify-center text-slate-600 overflow-hidden shadow-inner relative group">
              <img
                v-if="species?.image_url"
                :src="species.image_url"
                :alt="species?.name"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div v-else class="text-center p-6 flex flex-col items-center gap-2">
                <!-- Icono de cámara SVG -->
                <svg class="w-12 h-12 text-slate-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
                </svg>
                <span class="text-xs font-mono">Sin imagen científica disponible</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Panel de Explicabilidad (Trazas) -->
    <div class="w-full max-w-2xl mb-8">
      <ExplanabilityPanel />
    </div>

    <!-- Botones de Acción -->
    <div class="flex justify-center gap-4 mt-4">
      <BaseButton variant="primary" @click="handleRestart">
        Realizar Nuevo Diagnóstico
      </BaseButton>
    </div>

  </div>
</template>
