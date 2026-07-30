<script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuth } from '@/composables/useAuth';
import { useDiagnosisStore } from '@/stores/diagnosisStore';
import { createSpecies } from '@/services/speciesApi';

const emit = defineEmits(['close', 'species-added']);

const { token } = useAuth();
const diagnosisStore = useDiagnosisStore();

// ── 1. General & Taxonomy Form State ──────────────────────────────────────────
const name = ref('');
const idOverride = ref('');
const genus = ref('Petrolisthes');
const customGenus = ref('');
const habitat = ref('');
const fieldCharacteristicsText = ref('');

// Predefined genera for Porcellanidae
const commonGenera = [
  'Petrolisthes',
  'Pachycheles',
  'Porcellana',
  'Megalobrachium',
  'Clastotoechus',
  'Neopisosoma',
  'Minyocerus',
  'Pisidia',
  'Otro...'
];

// Computed species ID slugified in lowercase
const computedId = computed(() => {
  if (idOverride.value.trim()) {
    return idOverride.value.trim().toLowerCase().replace(/\s+/g, '_');
  }
  if (!name.value.trim()) return '';
  return name.value.trim().toLowerCase().replace(/\s+/g, '_');
});

// Final genus value
const finalGenus = computed(() => {
  if (genus.value === 'Otro...') {
    return customGenus.value.trim();
  }
  return genus.value;
});

// ── 2. Image Upload State ──────────────────────────────────────────────────────
const imageFile = ref(null);
const imagePreview = ref(null);
const imageBase64 = ref(null);
const imageFilename = ref('');
const isDragging = ref(false);

function handleFileSelect(event) {
  const file = event.target.files?.[0];
  if (file) processImageFile(file);
}

function handleDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer?.files?.[0];
  if (file) processImageFile(file);
}

function processImageFile(file) {
  if (!file.type.startsWith('image/')) {
    alert('Por favor selecciona un archivo de imagen válido (JPG, PNG, WEBP).');
    return;
  }
  if (file.size > 2 * 1024 * 1024) {
    alert('El tamaño de la imagen no debe superar los 2 MB.');
    return;
  }

  imageFile.value = file;
  imageFilename.value = file.name;

  const reader = new FileReader();
  reader.onload = (e) => {
    imagePreview.value = e.target.result;
    imageBase64.value = e.target.result;
  };
  reader.readAsDataURL(file);
}

function removeImage() {
  imageFile.value = null;
  imagePreview.value = null;
  imageBase64.value = null;
  imageFilename.value = '';
}

// ── 3. Dynamic Morphological Attributes State ─────────────────────────────────
// Mandatory rule for Porcellanidae: "segmento_antenal" is required
const attributes = ref([
  {
    mode: 'existing',
    fact: 'segmento_antenal',
    value: 'largo',
    customValue: '',
    questionText: '',
    optionLabelText: '',
    isRequired: true,
  }
]);

// Available existing questions/facts from store
const existingFacts = computed(() => {
  return diagnosisStore.questions.map(q => ({
    fact: q.fact,
    question: q.question,
    options: q.options || [],
    category: q.category || 'General'
  }));
});

function addAttributeRow() {
  attributes.value.push({
    mode: 'existing',
    fact: '',
    value: '',
    customValue: '',
    questionText: '',
    optionLabelText: '',
    isRequired: false,
  });
}

function removeAttributeRow(index) {
  if (attributes.value[index]?.isRequired) return;
  attributes.value.splice(index, 1);
}

function onExistingFactChange(row) {
  row.value = '';
  row.customValue = '';
  const selectedFact = existingFacts.value.find(f => f.fact === row.fact);
  if (selectedFact && selectedFact.options.length > 0) {
    row.value = selectedFact.options[0].value;
  }
}

function getOptionsForFact(factName) {
  const f = existingFacts.value.find(item => item.fact === factName);
  return f ? f.options : [];
}

// ── 4. Validation, Loading, & Submit ──────────────────────────────────────────
const isLoading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');
const nameError = ref('');
const genusError = ref('');
const antennaError = ref('');

function validateForm() {
  let valid = true;
  nameError.value = '';
  genusError.value = '';
  antennaError.value = '';
  errorMessage.value = '';

  if (!name.value.trim()) {
    nameError.value = 'El nombre de la especie es obligatorio.';
    valid = false;
  }

  if (!finalGenus.value) {
    genusError.value = 'El género taxonómico es obligatorio.';
    valid = false;
  }

  const antennaRow = attributes.value.find(r => r.fact === 'segmento_antenal' || r.fact === 'largo_antena');
  if (!antennaRow || (!antennaRow.value && !antennaRow.customValue)) {
    antennaError.value = 'El hecho obligatorio "Largo de Antena" debe tener un valor asignado.';
    valid = false;
  }

  for (let i = 0; i < attributes.value.length; i++) {
    const row = attributes.value[i];
    if (row.mode === 'existing' && !row.fact) {
      errorMessage.value = `Fila ${i + 1}: Debe seleccionar un hecho existente.`;
      return false;
    }
    if (row.mode === 'custom' && !row.fact.trim()) {
      errorMessage.value = `Fila ${i + 1}: Debe ingresar el identificador del nuevo campo.`;
      return false;
    }
  }

  return valid;
}

async function handleSubmit() {
  if (!validateForm()) return;

  isLoading.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const attributesMap = {};
    const factLabels = {};
    const optionLabels = {};

    // NOTE: 'genus' is NOT added to attributesMap per requirements.
    // It is sent via request.genus and request.taxonomy.genus.
    attributes.value.forEach(row => {
      const factName = row.mode === 'existing' ? row.fact : row.fact.trim().toLowerCase().replace(/\s+/g, '_');
      if (factName === 'genus') return; // Skip genus if selected accidentally in attributes

      const val = row.value === '__custom__' || !row.value ? row.customValue.trim() : row.value;
      attributesMap[factName] = val;

      if (row.mode === 'custom') {
        if (row.questionText.trim()) {
          factLabels[factName] = row.questionText.trim();
        }
        if (row.optionLabelText.trim()) {
          optionLabels[factName] = { [val]: row.optionLabelText.trim() };
        }
      } else if (row.customValue.trim()) {
        optionLabels[factName] = { [val]: row.customValue.trim() };
      }
    });

    const fieldCharacteristicsList = fieldCharacteristicsText.value
      .split('\n')
      .map(s => s.trim())
      .filter(Boolean);

    // Extract species epithet for taxonomy
    const nameParts = name.value.trim().split(/\s+/);
    const speciesEpithet = nameParts.length >= 2 ? nameParts.slice(1).join(' ') : nameParts[0];

    const taxonomyMap = {
      kingdom: 'Animalia',
      phylum: 'Arthropoda',
      subphylum: 'Crustacea',
      class: 'Malacostraca',
      order: 'Decapoda',
      infraorder: 'Anomura',
      family: 'Porcellanidae',
      genus: finalGenus.value,
      species: speciesEpithet
    };

    const payload = {
      id: computedId.value,
      name: name.value.trim(),
      description: `Especie de la familia Porcellanidae del género ${finalGenus.value}.`,
      habitat: habitat.value.trim(),
      field_characteristics: fieldCharacteristicsList,
      image_url: `/assets/${computedId.value}.${imageFilename.value ? imageFilename.value.split('.').pop() : 'jpg'}`,
      image_data: imageBase64.value,
      image_filename: imageFilename.value || `${computedId.value}.jpg`,
      genus: finalGenus.value,
      taxonomy: taxonomyMap,
      attributes: attributesMap,
      fact_labels: factLabels,
      option_labels: optionLabels,
    };

    const response = await createSpecies(payload, token.value);

    if (response.success) {
      successMessage.value = response.message || 'Especie registrada exitosamente.';
      await diagnosisStore.loadQuestions();
      emit('species-added', response.species);

      setTimeout(() => {
        emit('close');
      }, 1500);
    } else {
      errorMessage.value = response.message || 'Error al guardar la especie.';
    }
  } catch (err) {
    errorMessage.value = err.message || 'Error de comunicación con el servidor.';
  } finally {
    isLoading.value = false;
  }
}

function handleClose() {
  emit('close');
}

onMounted(async () => {
  if (diagnosisStore.questions.length === 0) {
    await diagnosisStore.loadQuestions();
  }
});
</script>

<template>
  <Teleport to="body">
    <div
      id="add-species-modal-backdrop"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md overflow-y-auto"
      @click.self="handleClose"
    >
      <div
        id="add-species-modal-panel"
        class="relative w-full max-w-3xl my-8 rounded-2xl border border-slate-700/60 bg-slate-900/95 shadow-2xl shadow-cyan-950/50 backdrop-blur-xl overflow-hidden text-slate-100 flex flex-col max-h-[90vh]"
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <!-- Top accent bar -->
        <div class="h-1.5 w-full bg-gradient-to-r from-cyan-500 via-teal-400 to-emerald-500 shrink-0"></div>

        <!-- Header -->
        <div class="px-6 pt-5 pb-4 border-b border-slate-800 flex justify-between items-start shrink-0">
          <div>
            <div class="flex items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-mono font-semibold bg-emerald-500/15 border border-emerald-500/40 text-emerald-300">
                Porcellanidae (Porcelánidos)
              </span>
              <span class="text-xs text-slate-400 font-mono">Modo Experto</span>
            </div>
            <h2 id="modal-title" class="text-xl font-extrabold text-slate-100 tracking-tight mt-1">
              Registrar Nueva Especie
            </h2>
          </div>
          <button
            id="close-modal-btn"
            @click="handleClose"
            class="text-slate-500 hover:text-slate-300 transition-colors p-1.5 rounded-lg hover:bg-slate-800"
            aria-label="Cerrar modal"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- Form Body (Scrollable) -->
        <form @submit.prevent="handleSubmit" class="flex-1 overflow-y-auto px-6 py-6 space-y-8">

          <!-- Alert Notifications -->
          <Transition name="fade">
            <div v-if="errorMessage" class="p-4 rounded-xl bg-rose-950/50 border border-rose-500/50 text-rose-300 text-sm flex items-start gap-3">
              <svg class="w-5 h-5 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v3.75m9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
              </svg>
              <span>{{ errorMessage }}</span>
            </div>
          </Transition>

          <Transition name="fade">
            <div v-if="successMessage" class="p-4 rounded-xl bg-emerald-950/50 border border-emerald-500/50 text-emerald-300 text-sm flex items-start gap-3">
              <svg class="w-5 h-5 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>{{ successMessage }}</span>
            </div>
          </Transition>

          <!-- ── SECCIÓN 1: INFORMACIÓN GENERAL Y TAXONÓMICA ─────────────────── -->
          <div class="space-y-4">
            <div class="flex items-center gap-2 pb-1 border-b border-slate-800 text-teal-400 font-semibold text-sm uppercase tracking-wider">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
              </svg>
              1. Información Taxonómica y General
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Name -->
              <div class="space-y-1.5">
                <label class="text-xs font-semibold text-slate-300">
                  Nombre de la Especie <span class="text-rose-400">*</span>
                </label>
                <input
                  v-model="name"
                  type="text"
                  placeholder="ej. Petrolisthes armatus"
                  :class="[
                    'w-full px-3.5 py-2.5 rounded-xl text-sm bg-slate-800/80 border transition-all outline-none text-slate-100 placeholder-slate-500',
                    nameError ? 'border-rose-500 focus:ring-1 focus:ring-rose-500' : 'border-slate-700/70 focus:border-teal-500 focus:ring-1 focus:ring-teal-500'
                  ]"
                />
                <p v-if="nameError" class="text-xs text-rose-400">{{ nameError }}</p>
                <p v-if="computedId" class="text-[11px] font-mono text-slate-500">
                  ID generado: <span class="text-teal-400">{{ computedId }}</span>
                </p>
              </div>

              <!-- Genus -->
              <div class="space-y-1.5">
                <label class="text-xs font-semibold text-slate-300">
                  Género Taxonómico <span class="text-rose-400">*</span>
                </label>
                <select
                  v-model="genus"
                  class="w-full px-3.5 py-2.5 rounded-xl text-sm bg-slate-800/80 border border-slate-700/70 text-slate-100 outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                >
                  <option v-for="g in commonGenera" :key="g" :value="g">{{ g }}</option>
                </select>
                <input
                  v-if="genus === 'Otro...'"
                  v-model="customGenus"
                  type="text"
                  placeholder="Escriba el nuevo género"
                  class="mt-2 w-full px-3.5 py-2 rounded-xl text-sm bg-slate-800/80 border border-slate-700 text-slate-100 outline-none focus:border-teal-500"
                />
                <p v-if="genusError" class="text-xs text-rose-400">{{ genusError }}</p>
              </div>
            </div>

            <!-- Habitat -->
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-slate-300">Distribución Geográfica / Hábitat (Opcional)</label>
              <textarea
                v-model="habitat"
                rows="2"
                placeholder="ej. Zona intermareal bajo rocas y sustratos coralinos del Caribe..."
                class="w-full px-3.5 py-2 rounded-xl text-sm bg-slate-800/80 border border-slate-700/70 text-slate-100 placeholder-slate-500 outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
              ></textarea>
            </div>

            <!-- Field Characteristics -->
            <div class="space-y-1.5">
              <label class="text-xs font-semibold text-slate-300">Características de Campo (Notas de identificación rápida, 1 por línea)</label>
              <textarea
                v-model="fieldCharacteristicsText"
                rows="2"
                placeholder="ej. Coloración marrón rojiza&#10;Pinzas alargadas con margen liso"
                class="w-full px-3.5 py-2 rounded-xl text-sm bg-slate-800/80 border border-slate-700/70 text-slate-100 placeholder-slate-500 outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
              ></textarea>
            </div>
          </div>

          <!-- ── SECCIÓN 2: CARGA DE IMAGEN ─────────────────────────────────── -->
          <div class="space-y-4">
            <div class="flex items-center gap-2 pb-1 border-b border-slate-800 text-teal-400 font-semibold text-sm uppercase tracking-wider">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
              </svg>
              2. Carga de Imagen (Assets del Frontend)
            </div>

            <div
              :class="[
                'border-2 border-dashed rounded-2xl p-6 text-center transition-all cursor-pointer relative overflow-hidden',
                isDragging ? 'border-teal-400 bg-teal-950/20' : 'border-slate-700/80 bg-slate-800/40 hover:border-slate-600'
              ]"
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleDrop"
              @click="$refs.fileInput.click()"
            >
              <input
                ref="fileInput"
                type="file"
                accept="image/jpeg,image/png,image/webp,image/jpg"
                class="hidden"
                @change="handleFileSelect"
              />

              <div v-if="!imagePreview" class="flex flex-col items-center gap-2 text-slate-400">
                <div class="p-3 rounded-full bg-slate-800 text-teal-400 border border-slate-700">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                  </svg>
                </div>
                <p class="text-sm font-semibold text-slate-200">Arrastra la imagen aquí o haz clic para seleccionar</p>
                <p class="text-xs text-slate-500">JPG, PNG, WEBP (Máx. 2MB). Se guardará en <span class="font-mono text-teal-400">assets/{{ computedId || 'id' }}.jpg</span></p>
              </div>

              <div v-else class="flex flex-col sm:flex-row items-center gap-4 text-left">
                <img :src="imagePreview" alt="Previsualización" class="w-32 h-32 object-cover rounded-xl border border-slate-700 shrink-0" />
                <div class="flex-1 space-y-1">
                  <p class="text-sm font-semibold text-slate-200">{{ imageFilename }}</p>
                  <p class="text-xs text-slate-400">Imagen lista para integrarse en <span class="font-mono text-teal-300">/assets/{{ computedId }}.jpg</span></p>
                  <button
                    type="button"
                    @click.stop="removeImage"
                    class="mt-2 text-xs font-semibold text-rose-400 hover:text-rose-300 flex items-center gap-1"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                    </svg>
                    Eliminar imagen
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- ── SECCIÓN 3: ATRIBUTOS MORFOLÓGICOS DINÁMICOS ─────────────────── -->
          <div class="space-y-4">
            <div class="flex justify-between items-center pb-1 border-b border-slate-800">
              <div class="flex items-center gap-2 text-teal-400 font-semibold text-sm uppercase tracking-wider">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0m-9.75 0h9.75" />
                </svg>
                3. Atributos Morfológicos (Motor de Inferencia)
              </div>

              <button
                type="button"
                @click="addAttributeRow"
                class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-800 border border-slate-700 text-teal-300 hover:bg-slate-700 flex items-center gap-1.5 transition-colors"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
                + Agregar Atributo
              </button>
            </div>

            <p v-if="antennaError" class="text-xs text-rose-400">{{ antennaError }}</p>

            <!-- Attribute Rows -->
            <div class="space-y-3">
              <div
                v-for="(row, idx) in attributes"
                :key="idx"
                class="p-4 rounded-xl bg-slate-800/60 border border-slate-700/60 space-y-3 relative"
              >
                <!-- Badge header for row -->
                <div class="flex justify-between items-center">
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-mono font-bold text-slate-400">#{{ idx + 1 }}</span>
                    <span v-if="row.isRequired" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/20 border border-amber-500/40 text-amber-300">
                      Obligatorio (Porcellanidae)
                    </span>

                    <!-- Mode Toggle (if not mandatory) -->
                    <div v-else class="flex rounded-lg bg-slate-900 p-0.5 border border-slate-700/80 text-xs">
                      <button
                        type="button"
                        @click="row.mode = 'existing'"
                        :class="['px-2.5 py-1 rounded-md transition-colors font-medium', row.mode === 'existing' ? 'bg-teal-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200']"
                      >
                        Existente
                      </button>
                      <button
                        type="button"
                        @click="row.mode = 'custom'"
                        :class="['px-2.5 py-1 rounded-md transition-colors font-medium', row.mode === 'custom' ? 'bg-teal-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-slate-200']"
                      >
                        Nuevo Campo
                      </button>
                    </div>
                  </div>

                  <!-- Delete button (disabled for mandatory) -->
                  <button
                    v-if="!row.isRequired"
                    type="button"
                    @click="removeAttributeRow(idx)"
                    class="text-slate-500 hover:text-rose-400 transition-colors p-1"
                    title="Eliminar atributo"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                    </svg>
                  </button>
                </div>

                <!-- Mode A: Existing Fact -->
                <div v-if="row.mode === 'existing'" class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div class="space-y-1">
                    <label class="text-[11px] font-semibold text-slate-400">Hecho / Atributo Existente</label>
                    <select
                      v-model="row.fact"
                      :disabled="row.isRequired"
                      @change="onExistingFactChange(row)"
                      class="w-full px-3 py-2 rounded-xl text-xs bg-slate-900 border border-slate-700 text-slate-100 outline-none focus:border-teal-500 disabled:opacity-75"
                    >
                      <option v-for="f in existingFacts" :key="f.fact" :value="f.fact">
                        {{ f.fact }} ({{ f.category }})
                      </option>
                    </select>
                  </div>

                  <div class="space-y-1">
                    <label class="text-[11px] font-semibold text-slate-400">Valor Asignado</label>
                    <select
                      v-model="row.value"
                      class="w-full px-3 py-2 rounded-xl text-xs bg-slate-900 border border-slate-700 text-slate-100 outline-none focus:border-teal-500"
                    >
                      <option v-for="opt in getOptionsForFact(row.fact)" :key="opt.value" :value="opt.value">
                        {{ opt.label }} ({{ opt.value }})
                      </option>
                      <option value="__custom__">+ Ingresar valor personalizado</option>
                    </select>

                    <input
                      v-if="row.value === '__custom__'"
                      v-model="row.customValue"
                      type="text"
                      placeholder="Ingrese nuevo valor"
                      class="mt-1.5 w-full px-3 py-1.5 rounded-xl text-xs bg-slate-900 border border-slate-700 text-slate-100 outline-none focus:border-teal-500"
                    />
                  </div>
                </div>

                <!-- Mode B: Custom New Fact -->
                <div v-else class="space-y-3">
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div class="space-y-1">
                      <label class="text-[11px] font-semibold text-slate-400">Nombre del Hecho (fact id)</label>
                      <input
                        v-model="row.fact"
                        type="text"
                        placeholder="ej. presencia_espinas_carpales"
                        class="w-full px-3 py-2 rounded-xl text-xs bg-slate-900 border border-slate-700 text-slate-100 outline-none focus:border-teal-500 font-mono"
                      />
                    </div>
                    <div class="space-y-1">
                      <label class="text-[11px] font-semibold text-slate-400">Valor Asignado</label>
                      <input
                        v-model="row.customValue"
                        type="text"
                        placeholder="ej. presente / 3_espinas"
                        class="w-full px-3 py-2 rounded-xl text-xs bg-slate-900 border border-slate-700 text-slate-100 outline-none focus:border-teal-500"
                      />
                    </div>
                  </div>

                  <div class="space-y-1">
                    <label class="text-[11px] font-semibold text-slate-400">Pregunta Descriptiva para Usuarios (Opcional)</label>
                    <input
                      v-model="row.questionText"
                      type="text"
                      placeholder="ej. ¿Posee espinas en el carpo del quelípedo?"
                      class="w-full px-3 py-2 rounded-xl text-xs bg-slate-900 border border-slate-700 text-slate-100 outline-none focus:border-teal-500"
                    />
                  </div>
                </div>

              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="pt-4 border-t border-slate-800 flex justify-end gap-3">
            <button
              type="button"
              @click="handleClose"
              class="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
            >
              Cancelar
            </button>

            <button
              id="submit-species-btn"
              type="submit"
              :disabled="isLoading"
              class="flex items-center gap-2 px-6 py-2.5 rounded-xl text-xs font-bold
                     bg-gradient-to-r from-cyan-500 via-teal-400 to-emerald-500 text-slate-950
                     hover:from-cyan-400 hover:to-emerald-400
                     disabled:opacity-60 disabled:cursor-not-allowed
                     transition-all shadow-lg shadow-cyan-950/40"
            >
              <svg v-if="isLoading" class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
              </svg>
              <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.5v15m7.5-7.5h-15" />
              </svg>
              {{ isLoading ? 'Guardando Especie...' : 'Guardar e Integrar Especie' }}
            </button>
          </div>

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
