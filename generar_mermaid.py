# generar_mermaid.py
"""
Este script genera el archivo estructura_proyecto.md con un diagrama Mermaid de ejemplo.
"""

contenido_mermaid = """
graph TD
    A[Inicio] --> B[Recolección de Datos]
    B --> C[Procesamiento de Datos]
    C --> D[Entrenamiento de Modelos]
    D --> E[Evaluación de Modelos]
    E --> F[Despliegue en Producción]
    F --> G[Visualización de Resultados]
    G --> H[Monitoreo]
    H --> I[Fin]
"""

# Guardar en archivo
with open("estructura_proyecto.md", "w", encoding="utf-8") as f:
    f.write(contenido_mermaid)

print("✅ Diagrama Mermaid generado exitosamente en 'estructura_proyecto.md'")
