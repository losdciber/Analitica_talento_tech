import os

def generar_mermaid(path_proyecto, archivo_salida="estructura_proyecto.md"):
    mermaid = ["```mermaid", "graph TD"]
    nodos = set()
    conexiones = []

    def agregar_nodos(ruta_base, padre="ROOT"):
        for item in os.listdir(ruta_base):
            item_path = os.path.join(ruta_base, item)
            if item.startswith("."):  # Ignorar archivos ocultos
                continue
            nodo_id = item_path.replace("\\", "_").replace("/", "_").replace(" ", "_")
            nodos.add(f'{nodo_id}["{item}"]')
            if padre != "ROOT":
                padre_id = ruta_base.replace("\\", "_").replace("/", "_").replace(" ", "_")
                conexiones.append(f"{padre_id} --> {nodo_id}")
            else:
                conexiones.append(f"A[Analitica_talento_tech] --> {nodo_id}")

            if os.path.isdir(item_path):
                agregar_nodos(item_path, item_path)

    mermaid.append('A[Analitica_talento_tech]')
    agregar_nodos(path_proyecto)

    mermaid.extend(sorted(nodos))
    mermaid.extend(conexiones)
    mermaid.append("```")

    with open(os.path.join(path_proyecto, archivo_salida), "w", encoding="utf-8") as f:
        f.write("# Estructura del Proyecto\n\n")
        f.write("\n".join(mermaid))

    print(f"✅ Diagrama generado en {archivo_salida}")

# Usa el path actual o cámbialo según lo necesites
if __name__ == "__main__":
    generar_mermaid(".")
