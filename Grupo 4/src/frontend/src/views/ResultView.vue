<script setup>
import { computed } from 'vue';
import { useDiagnosisStore } from '../stores/diagnosisStore';
import BaseButton from '../components/common/BaseButton.vue';
import ExplanabilityPanel from '../components/diagnosis/ExplanabilityPanel.vue';

const emit = defineEmits(['restart']);
const store = useDiagnosisStore();

const detectedSpecies = computed(() => store.detectedSpecies);
const topCandidates = computed(() => store.topCandidateSpecies);

const handleRestart = () => {
  emit('restart');
};

// Función para obtener la URL de la imagen usando import.meta.glob
const getSpeciesImage = (spec) => {
  if (!spec?.id) return null;
  
  const images = import.meta.glob('../assets/*.{jpg,png,webp,jpeg,svg}', { eager: true });
  const extensions = ['jpg', 'png', 'webp', 'jpeg', 'svg'];
  const id = spec.id.toLowerCase();
  
  for (const ext of extensions) {
    const path = `../assets/${id}.${ext}`;
    if (images[path]) {
      return images[path].default || images[path];
    }
  }
  return null;
};

// Formatear el nombre científico en cursiva (para mostrar en HTML)
const formatScientificName = (name) => {
  if (!name) return '<i>Clasificación Desconocida</i>';
  if (name.includes('<')) return name;
  return `<i>${name}</i>`;
};
</script>

<template>
  <div class="w-full max-w-4xl flex flex-col items-center px-4">
    
    <!-- Título de Finalización -->
    <div class="text-center mb-8">
      <div 
        :class="[
          'inline-flex p-3 rounded-full border mb-4',
          detectedSpecies 
            ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' 
            : 'bg-amber-500/10 border-amber-500/20 text-amber-400'
        ]"
      >
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path 
            v-if="detectedSpecies" 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" 
          />
          <path 
            v-else 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" 
          />
        </svg>
      </div>
      <h2 class="font-display font-extrabold text-3xl text-slate-100">
        {{ detectedSpecies ? 'Diagnóstico Concluido' : 'Especies con Mayor Coincidencia' }}
      </h2>
      <p class="text-sm text-slate-400 mt-2 max-w-xl mx-auto">
        {{ 
          detectedSpecies 
            ? 'El motor ha concluido la evaluación. Se muestran las 3 especies con mayor grado de coincidencia morfológica:' 
            : 'Se presentan las 3 especies con mayor porcentaje de coincidencia morfológica en la base de conocimientos:' 
        }}
      </p>
    </div>

    <!-- Lista de las 3 Especies con Mayor Grado de Coincidencia -->
    <div v-if="topCandidates.length > 0" class="w-full max-w-2xl space-y-6 mb-8">
      <div 
        v-for="(cand, idx) in topCandidates" 
        :key="cand.id || idx"
        :class="[
          'bg-slate-900/60 backdrop-blur-md border rounded-3xl overflow-hidden shadow-2xl transition-all duration-300',
          cand.certainty === 100 
            ? 'border-emerald-500/50 shadow-emerald-950/20' 
            : 'border-slate-800 hover:border-teal-500/30'
        ]"
      >
        <!-- Cabecera de la Especie -->
        <div class="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-900 p-5 border-b border-slate-800 flex justify-between items-center">
          <div>
            <span 
              :class="[
                'text-xs font-semibold uppercase tracking-wider block mb-0.5',
                cand.certainty === 100 ? 'text-emerald-400' : 'text-teal-400'
              ]"
            >
              {{ cand.certainty === 100 ? 'Especie Identificada (#1)' : `Coincidencia #${idx + 1}` }}
            </span>
            <h3 class="font-display font-bold text-xl md:text-2xl text-slate-100" v-html="formatScientificName(cand.name || cand.species_name)">
            </h3>
          </div>

          <!-- Badge de Porcentaje de Coincidencia -->
          <div class="flex flex-col items-end">
            <span 
              :class="[
                'px-3 py-1 rounded-full text-xs font-bold border',
                cand.certainty === 100 
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' 
                  : 'bg-teal-500/10 text-teal-400 border-teal-500/30'
              ]"
            >
              {{ cand.certainty }}% Coincidencia
            </span>
            <span class="text-[10px] font-mono text-slate-500 mt-1">
              {{ cand.matched_attributes }}/{{ cand.total_attributes }} atributos coincidentes
            </span>
          </div>
        </div>

        <!-- Detalles de la Especie -->
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
            
            <div class="space-y-4">
              <div>
                <h4 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">Descripción</h4>
                <p class="text-xs text-slate-300 leading-relaxed">
                  {{ cand.description || 'Sin descripción disponible.' }}
                </p>
              </div>

              <div>
                <h4 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1">Hábitat Natural</h4>
                <p class="text-xs text-slate-300">
                  {{ cand.habitat || 'Desconocido' }}
                </p>
              </div>

              <!-- Atributos Morfológicos de la Especie -->
              <div v-if="cand.attributes && Object.keys(cand.attributes).length > 0">
                <h4 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">Atributos Morfológicos</h4>
                <div class="grid grid-cols-1 gap-1 bg-slate-950/40 p-2.5 rounded-xl border border-slate-800/60">
                  <div v-for="(val, key) in cand.attributes" :key="key" class="text-xs flex justify-between">
                    <span class="text-slate-400 font-mono">{{ key.replace('_', ' ') }}:</span>
                    <span class="text-teal-300 font-semibold">{{ val }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Imagen de la Especie -->
            <div class="flex flex-col items-center justify-center">
              <div class="w-full aspect-square rounded-2xl bg-slate-950/60 border border-slate-800 flex items-center justify-center text-slate-600 overflow-hidden shadow-inner relative group">
                <img
                  v-if="getSpeciesImage(cand)"
                  :src="getSpeciesImage(cand)"
                  :alt="cand.name || 'Especie'"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div v-else class="text-center p-4 flex flex-col items-center gap-1.5">
                  <svg class="w-10 h-10 text-slate-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
                  </svg>
                  <span class="text-[10px] font-mono">Sin imagen disponible</span>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- Si no hay especies candidatas -->
    <div v-else class="w-full max-w-2xl bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-3xl p-8 text-center mb-8">
      <p class="text-sm text-slate-300">
        No se pudieron calcular coincidencias para las especies registradas. Pruebe iniciando un nuevo diagnóstico.
      </p>
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