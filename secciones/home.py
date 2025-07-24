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
        Desde la firma del Acuerdo de París en 2015, la transición energética se ha convertido en un pilar fundamental de los esfuerzos globales para hacer frente a la crisis climática. En este acuerdo, 196 países —incluida Colombia— se comprometieron a evitar que el aumento de la temperatura global supere los 2 °C respecto a los niveles preindustriales, con el objetivo de limitarlo a 1,5 °C. Como consecuencia, más de 100 naciones, responsables de aproximadamente dos tercios de las emisiones globales y del PIB mundial, han establecido metas para alcanzar la carbono neutralidad hacia 2050 o en fechas cercanas.

        Colombia, en consonancia con estos compromisos internacionales, ha definido una hoja de ruta para transformar su matriz energética. Este proceso se sustenta en políticas públicas clave como el Plan Energético Nacional, la Estrategia 2050 y la Misión de Transformación Energética.""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Problemática
    with st.expander("📌 1. DESCRIPCIÓN DE LA PROBLEMÁTICA"):
        st.markdown('<div class="intro-text">', unsafe_allow_html=True)
        st.markdown("""
        Colombia se encuentra en una etapa decisiva de su transición energética, impulsando cada vez más el uso de fuentes limpias como la solar, eólica, hidroeléctrica, biomasa y, más recientemente, el hidrógeno verde.

        Un diagnóstico inicial reveló una marcada dependencia de la energía hidroeléctrica: al cierre de 2018, el 68,3 % de la capacidad instalada provenía de esta fuente, seguida por un 30,7 % de generación térmica. En contraste, las fuentes solar y eólica apenas representaban el 0,8 %, mientras que el bagazo contribuía con solo el 0,2 %.

        Si bien se han registrado avances, la participación de energías renovables no convencionales continúa siendo limitada. En este contexto, es fundamental que la transición energética sea justa, garantizando beneficios para todos los sectores de la sociedad, en especial para las comunidades más vulnerables.

        Asimismo, resulta clave contar con información clara, accesible y actualizada que oriente la toma de decisiones. Comprender la evolución del sistema energético —diferenciando entre fuentes renovables y no renovables— permite identificar obstáculos, logros alcanzados y oportunidades de mejora. """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Objetivos
    with st.expander("🎯 2. OBJETIVO PRINCIPAL Y ESPECÍFICOS"):
        st.markdown('<div class="intro-text">', unsafe_allow_html=True)
        st.markdown("""
        Objetivo General
        Documentar y analizar el progreso de Colombia en su transición energética hacia fuentes renovables —como la solar, eólica, hidroeléctrica, biomasa e hidrógeno verde— en concordancia con los compromisos nacionales e internacionales de mitigación del cambio climático y reducción de emisiones de gases de efecto invernadero.
        <ul>
            <li>Cuantificar la evolución del aporte de cada fuente renovable en la matriz energética nacional durante el período 2000–2025, identificando tendencias, brechas y puntos críticos en su desarrollo..</li>
            <li>Comparar el desempeño energético de Colombia con otros países de América Latina y referentes globales, evaluando su posición relativa en términos de diversificación, sostenibilidad y penetración de energías limpias.</li>
            <li>Formular recomendaciones estratégicas orientadas a acelerar una transición energética justa, inclusiva y sostenible, con énfasis en el cierre de brechas sociales, territoriales y tecnológicas.</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Conclusiones
    with st.expander("📘 7. CONCLUSIONES"):
        st.markdown('<div class="intro-text">', unsafe_allow_html=True)
        st.markdown("""
        <strong>Resumen de hallazgos:</strong>
        <ul>
            <li>Colombia ha registrado avances importantes en la generación de energía renovable, especialmente en el aprovechamiento de fuentes hidroeléctricas. Sin embargo, la alta dependencia de esta única fuente limita la resiliencia y flexibilidad del sistema energético nacional.</li>
            <li>La electrificación de sectores estratégicos como el transporte y la industria aún es insuficiente, lo que ralentiza la descarbonización integral del país.</li>
            <li>Persisten brechas regionales, tecnológicas y sociales que dificultan una transición energética equitativa y sostenible.</li>
            <li>Aunque el marco institucional y financiero ha mostrado avances, aún requiere fortalecimiento y mayor articulación intersectorial para lograr una implementación efectiva y coherente.</li>
            
        </ul>

        <strong>Respuestas frente a la problemática:</strong>
        <ul>
            <li>Profundizar en el análisis de la evolución de la generación y el consumo energético, diferenciando fuentes y sectores.</li>
            <li>Promover la toma de decisiones estratégicas basadas en datos confiables, actualizados y accesibles.</li>
            <li>Fomentar la articulación efectiva entre políticas públicas, inversión privada y participación ciudadana para acelerar la transformación del sistema energético.</li>
            
        </ul>

        <strong>Implicaciones:</strong>
        <ul>
            <li>Existe el riesgo de que Colombia no logre cumplir sus compromisos climáticos a nivel nacional e internacional.</li>
            <li>Se mantendrían condiciones de vulnerabilidad energética y desigualdad social en distintas regiones del país.</li>
            <li>El país podría perder su oportunidad de consolidarse como líder regional en la transición energética en América Latina.</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recomendaciones
    with st.expander("💡 8. RECOMENDACIONES"):
        st.markdown('<div class="intro-text">', unsafe_allow_html=True)
        st.markdown("""
        <strong>Acciones sugeridas:</strong>
        <ul>
            <li>Acelerar la implementación de proyectos solares y eólicos, con especial énfasis en regiones estratégicas como La Guajira.</li>
            <li>Fomentar la movilidad eléctrica y promover medidas de eficiencia energética en todos los sectores productivos.</li>
            <li>Optimizar la gestión del recurso hídrico e impulsar el desarrollo de infraestructura de almacenamiento energético.</li>
            <li>Diseñar e implementar políticas para la eliminación progresiva del uso de carbón como fuente energética.</li>
            <li>Fortalecer las Contribuciones Determinadas a Nivel Nacional (NDC) y activar mecanismos para captar financiamiento climático internacional.</li>
        </ul>

        <strong>Siguientes pasos:</strong>
        <ul>
            <li>Actualizar y ampliar los datos de generación y consumo energético hasta el año 2025.</li>
            <li>Profundizar el análisis sectorial, diferenciando dinámicas y desafíos por industria, región y tipo de usuario.</li>
            <li>Consolidar alianzas público-privadas que faciliten inversión, innovación y transferencia tecnológica.</li>
            <li>Diseñar campañas de educación y cultura energética, orientadas a la ciudadanía y a tomadores de decisiones.

        </li>
        </ul>

        <strong>Ideas para futuros análisis:</strong>
        <ul>
            <li>Desarrollo de modelos predictivos mediante inteligencia artificial para proyectar escenarios de transición.</li>
            <li>Realización de análisis comparativos internacionales con enfoque cualitativo y contextual.</li>
            <li>Evaluación de los impactos sociales y territoriales de la transición energética.</li>
            <li>Estudio del ciclo de vida completo de las tecnologías de energía renovable.</li>
        </ul>

        <strong>Implicaciones:</strong>
        <ul>
            <li>Aumento de la vulnerabilidad energética debido a la falta de diversificación en la matriz.</li>
            <li>Riesgo de incumplimiento de las metas climáticas para 2030 si no se acelera el ritmo de implementación.</li>
            <li>Limitaciones técnicas y operativas para integrar energías renovables sin infraestructura adecuada.</li>
            <li>Pérdida de efectividad en las políticas si no se establece un sistema de monitoreo y evaluación continuo.</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

