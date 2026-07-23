<script setup>
import { ref } from 'vue';
import { useDiagnosisStore } from '../../stores/diagnosisStore';

const store = useDiagnosisStore();
const isOpen = ref(true);

const togglePanel = () => {
  isOpen.value = !isOpen.value;
};
</script>

<template>
  <div class="w-full bg-slate-900/40 border border-slate-800 rounded-2xl overflow-hidden mt-6 shadow-lg">
    <!-- Cabecera del Panel (Clic para colapsar/expandir) -->
    <button
      @click="togglePanel"
      class="w-full px-6 py-4 flex items-center justify-between bg-slate-900/60 hover:bg-slate-900/80 transition-colors text-left cursor-pointer"
    >
      <div class="flex items-center gap-3">
        <!-- Icono de Red Neuronal / Traza SVG -->
        <svg class="w-5 h-5 text-teal-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
        </svg>
        <span class="font-display font-semibold text-slate-200">Panel de Explicabilidad (Trazas Lógicas)</span>
      </div>
      
      <!-- Flecha dinámica -->
      <svg
        :class="['w-5 h-5 text-slate-400 transition-transform duration-300', isOpen ? 'rotate-180' : '']"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
      </svg>
    </button>

    <!-- Cuerpo del Panel -->
    <div v-show="isOpen" class="p-6 border-t border-slate-800/50 bg-slate-950/30">
      <div v-if="store.firedRulesDetails.length === 0" class="text-sm text-slate-500 italic text-center py-4">
        Ninguna regla del motor se ha disparado aún.
      </div>
      
      <div v-else class="space-y-4 relative before:absolute before:top-2 before:bottom-2 before:left-[17px] before:w-0.5 before:bg-slate-800/80">
        <!-- Renderizar cada regla disparada -->
        <div
          v-for="(rule, idx) in store.firedRulesDetails"
          :key="rule.id"
          class="flex gap-4 relative group"
        >
          <!-- Indicador visual cronológico -->
          <div class="relative z-10 w-9 h-9 rounded-full bg-slate-900 border border-slate-700 flex items-center justify-center font-mono font-bold text-xs text-teal-400 group-hover:border-teal-400 transition-colors shadow">
            {{ idx + 1 }}
          </div>

          <!-- Contenido de la regla -->
          <div class="flex-1 bg-slate-900/30 rounded-xl p-4 border border-slate-800/50 group-hover:border-slate-800 transition-colors">
            <div class="flex justify-between items-start gap-4 mb-2">
              <h4 class="font-semibold text-sm text-slate-200">{{ rule.name }}</h4>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-teal-400 uppercase tracking-wider">
                {{ rule.id }}
              </span>
            </div>
            
            <p class="text-xs text-slate-400 leading-relaxed mb-3">
              {{ rule.description }}
            </p>

            <!-- Detalles de Antecedentes y Consecuentes -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs bg-slate-950/40 rounded-lg p-2.5 border border-slate-800/30">
              <!-- Antecedentes (SI) -->
              <div>
                <span class="font-bold text-[10px] text-cyan-400 uppercase tracking-wider block mb-1">Si se cumple:</span>
                <ul class="space-y-1 text-slate-300">
                  <li v-for="ant in rule.antecedents" :key="ant.fact" class="flex gap-1.5 font-mono text-[11px] items-center">
                    <span class="text-slate-400">{{ ant.fact }}</span>
                    <span class="text-teal-400 font-bold">{{ ant.operator }}</span>
                    <span class="text-emerald-400">{{ ant.value }}</span>
                  </li>
                </ul>
              </div>

              <!-- Consecuentes (ENTONCES) -->
              <div>
                <span class="font-bold text-[10px] text-emerald-400 uppercase tracking-wider block mb-1">Entonces deducir:</span>
                <ul class="space-y-1 text-slate-300">
                  <li v-for="con in rule.consequents" :key="con.fact" class="flex gap-1.5 font-mono text-[11px] items-center">
                    <span class="text-slate-400">{{ con.fact }}</span>
                    <span class="text-emerald-400">=</span>
                    <span class="text-teal-400 font-bold">{{ con.value }}</span>
                  </li>
                </ul>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  </div>
</template>
