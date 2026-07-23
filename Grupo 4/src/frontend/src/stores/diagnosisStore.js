import { defineStore } from 'pinia';
import { runInference, getQuestions, getRules } from '../services/api';

export const useDiagnosisStore = defineStore('diagnosis', {
  state: () => ({
    questions: [],
    rules: [],
    workingMemory: {},
    historyStack: [],
    firedRules: [],
    detectedSpecies: null,
    nextRecommendedFact: null,
    loading: false,
    error: null,
    currentStepIndex: 0,
  }),

  getters: {
    // Busca la pregunta correspondiente al siguiente hecho recomendado
    currentQuestion(state) {
      if (!state.nextRecommendedFact) return null;
      return state.questions.find(q => q.fact === state.nextRecommendedFact) || null;
    },
    // Calcula el progreso en porcentaje aproximado
    progressPercentage(state) {
      if (state.detectedSpecies) return 100;
      if (state.questions.length === 0) return 0;
      
      const answeredCount = Object.keys(state.workingMemory).length;
      // Estima el progreso como el ratio de preguntas respondidas respecto a las totales (máx 90% antes del resultado final)
      const ratio = answeredCount / state.questions.length;
      return Math.min(Math.round(ratio * 100), 95);
    },
    // Verifica si la pila de historial está vacía para deshabilitar el botón de retroceso
    canGoBack(state) {
      return state.historyStack.length > 0;
    },
    // Obtiene los detalles de las reglas disparadas cronológicamente
    firedRulesDetails(state) {
      return state.firedRules
        .map(id => state.rules.find(r => r.id === id))
        .filter(Boolean);
    }
  },

  actions: {
    // Carga inicial del catálogo de preguntas y reglas
    async loadQuestions() {
      this.loading = true;
      this.error = null;
      try {
        const [questions, rules] = await Promise.all([getQuestions(), getRules()]);
        this.questions = questions;
        this.rules = rules;
      } catch (err) {
        this.error = err.message || 'Error al cargar las preguntas y reglas';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    // Inicia un nuevo diagnóstico reseteando los estados
    async startNewDiagnosis() {
      this.workingMemory = {};
      this.historyStack = [];
      this.firedRules = [];
      this.detectedSpecies = null;
      this.nextRecommendedFact = null;
      this.currentStepIndex = 0;
      this.error = null;
      
      // Primera llamada de inferencia con memoria vacía
      await this.submitAnswer();
    },

    // Envía la memoria de trabajo actual al motor del backend y actualiza los resultados
    async submitAnswer() {
      this.loading = true;
      this.error = null;
      try {
        const result = await runInference(this.workingMemory);
        
        // Sincronizar memoria (FastAPI aplica las reglas y puede inferir nuevos hechos)
        this.workingMemory = result.working_memory;
        this.firedRules = result.fired_rules;
        this.detectedSpecies = result.detected_species;
        this.nextRecommendedFact = result.next_recommended_fact;
      } catch (err) {
        this.error = err.message || 'Error en la inferencia';
        console.error(err);
      } finally {
        this.loading = false;
      }
    },

    // Guarda una respuesta para el hecho actual y avanza a la siguiente inferencia
    async answerQuestion(factName, value) {
      // Guardar el estado actual en la pila de historial para permitir retroceder
      this.historyStack.push(JSON.parse(JSON.stringify(this.workingMemory)));
      
      // Asignar el nuevo hecho
      this.workingMemory[factName] = value;
      this.currentStepIndex++;
      
      // Consultar el motor con la memoria actualizada
      await this.submitAnswer();
    },

    // Retrocede a la pregunta anterior restaurando el estado previo de la memoria
    async goBack() {
      if (!this.canGoBack) return;
      
      this.loading = true;
      const previousState = this.historyStack.pop();
      this.workingMemory = previousState;
      this.currentStepIndex = Math.max(0, this.currentStepIndex - 1);
      
      // Volver a consultar al motor para sincronizar firedRules y next_recommended_fact
      await this.submitAnswer();
    }
  }
});
