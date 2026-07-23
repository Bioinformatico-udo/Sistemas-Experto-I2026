const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export async function runInference(workingMemory) {
  const response = await fetch(`${API_BASE}/infer`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(workingMemory),
  });
  if (!response.ok) {
    throw new Error('Error al ejecutar la inferencia en el motor experto');
  }
  return response.json();
}

export async function getQuestions() {
  const response = await fetch(`${API_BASE}/questions`);
  if (!response.ok) {
    throw new Error('Error al obtener la lista de preguntas del backend');
  }
  return response.json();
}

export async function getRules() {
  const response = await fetch(`${API_BASE}/rules`);
  if (!response.ok) {
    throw new Error('Error al obtener el listado de reglas del backend');
  }
  return response.json();
}
