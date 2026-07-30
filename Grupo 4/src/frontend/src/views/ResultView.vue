<script setup>
import { computed, ref } from 'vue';
import { useDiagnosisStore } from '../stores/diagnosisStore';
import BaseButton from '../components/common/BaseButton.vue';
import ExplanabilityPanel from '../components/diagnosis/ExplanabilityPanel.vue';

const emit = defineEmits(['restart']);
const store = useDiagnosisStore();

const species = computed(() => store.detectedSpecies);
const candidates = computed(() => store.topCandidateSpecies);

// Estado para los paneles desplegables
const expandedSections = ref({
  taxonomy: false,
});

const toggleSection = (section) => {
  expandedSections.value[section] = !expandedSections.value[section];
};

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

// Verificar si hay datos de taxonomía
const hasTaxonomy = computed(() => {
  return species.value?.taxonomy && Object.keys(species.value.taxonomy).length > 0;
});

// Formatear la taxonomía para mostrar
const formatTaxonomy = (taxonomy) => {
  if (!taxonomy) return [];
  const labels = {
    kingdom: 'Reino',
    phylum: 'Filo',
    subphylum: 'Subfilo',
    class: 'Clase',
    order: 'Orden',
    infraorder: 'Infraorden',
    family: 'Familia',
    genus: 'Género',
    species: 'Especie'
  };
  
  return Object.entries(taxonomy)
    .filter(([key]) => labels[key])
    .map(([key, value]) => ({
      label: labels[key] || key,
      value: key === 'species' ? `<i>${value}</i>` : value
    }));
};
</script>

<template>
  <div class="w-full max-w-4xl flex flex-col items-center px-4">
    
    <!-- ═══════════════════════════════════════════════════════
         CASO 1: ESPECIE DETECTADA CON 100% DE EXACTITUD
         ═══════════════════════════════════════════════════════ -->
    <template v-if="species">
      <!-- Título de Finalización -->
      <div class="text-center mb-8">
        <div class="inline-flex p-3 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 mb-4">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 class="font-display font-extrabold text-3xl text-slate-100">Diagnóstico Concluido</h2>
        <p class="text-sm text-slate-400 mt-2">El motor de inferencia ha identificado la especie con 100% de exactitud</p>
      </div>

      <!-- Ficha Técnica Completa de la Especie Detectada -->
      <div class="w-full max-w-2xl bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-3xl overflow-hidden shadow-2xl mb-8">
        
        <!-- Cabecera de la Ficha -->
        <div class="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-900 p-6 border-b border-slate-800/80">
          <span class="text-xs font-semibold uppercase tracking-wider text-teal-400 block mb-1">Especie Identificada</span>
          <h1 class="font-display font-extrabold text-2xl md:text-3xl text-slate-100" v-html="formatScientificName(species?.name)">
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
                  {{ species?.description || 'No hay descripción disponible para esta especie.' }}
                </p>
              </div>

              <div>
                <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">Hábitat Natural</h3>
                <p class="text-sm text-slate-300 leading-relaxed">
                  {{ species?.habitat || 'Desconocido' }}
                </p>
              </div>

              <!-- Atributos Morfológicos -->
              <div v-if="species?.attributes && Object.keys(species.attributes).length > 0">
                <h3 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">Atributos Morfológicos</h3>
                <div class="grid grid-cols-1 gap-1.5 bg-slate-950/40 p-3 rounded-xl border border-slate-800/60">
                  <div v-for="(val, key) in species.attributes" :key="key" class="text-xs flex justify-between">
                    <span class="text-slate-400 font-mono">{{ key.replace('_', ' ') }}:</span>
                    <span class="text-teal-300 font-semibold">{{ val }}</span>
                  </div>
                </div>
              </div>

              <!-- Características Clave en Campo -->
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

            <!-- Imagen de la Especie -->
            <div class="flex flex-col items-center justify-center">
              <div class="w-full aspect-square rounded-2xl bg-slate-950/60 border border-slate-800 flex items-center justify-center text-slate-600 overflow-hidden shadow-inner relative group">
                <img
                  v-if="getSpeciesImage(species)"
                  :src="getSpeciesImage(species)"
                  :alt="species?.name || 'Especie'"
                  class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div v-else class="text-center p-6 flex flex-col items-center gap-2">
                  <svg class="w-12 h-12 text-slate-700" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6.827 6.175A2.31 2.31 0 015.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 00-1.134-.175 2.31 2.31 0 01-1.64-1.055l-.822-1.316a2.192 2.192 0 00-1.736-1.039 48.774 48.774 0 00-5.232 0 2.192 2.192 0 00-1.736 1.039l-.821 1.316z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 12.75a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM18.75 10.5h.008v.008h-.008V10.5z" />
                  </svg>
                  <span class="text-xs font-mono">Sin imagen científica disponible</span>
                </div>
              </div>
            </div>

          </div>

          <!-- Sección de Taxonomía Desplegable -->
          <div v-if="hasTaxonomy" class="mt-8 border-t border-slate-800 pt-6">
            <div class="bg-slate-800/40 rounded-xl overflow-hidden border border-slate-700/50">
              <button 
                @click="toggleSection('taxonomy')"
                class="w-full flex items-center justify-between p-4 text-left hover:bg-slate-800/60 transition-colors duration-200"
              >
                <span class="text-sm font-semibold text-slate-300 flex items-center gap-2">
                  <svg class="w-4 h-4 text-teal-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                  </svg>
                  Taxonomía Completa
                </span>
                <svg 
                  class="w-5 h-5 text-slate-500 transition-transform duration-300" 
                  :class="{ 'rotate-180': expandedSections.taxonomy }"
                  fill="none" 
                  stroke="currentColor" 
                  stroke-width="2" 
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                </svg>
              </button>
              <div 
                v-show="expandedSections.taxonomy"
                class="px-4 pb-4 space-y-1.5"
              >
                <div 
                  v-for="item in formatTaxonomy(species?.taxonomy)" 
                  :key="item.label"
                  class="flex items-start gap-3 text-sm"
                >
                  <span class="text-slate-500 font-medium min-w-[80px]">{{ item.label }}:</span>
                  <span class="text-slate-300" v-html="item.value"></span>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </template>

    <!-- ═══════════════════════════════════════════════════════
         CASO 2: NO SE ENCONTRÓ ESPECIE CON 100% DE EXACTITUD
         ═══════════════════════════════════════════════════════ -->
    <template v-else>
      <div class="text-center mb-8">
        <div class="inline-flex p-3 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 mb-4">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
          </svg>
        </div>
        <h2 class="font-display font-extrabold text-3xl text-slate-100">No se encontró una especie exacta</h2>
        <p class="text-sm text-slate-400 mt-2 max-w-xl mx-auto">
          No se detectó una especie con 100% de certidumbre según los datos ingresados. A continuación se presentan las 3 especies más probables con al menos 50% de concordancia y sin atributos en conflicto:
        </p>
      </div>

      <!-- Lista de las 3 Especies Candidatas -->
      <div v-if="candidates.length > 0" class="w-full max-w-2xl space-y-6 mb-8">
        <div 
          v-for="(cand, idx) in candidates" 
          :key="cand.id || idx"
          class="bg-slate-900/60 backdrop-blur-md border border-slate-800 hover:border-teal-500/30 rounded-3xl overflow-hidden shadow-xl transition-all duration-300"
        >
          <!-- Cabecera Candidata -->
          <div class="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-900 p-5 border-b border-slate-800 flex justify-between items-center">
            <div>
              <span class="text-xs font-semibold uppercase tracking-wider text-amber-400 block mb-0.5">
                Candidata #{{ idx + 1 }}
              </span>
              <h3 class="font-display font-bold text-xl text-slate-100" v-html="formatScientificName(cand.name || cand.species_name)">
              </h3>
            </div>

            <!-- Porcentaje de Certeza -->
            <div class="flex flex-col items-end">
              <span class="px-3 py-1 rounded-full text-xs font-bold bg-teal-500/10 text-teal-400 border border-teal-500/30">
                {{ cand.certainty }}% Exactitud
              </span>
              <span class="text-[10px] font-mono text-slate-500 mt-1">
                {{ cand.matched_attributes }}/{{ cand.total_attributes }} atributos coincidentes
              </span>
            </div>
          </div>

          <!-- Detalles Candidata -->
          <div class="p-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
              
              <div class="space-y-4">
                <p v-if="cand.description" class="text-xs text-slate-300 leading-relaxed">
                  {{ cand.description }}
                </p>
                <p v-if="cand.habitat" class="text-xs text-slate-400">
                  <strong class="text-slate-500 uppercase tracking-wider">Hábitat:</strong> {{ cand.habitat }}
                </p>

                <!-- Atributos Morfológicos de la Especie -->
                <div v-if="cand.attributes && Object.keys(cand.attributes).length > 0">
                  <h4 class="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-1.5">Atributos Morfológicos</h4>
                  <div class="grid grid-cols-1 gap-1 bg-slate-950/40 p-2.5 rounded-xl border border-slate-800/60">
                    <div v-for="(val, key) in cand.attributes" :key="key" class="text-xs flex justify-between">
                      <span class="text-slate-400 font-mono">{{ key.replace('_', ' ') }}:</span>
                      <span class="text-teal-300 font-semibold">{{ val }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Imagen Candidata -->
              <div class="flex flex-col items-center justify-center">
                <div class="w-full aspect-square rounded-2xl bg-slate-950/60 border border-slate-800 flex items-center justify-center text-slate-600 overflow-hidden shadow-inner relative group">
                  <img
                    v-if="getSpeciesImage(cand)"
                    :src="getSpeciesImage(cand)"
                    :alt="cand.name || 'Candidata'"
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

      <!-- Si no hay candidatas -->
      <div v-else class="w-full max-w-2xl bg-slate-900/60 backdrop-blur-md border border-slate-800 rounded-3xl p-8 text-center mb-8">
        <p class="text-sm text-slate-300">
          No se pudieron calcular coincidencias para las especies registradas. Pruebe iniciando un nuevo diagnóstico.
        </p>
      </div>
    </template>

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