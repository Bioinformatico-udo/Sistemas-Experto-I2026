import uvicorn
import os
import sys

if __name__ == "__main__":
    print("=" * 60)
    print("🪸 CORAL EXPERT SYSTEM - SERVIDOR UNIFICADO (FASTAPI + REACT)")
    print("=" * 60)
    print("🚀 Iniciando servidor FastAPI...")
    print("🌐 Interfaz Web (React): http://localhost:8000")
    print("📚 Documentación API (Swagger): http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)
