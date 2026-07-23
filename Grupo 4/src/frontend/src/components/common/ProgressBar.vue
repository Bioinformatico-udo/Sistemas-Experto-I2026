<script setup>
defineProps({
  progress: {
    type: Number,
    required: true,
  }
});
</script>

<template>
  <div class="w-full">
    <div class="flex justify-between items-center mb-2">
      <span class="text-xs font-semibold uppercase tracking-wider text-teal-400">Progreso Estimado</span>
      <span class="text-xs font-mono font-bold text-slate-300">{{ progress }}%</span>
    </div>
    <div class="w-full h-2.5 bg-slate-900 rounded-full overflow-hidden border border-slate-800">
      <div
        class="h-full bg-gradient-to-r from-cyan-500 to-emerald-500 rounded-full transition-all duration-500 ease-out"
        :style="{ width: `${progress}%` }"
      ></div>
    </div>
  </div>
</template>
