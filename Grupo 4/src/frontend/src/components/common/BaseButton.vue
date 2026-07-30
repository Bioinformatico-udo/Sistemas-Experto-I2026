<script setup>
import { computed } from 'vue';

const props = defineProps({
  variant: {
    type: String,
    default: 'primary', // primario, secundario, contorno, peligro
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  type: {
    type: String,
    default: 'button',
  }
});

const baseClasses = 'inline-flex items-center justify-center px-5 py-2.5 rounded-xl font-medium tracking-wide transition-all duration-300 transform active:scale-95 disabled:opacity-50 disabled:pointer-events-none focus:outline-none focus:ring-2 focus:ring-teal-500/50 cursor-pointer';

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'primary':
      return 'bg-gradient-to-r from-cyan-500 to-emerald-500 text-slate-950 font-bold hover:shadow-lg hover:shadow-cyan-500/20 hover:-translate-y-0.5';
    case 'secondary':
      return 'bg-slate-800 text-slate-100 hover:bg-slate-700/80 border border-slate-700 hover:border-slate-600';
    case 'outline':
      return 'bg-transparent text-teal-400 border border-teal-500/30 hover:border-teal-400 hover:bg-teal-400/10';
    case 'danger':
      return 'bg-rose-950/40 text-rose-400 border border-rose-500/30 hover:bg-rose-500 hover:text-white';
    default:
      return 'bg-slate-800 text-slate-100';
  }
});
</script>

<template>
  <button
    :type="type"
    :class="[baseClasses, variantClasses]"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

