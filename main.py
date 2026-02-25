import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

from ataques import fuerza_bruta, estimar_longitud_clave, encontrar_repeticiones, AtaqueFrecuencias, \
    obtener_longitudes_mas_probables
from ataques_modernos import AtaqueFuerzaBruta, AtaqueDiccionarioReglas
from cifrados import Cifrados

st.set_page_config(
    page_title="Simulador de Ataques Criptográficos",
    page_icon="🔐",
    layout="wide"
)

def main():
    st.title("Simulador de Ataques Criptográficos")
    st.markdown(
        """
        ### Microcredencial en Criptografía y Seguridad Digital
        """
    )

    # Sidebar para navegación
    st.sidebar.title("Ataques disponibles")
    opcion = st.sidebar.radio(
        "Selecciona un ataque:",
        ["Inicio", "Ataque a César", "Análisis de Frecuencias", "Ataque Kasiski", "Ataque por fuerza bruta", "Ataque diccionario con reglas"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### Teoría
    - <a href="https://es.wikipedia.org/wiki/Cifrado_C%C3%A9sar" target="_blank">Cifrado César</a>
    - <a href="https://es.wikipedia.org/wiki/Cifrado_por_sustituci%C3%B3n" target="_blank">Cifrado por sustitución</a>
    - <a href="https://es.wikipedia.org/wiki/Cifrado_de_Vigen%C3%A8re" target="_blank">Cifrado de Vigenère</a>
    - <a href="https://es.wikipedia.org/wiki/Ataque_de_fuerza_bruta" target="_blank">Ataque de fuerza bruta</a>
    - <a href="https://es.wikipedia.org/wiki/Ataque_de_diccionario" target="_blank">Ataque de diccionario</a>
    """, unsafe_allow_html=True)

    if opcion == "Inicio":
        mostrar_inicio()
    elif opcion == "Ataque a César":
        mostrar_ataque_cesar()
    elif opcion == "Análisis de Frecuencias":
        mostrar_analisis_frecuencias()
    elif opcion == "Ataque Kasiski":
        mostrar_ataque_kasiski()
    elif opcion == "Ataque por fuerza bruta":
        mostrar_ataque_fuerza_bruta()
    elif opcion == "Ataque diccionario con reglas":
        mostrar_ataque_diccionario_reglas()

def mostrar_inicio():
    st.header("Bienvenido al Simulador")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        ### Ataque a César
        **Fuerza bruta** probando todas las 25 claves posibles.

        *Verás cómo un cifrado simple puede romperse fácilmente.*
        """)

    with col2:
        st.markdown("""
        ### Análisis de Frecuencias
        Compara las frecuencias del texto cifrado con las del español.

        *Las sustituciones simples no ocultan las estadísticas del lenguaje.*
        """)

    with col3:
        st.markdown("""
        ### Ataque Kasiski
        Encuentra repeticiones para estimar la longitud de la clave.

        *El primer paso para romper Vigenère.*
        """)

    with col4:
        st.markdown("""
        ### Ataques Modernos
        **Fuerza bruta a hashes** y **diccionario con reglas**.

        *Simulaciones educativas de ataques reales.*
        """)

    st.markdown("---")
    st.markdown("""
    ### Información adicional
    > Todos los ataques se realizan sobre **ejemplos educativos** creados específicamente
    > para demostrar vulnerabilidades. No se atacan sistemas reales.\n
    > Este simulador demuestra las vulnerabilidades de cifrados clásicos mediante ataques controlados.\n
    > Los ataques modernos usan **hashes débiles (MD5/SHA1)** exclusivamente con fines educativos.
    > Los sistemas reales usan funciones lentas con salt (bcrypt, Argon2).\n
    > Desarrollado con streamlit, por Echeyde Ramos Caballero.
    """)


def mostrar_ataque_cesar():
    st.header("Ataque de Fuerza Bruta a César")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        ### Instrucciones
        1. Introduce un texto (puede ser plano o cifrado)
        2. Si marcas la opción, se cifrará automáticamente
        3. El programa probará las 25 claves
        4. Busca el texto con más sentido entre los resultados

        **¿Cómo funciona?**
        El cifrado César solo tiene 25 claves posibles,
        así que el ataque consiste en probar todas sistemáticamente. Al menos una de ellas resultará
        en el texto plano original.
        """)

        # Opción para aplicar César a texto plano
        aplicar_cesar = st.checkbox(
            "Aplicar cifrado César al texto introducido",
            value=False
        )

        # Si está marcado, permitir elegir la clave de cifrado
        clave_cifrado = 3
        if aplicar_cesar:
            clave_cifrado = st.number_input(
                "Clave de cifrado (desplazamiento):",
                min_value=1,
                max_value=25,
                value=3
            )

        # Texto de ejemplo predefinido
        texto_ejemplo = "Hola mundo, este es un mensaje secreto"

        texto_entrada = st.text_area(
            "Introduce tu texto:",
            value=texto_ejemplo,
            height=150
        )

        # Texto que se usará para el ataque (puede ser el original o el cifrado)
        texto_para_ataque = texto_entrada

        # Si se marcó la opción, cifrar el texto
        if aplicar_cesar and texto_entrada:
            from cifrados import Cifrados
            texto_para_ataque = Cifrados.cifrado_cesar(texto_entrada, clave_cifrado)

        if st.button("Ejecutar ataque", type="primary"):
            with st.spinner("Atacando el cifrado..."):
                time.sleep(1)  # Simular procesamiento
                resultados = fuerza_bruta(texto_para_ataque)

                st.session_state['resultados_cesar'] = resultados
                st.session_state['ataque_ejecutado'] = True
                st.session_state['texto_original'] = texto_entrada
                st.session_state['texto_cifrado'] = texto_para_ataque
                st.session_state['aplico_cifrado'] = aplicar_cesar
                if aplicar_cesar:
                    st.session_state['clave_usada'] = clave_cifrado
                else:
                    del st.session_state['clave_usada']

    with col2:
        # MOSTRAR EL TEXTO CIFRADO SI SE APLICÓ
        if 'texto_cifrado' in st.session_state and st.session_state['aplico_cifrado']:
            st.markdown("### Texto cifrado generado")
            st.info(f"**Texto cifrado:** {st.session_state['texto_cifrado']}")

            if 'clave_usada' in st.session_state:
                st.caption(f"*Cifrado con clave: {st.session_state['clave_usada']}*")

            st.markdown("---")

        if 'ataque_ejecutado' in st.session_state and st.session_state['ataque_ejecutado']:
            resultados = st.session_state['resultados_cesar']

            # Convertir a DataFrame para mejor visualización
            df = pd.DataFrame(resultados)

            # Mostrar tabla con estilo
            st.markdown("### Resultados del ataque (25 claves probadas)")

            # Añadir columna de previsualización
            df['Vista previa'] = df['Texto descifrado']

            st.dataframe(
                df[['Clave', 'Vista previa']],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Clave": st.column_config.NumberColumn("Clave", format="%d", width=50),
                    "Vista previa": st.column_config.TextColumn("Texto", width=600),
                }
            )

            # Marcar el texto más probable
            st.markdown("---")
            st.markdown("### ¿Cuál es el texto correcto?")

            # Verificar si la clave correcta está en los resultados
            if 'clave_usada' in st.session_state:
                clave_correcta = st.session_state['clave_usada']
                texto_descifrado_correcto = df[df['Clave'] == clave_correcta]['Texto descifrado'].values

                if len(texto_descifrado_correcto) > 0:
                    # Comparar con el texto original
                    if 'texto_original' in st.session_state:
                        if texto_descifrado_correcto[0] == st.session_state['texto_original']:
                            st.success(f"**Clave correcta encontrada**")
                            st.markdown(f"**Clave {clave_correcta}:** {texto_descifrado_correcto[0]}")

            else:
                st.info("Dado que no se conoce el texto correcto, comprueba cuál tiene más sentido.")


def mostrar_analisis_frecuencias():
    st.header("Análisis de Frecuencias")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        ### Instrucciones
        1. Introduce un texto cifrado por sustitución
        2. Se calcularán las frecuencias
        3. Compara con las del español

        **¿Cómo funciona?**
        En cualquier idioma, algunas letras son más 
        frecuentes que otras (en español, la 'E' es la más común).
        """)

        # Texto de ejemplo
        texto_ejemplo = "Xl wxlxli qsv jiv uirgmxmsr wiw yrmhsh jvigmirgme"

        texto_cifrado = st.text_area(
            "Texto cifrado:",
            value=texto_ejemplo,
            height=100,
            key="freq_input"
        )

        if st.button("Analizar frecuencias", type="primary"):
            with st.spinner("Calculando frecuencias..."):
                st.session_state['frec_analizado'] = texto_cifrado

    with col2:
        if 'frec_analizado' in st.session_state:
            texto = st.session_state['frec_analizado']

            # Calcular frecuencias
            frecuencias = AtaqueFrecuencias.calcular_frecuencias(texto)

            # Mostrar visualización
            st.markdown("### Comparativa de frecuencias")
            fig = AtaqueFrecuencias.visualizar(texto)
            st.pyplot(fig)
            plt.close()

            # Mostrar tabla de frecuencias
            st.markdown("### Frecuencias detalladas")

            col_a, col_b = st.columns(2)

            with col_a:
                st.markdown("**En texto cifrado:**")
                df_cifrado = pd.DataFrame(
                    list(frecuencias.items())[:10],
                    columns=['Letra', 'Frecuencia (%)']
                )
                st.dataframe(df_cifrado, hide_index=True, use_container_width=True)

            with col_b:
                st.markdown("**En español (estándar):**")
                frec_esp = sorted(
                    AtaqueFrecuencias.FRECUENCIAS_ESPANOL.items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:10]
                df_esp = pd.DataFrame(frec_esp, columns=['Letra', 'Frecuencia (%)'])
                st.dataframe(df_esp, hide_index=True, use_container_width=True)

            # Sugerencias de sustitución
            st.markdown("### Hipótesis de sustitución")

            letras_cifrado = list(frecuencias.keys())
            letras_espanol = list(dict(sorted(
                AtaqueFrecuencias.FRECUENCIAS_ESPANOL.items(),
                key=lambda x: x[1],
                reverse=True
            )).keys())

            hipotesis = []
            for i in range(min(5, len(letras_cifrado), len(letras_espanol))):
                hipotesis.append({
                    'En cifrado': letras_cifrado[i].upper(),
                    'Probablemente es': letras_espanol[i].upper()
                })

            df_hip = pd.DataFrame(hipotesis)
            st.dataframe(df_hip, hide_index=True, use_container_width=True)


def mostrar_ataque_kasiski():
    st.header("Ataque de Kasiski a Vigenère")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        ### Instrucciones
        1. Introduce un texto cifrado con Vigenère
        2. El programa busca secuencias repetidas
        3. Estima la longitud de la clave

        **¿Cómo funciona?**
        Las secuencias repetidas en el texto cifrado 
        suelen estar separadas por múltiplos de la longitud de la clave.
        El ataque consiste en buscar estas repeticiones y sus distancias 
        para obtener todas las posibles longitudes de clave. De entre éstas,
         las más frecuentes son las más probables de ser la clave correcta.
        """)

        # Texto de ejemplo
        texto_ejemplo = "Vzmv yp eesxq alvrq buz wg cekmvp pjvsfe osfz eg xgitj wg cekmvp y oizeo t xgitj euí buz in eesxq de mirttz"

        # Opción para aplicar Vigenère primero a un texto plano
        aplicar_vigenere = st.checkbox("Aplicar cifrado Vigenère a texto plano", value=False)

        texto_cifrado_con_clave = st.text_area(
            "Texto plano a cifrar:" if aplicar_vigenere else "Texto cifrado (Vigenère):",
            value=texto_ejemplo,
            height=150,
            key="kasiski_input"
        )


        clave_vigenere = "clave"
        if aplicar_vigenere:
            clave_vigenere = st.text_input("Clave para cifrar:", value="clave")

        if st.button("Analizar con Kasiski", type="primary"):
            with st.spinner("Analizando repeticiones..."):
                # Aplicar Vigenère si se seleccionó
                if aplicar_vigenere and clave_vigenere:
                    texto_para_analizar = Cifrados.cifrado_vigenere(texto_cifrado_con_clave, clave_vigenere)
                    st.info(f"Texto cifrado con clave '{clave_vigenere}' (longitud {len(clave_vigenere)})")
                else:
                    texto_para_analizar = texto_cifrado_con_clave

                st.session_state['texto_kasiski'] = texto_para_analizar
                st.session_state['clave_usada'] = clave_vigenere if aplicar_vigenere else "desconocida"

    with col2:
        if 'texto_kasiski' in st.session_state:
            texto = st.session_state['texto_kasiski']

            st.markdown("### Análisis de repeticiones")
            st.text(f"Texto a analizar: {texto[:100]}...")

            # Encontrar repeticiones
            repeticiones = encontrar_repeticiones(texto)

            if repeticiones:
                # Mostrar repeticiones encontradas
                datos_rep = []
                for secuencia, distancias in list(repeticiones.items()):
                    datos_rep.append({
                        'Secuencia': secuencia,
                        'Repeticiones': len(distancias),
                        'Distancias': str(set(distancias))[:50]
                    })

                st.markdown("#### Secuencias repetidas:")
                df_rep = pd.DataFrame(datos_rep)
                st.dataframe(df_rep, hide_index=True, use_container_width=True)

                # Estimar longitud de clave
                sugerencias = estimar_longitud_clave(repeticiones)

                if sugerencias:
                    st.markdown("#### Estimación de longitud de clave:")

                    df_sug = pd.DataFrame(
                        sugerencias[:5],
                        columns=['Longitud', 'Frecuencia']
                    )

                    # Crear gráfico de barras
                    fig, ax = plt.subplots(figsize=(10, 4))
                    ax.bar(df_sug['Longitud'].astype(str), df_sug['Frecuencia'],
                           color='lightgreen', edgecolor='darkgreen')
                    ax.set_xlabel('Longitud de clave')
                    ax.set_ylabel('Frecuencia')
                    ax.set_title('Posibles longitudes de clave')
                    ax.grid(axis='y', alpha=0.3)
                    st.pyplot(fig)
                    plt.close()

                    longitudes_probables = obtener_longitudes_mas_probables(sugerencias)

                    if longitudes_probables:
                        longitudes_str = ", ".join(map(str, longitudes_probables))
                        st.success(f"**Longitudes más probables: {longitudes_str}**")
                    else:
                        st.warning("No se pudieron estimar longitudes de clave.")

                    if 'clave_usada' in st.session_state and st.session_state['clave_usada'] != "desconocida":
                        if sugerencias[0][0] == len(st.session_state['clave_usada']):
                            st.success("El ataque acertó la longitud de la clave")
                        else:
                            st.warning(f"La clave real tenía longitud {len(st.session_state['clave_usada'])}")
                else:
                    st.warning("No se pudieron encontrar suficientes repeticiones para estimar la clave.")
            else:
                st.warning("No se encontraron secuencias repetidas significativas.")


def mostrar_ataque_fuerza_bruta():
    st.header("Ataque Moderno: Fuerza Bruta a Hashes")

    st.warning("""
    **AVISO**: Este simulador usa algoritmos de hash débiles (MD5, SHA1) 
    EXCLUSIVAMENTE con fines educativos para demostrar vulnerabilidades.
    Los sistemas reales usan funciones como bcrypt, Argon2 o PBKDF2 con salt.
    """)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("""
        ### ¿Cómo funciona?

        1. Las contraseñas no se guardan en texto plano, sino como **hashes**
        2. Si un atacante roba la base de datos de hashes puede probar miles de contraseñas por segundo
        4. Compara el hash calculado con el robado

        **Este ataque simula ese proceso.**
        """)

        # Seleccionar tipo de análisis
        tipo = st.radio(
            "Selecciona el tipo de análisis:",
            ["Analizar seguridad de una contraseña",
             "Comparar tiempos de ataque",
             "Ver diccionario de contraseñas comunes"],
            key="tipo_ataque_selector"  # Añadir key para identificarlo
        )

        # LIMPIAR ESTADO CUANDO CAMBIA EL TIPO
        if 'tipo_anterior' not in st.session_state:
            st.session_state['tipo_anterior'] = tipo
        elif st.session_state['tipo_anterior'] != tipo:
            # Si cambió el tipo, limpiar los estados
            keys_to_clear = ['analisis_contraseña', 'contraseña_analizada', 'tiempo_calculado']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state['tipo_anterior'] = tipo

        if tipo == "Analizar seguridad de una contraseña":
            contraseña = st.text_input(
                "Introduce una contraseña para analizar:",
                value="MiClave123",
                type="password"
            )

            if st.button("Analizar seguridad", type="primary"):
                with st.spinner("Analizando..."):
                    analisis = AtaqueFuerzaBruta.analizar_seguridad_contraseña(contraseña)
                    st.session_state['analisis_contraseña'] = analisis
                    st.session_state['contraseña_analizada'] = contraseña
                    # Limpiar cualquier resultado de comparación anterior
                    if 'tiempo_calculado' in st.session_state:
                        del st.session_state['tiempo_calculado']

        elif tipo == "Comparar tiempos de ataque":
            st.markdown("""
            ### Configuración para comparativa

            Vamos a comparar cuánto tardaría en romperse una contraseña
            según su complejidad y el poder de cómputo del atacante.
            """)

            col_a, col_b = st.columns(2)

            with col_a:
                longitud = st.slider("Longitud de la contraseña:", 4, 20, 8)
                mayus = st.checkbox("Incluye mayúsculas", True)
                numeros = st.checkbox("Incluye números", True)

            with col_b:
                simbolos = st.checkbox("Incluye símbolos", False)
                escenario = st.selectbox(
                    "Poder del atacante:",
                    ["PC doméstico", "GPU dedicada", "Botnet/Cloud"]
                )

            if st.button("Calcular tiempos", type="primary"):
                velocidad = AtaqueFuerzaBruta.VELOCIDADES[escenario]
                tiempo_str, segundos = AtaqueFuerzaBruta.calcular_tiempo_estimado(
                    longitud, mayus, numeros, simbolos, velocidad
                )

                st.session_state['tiempo_calculado'] = {
                    "tiempo": tiempo_str,
                    "segundos": segundos,
                    "longitud": longitud,
                    "escenario": escenario,
                    "mayus": mayus,
                    "numeros": numeros,
                    "simbolos": simbolos
                }
                # Limpiar cualquier análisis anterior
                if 'analisis_contraseña' in st.session_state:
                    del st.session_state['analisis_contraseña']

        else:  # Ver diccionario
            st.markdown("### Diccionario de contraseñas comunes")
            diccionario = AtaqueFuerzaBruta.generar_diccionario_comun()

            # Mostrar en columnas
            cols = st.columns(3)
            for i, passwd in enumerate(diccionario):
                cols[i % 3].code(passwd)

            st.markdown(f"**Total:** {len(diccionario)} contraseñas comunes")
            # Limpiar estados al ver diccionario
            keys_to_clear = ['analisis_contraseña', 'contraseña_analizada', 'tiempo_calculado']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]

    with col2:
        if 'analisis_contraseña' in st.session_state:
            analisis = st.session_state['analisis_contraseña']
            contraseña = st.session_state['contraseña_analizada']

            st.markdown(f"### Resultados para: `{contraseña}`")

            # Mostrar métricas en un cuadro
            with st.container():
                col_x, col_y = st.columns(2)

                with col_x:
                    st.metric("Longitud", analisis["longitud"])
                    st.metric("¿Es común?", "SÍ" if analisis["es_comun"] else "NO")

                with col_y:
                    st.metric("Fortaleza", analisis["fortaleza"])
                    # Características del conjunto
                    chars = []
                    if analisis["tiene_minusculas"]: chars.append("a-z")
                    if analisis["tiene_mayusculas"]: chars.append("A-Z")
                    if analisis["tiene_numeros"]: chars.append("0-9")
                    if analisis["tiene_simbolos"]: chars.append("!@#$")
                    st.metric("Conjunto", ", ".join(chars) if chars else "Solo letras")

            # Mostrar tiempos
            st.markdown("#### Tiempos estimados para romperla:")
            for escenario, tiempo in analisis["tiempos"].items():
                st.markdown(f"- **{escenario}:** {tiempo}")

            # Intentar visualizar, pero manejar error
            try:
                fig = AtaqueFuerzaBruta.visualizar_comparativa_tiempos(analisis)
                if fig is not None:
                    st.pyplot(fig)
                    plt.close(fig)
                else:
                    st.info("No se pudo generar la gráfica, pero se muestran los datos.")
            except Exception as e:
                st.info("Visualización gráfica no disponible, mostrando solo datos numéricos.")
                # Opcional: log del error para debugging
                print(f"Error en visualización: {e}")

        elif 'tiempo_calculado' in st.session_state:
            calc = st.session_state['tiempo_calculado']

            st.markdown("### Resultado del cálculo")

            # Mostrar resultado en un recuadro destacado
            st.success(f"**Tiempo estimado:** {calc['tiempo']}")

            # Mostrar configuración
            with st.expander("Ver configuración del cálculo", expanded=True):
                st.markdown(f"""
                - **Longitud:** {calc['longitud']} caracteres
                - **Mayúsculas:** {'✅' if calc.get('mayus', True) else '❌'}
                - **Números:** {'✅' if calc.get('numeros', True) else '❌'}
                - **Símbolos:** {'✅' if calc.get('simbolos', False) else '❌'}
                - **Escenario:** {calc['escenario']} 
                - **Velocidad:** {AtaqueFuerzaBruta.VELOCIDADES[calc['escenario']]:.0e} intentos/s
                """)

            # Intentar generar gráfico explicativo
            try:
                fig, ax = plt.subplots(figsize=(10, 5))

                # Calcular tiempos para diferentes longitudes
                longitudes = range(4, 17)
                tiempos = []
                for l in longitudes:
                    _, seg = AtaqueFuerzaBruta.calcular_tiempo_estimado(
                        l,
                        calc.get('mayus', True),
                        calc.get('numeros', True),
                        calc.get('simbolos', False),
                        AtaqueFuerzaBruta.VELOCIDADES[calc['escenario']]
                    )
                    tiempos.append(seg)

                ax.plot(longitudes, tiempos, 'b-o', linewidth=2, markersize=6, label='Tiempo estimado')
                ax.axvline(x=calc['longitud'], color='red', linestyle='--', alpha=0.7, linewidth=2,
                           label=f'Tu contraseña ({calc["longitud"]} chars)')
                ax.set_yscale('log')
                ax.set_xlabel('Longitud de la contraseña', fontsize=12)
                ax.set_ylabel('Tiempo (segundos, escala logarítmica)', fontsize=12)
                ax.set_title('⏰ Crecimiento exponencial del tiempo con la longitud', fontsize=14, fontweight='bold')
                ax.grid(True, alpha=0.3)
                ax.legend()

                # Añadir anotaciones para puntos clave
                for i, (l, t) in enumerate(zip(longitudes, tiempos)):
                    if l in [8, 12, 16]:  # Solo anotar algunas longitudes
                        ax.annotate(f'{t:.0e}s', (l, t), textcoords="offset points",
                                    xytext=(0, 10), ha='center', fontsize=8)

                plt.tight_layout()
                st.pyplot(fig)
                plt.close(fig)

            except Exception as e:
                st.info("ℹ️ No se pudo generar la gráfica comparativa, mostrando solo el resultado numérico.")
                print(f"Error en gráfico comparativo: {e}")


def mostrar_ataque_diccionario_reglas():
    st.header("Ataque Moderno: Diccionario con Reglas")

    st.info("""
    **¿Cómo funciona?** Los atacantes no prueban solo palabras del diccionario,
    sino que aplican **reglas de mutación** para generar variaciones inteligentes.

    Ejemplo: "password" → "Password", "PASSWORD", "password123", "p4ssw0rd", etc.
    """)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Configuración")

        # Palabras base
        palabras_base = ["admin", "password", "user", "clave", "secret",
                         "pass", "key", "login", "system", "root",
                         "master", "test", "demo", "guest", "hola"]

        # Opciones
        tipo_demo = st.radio(
            "Selecciona demostración:",
            ["Ver reglas aplicadas", "Simular ataque a contraseña"],
            key="tipo_demo_selector"  # Añadir key para identificarlo
        )

        # LIMPIAR ESTADO CUANDO CAMBIA EL TIPO
        if 'tipo_demo_anterior' not in st.session_state:
            st.session_state['tipo_demo_anterior'] = tipo_demo
        elif st.session_state['tipo_demo_anterior'] != tipo_demo:
            # Si cambió el tipo, limpiar los estados
            keys_to_clear = ['variaciones', 'palabra_base', 'resultado_reglas',
                            'dicc_completo', 'reglas_aplicadas', 'objetivo']
            for key in keys_to_clear:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state['tipo_demo_anterior'] = tipo_demo

        if tipo_demo == "Ver reglas aplicadas":
            palabra_ejemplo = st.selectbox("Palabra base:", palabras_base[:5])

            if st.button("Generar variaciones", type="primary"):
                variaciones = AtaqueDiccionarioReglas.aplicar_reglas(palabra_ejemplo)
                st.session_state['variaciones'] = variaciones
                st.session_state['palabra_base'] = palabra_ejemplo
                # Limpiar resultados de ataque anteriores
                keys_to_clear = ['resultado_reglas', 'dicc_completo', 'reglas_aplicadas', 'objetivo']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]

        else:  # Simular ataque
            st.markdown("#### Objetivo del ataque")

            # Opciones de contraseña objetivo
            opcion_objetivo = st.radio(
                "Elige contraseña objetivo:",
                ["Usar ejemplo predefinido", "Personalizar"]
            )

            if opcion_objetivo == "Usar ejemplo predefinido":
                objetivo = st.selectbox(
                    "Contraseña a 'atacar':",
                    ["Password123", "admin!", "SECRET", "p4ssw0rd", "clave2024",
                     "monkey", "qwerty123", "teamo!", "123456"]
                )
            else:
                objetivo = st.text_input(
                    "Introduce contraseña personalizada:",
                    value="MiClave123",
                    type="password"
                )

            if st.button("Simular ataque", type="primary"):
                with st.spinner("Aplicando reglas y buscando..."):
                    resultado = AtaqueDiccionarioReglas.simular_ataque(objetivo, palabras_base)

                    # Generar estadísticas
                    dicc_completo, reglas_aplicadas = AtaqueDiccionarioReglas.generar_diccionario_con_reglas(
                        palabras_base)

                    st.session_state['resultado_reglas'] = resultado
                    st.session_state['dicc_completo'] = dicc_completo
                    st.session_state['reglas_aplicadas'] = reglas_aplicadas
                    st.session_state['objetivo'] = objetivo
                    # Limpiar variaciones anteriores
                    keys_to_clear = ['variaciones', 'palabra_base']
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]

    with col2:
        if 'variaciones' in st.session_state:
            st.markdown(f"### Variaciones de '{st.session_state['palabra_base']}'")

            variaciones = st.session_state['variaciones']

            # Mostrar en columnas
            cols = st.columns(2)
            for i, var in enumerate(variaciones[:20]):  # Mostrar primeras 20
                cols[i % 2].code(var)

            st.markdown(f"**Total generadas:** {len(variaciones)} variaciones")

            # Explicación de reglas
            with st.expander("Ver reglas aplicadas"):
                st.markdown("""
                **Reglas comunes:**
                - Palabra original
                - Capitalizar primera letra
                - TODO MAYÚSCULAS
                - Añadir números (123, 2024, etc.)
                - Duplicar palabra
                - Invertir palabra
                - Leet speak (a→4, e→3, i→1, o→0, s→5)
                - Añadir símbolos (!, @, #, etc.)
                """)

        elif 'resultado_reglas' in st.session_state:
            resultado = st.session_state['resultado_reglas']
            objetivo = st.session_state['objetivo']
            dicc_completo = st.session_state['dicc_completo']

            st.markdown(f"### Resultado del ataque")
            st.markdown(f"**Objetivo:** `{objetivo}`")

            if resultado["encontrada"]:
                st.success("**¡CONTRASEÑA ENCONTRADA!**")

                st.markdown(f"""
                - **Palabra base:** `{resultado['palabra_base']}`
                - **Regla aplicada:** {resultado['regla']}
                - **Intentos necesarios:** {resultado['intentos']:,}
                """)

                # Mostrar eficiencia
                eficiencia = (resultado['intentos'] / len(dicc_completo)) * 100
                st.progress(eficiencia / 100)
                st.caption(f"Recorrido el {eficiencia:.1f}% del diccionario")

            else:
                st.error("❌ **No se encontró la contraseña**")
                st.markdown(f"""
                - **Intentos realizados:** {resultado['intentos']:,}
                - **Tamaño del diccionario:** {len(dicc_completo):,} palabras

                **Posibles razones:**
                - La contraseña no sigue patrones comunes
                - Es demasiado larga o compleja
                - Usa reglas no incluidas en este simulador
                """)

            # Visualizar estadísticas
            if 'reglas_aplicadas' in st.session_state:
                st.markdown("### Estadísticas del diccionario")
                fig = AtaqueDiccionarioReglas.visualizar_estadisticas(st.session_state['reglas_aplicadas'])
                st.pyplot(fig)
                plt.close()

                total_variaciones = sum(st.session_state['reglas_aplicadas'].values())
                st.metric("Total variaciones generadas", f"{total_variaciones:,}")

            if st.button("Nuevo ataque"):
                keys = ['resultado_reglas', 'dicc_completo', 'reglas_aplicadas', 'objetivo']
                for k in keys:
                    if k in st.session_state:
                        del st.session_state[k]
                st.rerun()


if __name__ == "__main__":
    main()