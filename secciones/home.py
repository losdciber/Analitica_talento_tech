import streamlit as st

def mostrar():
    # CSS
    st.markdown("""
        <style>
        .centered-title {
            font-size: 2.6em;
            font-weight: bold;
            color: #2C3E50;
            margin-top: 0.3em;
        }
        .intro-text {
            text-align: justify;
            font-size: 1.1em;
            line-height: 1.7;
            color: #333;
            background-color: #f9f9f9;
            padding: 1.5em;
            border-radius: 10px;
        }
        .section-header {
            font-size: 1.3em;
            font-weight: 700;
            color: #1F4E79;
        }
        summary {
            font-size: 1.2em !important;
            font-weight: bold !important;
            color: #1F4E79 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Encabezado principal
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown('<div class="centered-title">TRANSICIÓN ENERGÉTICA</div>', unsafe_allow_html=True)
    with col2:
        st.image("imagenes/LogoBancolombia.png", width=120)

    # Introducción
    with st.expander("📖 INTRODUCCIÓN"):
        st.markdown('<div class="intro-text">', unsafe_allow_html=True)
        st.markdown("""
        Desde la adopción del Acuerdo de París en 2015, la transición energética se ha consolidado como un eje central de los esfuerzos globales para enfrentar la crisis climática. En dicho acuerdo, 196 países, entre ellos Colombia, se comprometieron a evitar que el aumento de la temperatura global supere los 2 °C respecto a los niveles preindustriales, procurando limitarlo a 1,5 °C. Como resultado, más de 100 naciones, responsables de cerca de dos tercios de las emisiones globales y del PIB mundial, han fijado metas de carbono neutralidad para el año 2050 o poco después.

        Colombia no ha sido ajena a este compromiso. Con un enfoque alineado a las metas climáticas internacionales, el país ha trazado una hoja de ruta para transformar su matriz energética mediante políticas públicas como el Plan Energético Nacional, la Estrategia 2050 y la Misión de Transformación Energética.
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Problemática
    with st.expander("📌 1. DESCRIPCIÓN DE LA PROBLEMÁTICA"):
        st.markdown('<div class="intro-text">', unsafe_allow_html=True)
        st.markdown("""
        Colombia atraviesa una etapa crucial en su transición energética. El país ha comenzado a apostar por un mayor uso de energías limpias como la solar, eólica, hidroeléctrica, biomasa y, más recientemente, el hidrógeno verde.

        Un diagnóstico inicial evidenció una alta concentración en fuentes hidroeléctricas: al cierre de 2018, el 68,3 % de la capacidad instalada provenía del agua, seguida por un 30,7 % de térmicas, y una participación marginal de apenas 0,8 % de solar y eólica, y 0,2 % de bagazo.

        Aunque ha habido avances, la incorporación de energías renovables no convencionales sigue siendo limitada. Además, la transición debe ser justa, lo que implica beneficios para todos los sectores sociales, especialmente comunidades vulnerables.

        También es clave contar con información clara, accesible y actualizada que oriente estas decisiones. Comprender la evolución del sistema energético —diferenciando entre fuentes renovables y no renovables— permite identificar barreras, logros y oportunidades.
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Objetivos
    with st.expander("🎯 2. OBJETIVO PRINCIPAL Y ESPECÍFICOS"):
        st.markdown('<div class="intro-text">', unsafe_allow_html=True)
        st.markdown("""
        Documentar y analizar el avance de Colombia en su transición energética hacia fuentes renovables (solar, eólica, hidroeléctrica, biomasa e hidrógeno verde), en línea con sus compromisos nacionales e internacionales de reducción de emisiones.

        <ul>
            <li>Medir cuantitativamente la evolución del aporte de cada fuente renovable en la matriz energética nacional (2000–2025).</li>
            <li>Comparar el desempeño energético de Colombia con países latinoamericanos y globales.</li>
            <li>Proponer recomendaciones estratégicas para acelerar la transición energética justa.</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Conclusiones
    with st.expander("📘 7. CONCLUSIONES"):
        st.markdown('<div class="intro-text">', unsafe_allow_html=True)
        st.markdown("""
        <strong>Resumen de hallazgos:</strong>
        <ul>
            <li>Colombia ha logrado avances significativos en generación renovable, especialmente hidroeléctrica, pero su dependencia de una sola fuente limita la resiliencia del sistema.</li>
            <li>La electrificación de sectores clave como el transporte y la industria sigue siendo insuficiente.</li>
            <li>Existen brechas regionales, tecnológicas y sociales que afectan la equidad en la transición energética.</li>
            <li>El marco institucional y financiero está en desarrollo, pero requiere consolidación y mayor coherencia intersectorial.</li>
        </ul>

        <strong>Respuestas frente a la problemática:</strong>
        <ul>
            <li>Comprender mejor cómo evoluciona la generación y el consumo de energía.</li>
            <li>Tomar decisiones estratégicas basadas en datos.</li>
            <li>Articular políticas públicas, inversión privada y participación ciudadana.</li>
        </ul>

        <strong>Implicaciones:</strong>
        <ul>
            <li>Colombia podría no cumplir con sus compromisos climáticos.</li>
            <li>Persistiría la vulnerabilidad energética y brechas sociales.</li>
            <li>Se desaprovecharía su liderazgo en América Latina.</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recomendaciones
    with st.expander("💡 8. RECOMENDACIONES"):
        st.markdown('<div class="intro-text">', unsafe_allow_html=True)
        st.markdown("""
        <strong>Acciones sugeridas:</strong>
        <ul>
            <li>Acelerar proyectos solares y eólicos, especialmente en La Guajira.</li>
            <li>Impulsar movilidad eléctrica y eficiencia energética.</li>
            <li>Optimizar gestión hídrica y desarrollar infraestructura de almacenamiento.</li>
            <li>Diseñar políticas para eliminar progresivamente el carbón.</li>
            <li>Fortalecer los NDC y captar financiamiento climático internacional.</li>
        </ul>

        <strong>Siguientes pasos:</strong>
        <ul>
            <li>Actualizar datos hasta 2025.</li>
            <li>Profundizar análisis por sectores.</li>
            <li>Consolidar alianzas público-privadas.</li>
            <li>Implementar campañas de educación y cultura energética.</li>
        </ul>

        <strong>Ideas para futuros análisis:</strong>
        <ul>
            <li>Modelos predictivos con IA.</li>
            <li>Comparativos internacionales con enfoque cualitativo.</li>
            <li>Evaluar impactos sociales y territoriales.</li>
            <li>Análisis de ciclo de vida completo de energías renovables.</li>
        </ul>

        <strong>Implicaciones:</strong>
        <ul>
            <li>Mayor vulnerabilidad energética por falta de diversificación.</li>
            <li>Compromiso de metas al 2030 si no se acelera la acción.</li>
            <li>Limitaciones para integrar renovables sin infraestructura adecuada.</li>
            <li>Riesgo de diluir esfuerzos sin monitoreo constante.</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

