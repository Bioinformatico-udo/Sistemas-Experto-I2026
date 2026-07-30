<script setup>
import { ref } from 'vue';
import DeveloperCard from './DeveloperCard.vue';

const developers = ref([
  {
    name: 'Jesús Rodríguez',
    role: 'Lead Backend & Inferencia',
    description: 'Especialista en Inteligencia Artificial y modelado de bases de conocimiento bajo Arquitectura Hexagonal.',
    github: 'https://github.com/Ezuchu',
    portfolio: 'https://v0-portafolio-e5aivyax2-jesusmiguelrr17-8978s-projects.vercel.app/',
    photo: '' 
  },
  {
    name: 'Wilmer Moreno',
    role: 'UI/UX & Frontend Dev',
    description: 'Diseñador de interfaces reactivas y animaciones interactivas inspiradas en el concepto Oceanic Deep-Tech.',
    github: 'https://github.com/wilmermor',
    portfolio: 'https://wilmer-rho.vercel.app/',
    photo: ''
  },
  {
    name: 'Alejandra Méndez',
    role: 'Ingeniero del Conocimiento',
    description: 'Responsable del levantamiento de reglas taxonómicas y estructuración del motor de inferencia.',
    github: 'https://github.com/alemen-08',
    portfolio: '#',
    photo: ''
  }
]);
</script>

<template>
  <div class="w-full">
    <div class="text-center mb-8">
      <h2 class="font-display font-bold text-2xl text-slate-100">Ingenieros del Conocimiento</h2>
      <p class="text-sm text-slate-400 mt-2 max-w-lg mx-auto">
        Equipo multidisciplinario del Grupo 4 responsable del modelado ontológico y desarrollo del sistema experto.
      </p>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <DeveloperCard
        v-for="dev in developers"
        :key="dev.name"
        :developer="dev"
      />
    </div>
  </div>
</template>
