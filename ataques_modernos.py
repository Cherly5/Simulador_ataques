import hashlib
import matplotlib.pyplot as plt

class AtaqueFuerzaBruta:
    """
    Simulador de ataque de fuerza bruta a hashes de contraseñas
    """

    # Velocidades de ataque para diferentes escenarios (intentos/segundo)
    VELOCIDADES = {
        "PC doméstico": 1_000_000,  # 1 millón
        "GPU dedicada": 1_000_000_000,  # 1 mil millones
        "Botnet/Cloud": 1_000_000_000_000,  # 1 billón
    }

    @staticmethod
    def hash_password(contraseña, metodo="md5"):
        """
        Genera el hash de una contraseña
        ADVERTENCIA: MD5 y SHA1 son inseguros, se usan SOLO con fines educativos
        """
        contraseña_bytes = contraseña.encode('utf-8')

        if metodo == "md5":
            return hashlib.md5(contraseña_bytes).hexdigest()
        elif metodo == "sha1":
            return hashlib.sha1(contraseña_bytes).hexdigest()
        elif metodo == "sha256":
            return hashlib.sha256(contraseña_bytes).hexdigest()
        else:
            return hashlib.md5(contraseña_bytes).hexdigest()

    @staticmethod
    def generar_diccionario_comun():
        """
        Genera un diccionario con las contraseñas más comunes
        """
        return [
            "123456", "password", "123456789", "12345", "12345678",
            "qwerty", "abc123", "111111", "123123", "admin",
            "letmein", "welcome", "monkey", "password1", "1234",
            "iloveyou", "654321", "1234567", "sunshine", "master",
            "princesa", "futbol", "hola123", "teamo", "dragon",
            "superman", "batman", "pokemon", "michael", "jennifer"
        ]

    @staticmethod
    def calcular_tiempo_estimado(longitud, incluye_mayus=True, incluye_numeros=True, incluye_simbolos=False,
                                 velocidad=1_000_000):
        """
        Calcula el tiempo estimado para romper una contraseña por fuerza bruta
        """
        charset_size = 26  # minúsculas
        if incluye_mayus:
            charset_size += 26
        if incluye_numeros:
            charset_size += 10
        if incluye_simbolos:
            charset_size += 32

        combinaciones = charset_size ** longitud
        segundos = combinaciones / velocidad

        if segundos < 60:
            return f"{segundos:.1f} segundos", segundos
        elif segundos < 3600:
            return f"{segundos / 60:.1f} minutos", segundos
        elif segundos < 86400:
            return f"{segundos / 3600:.1f} horas", segundos
        elif segundos < 31536000:
            return f"{segundos / 86400:.1f} días", segundos
        else:
            return f"{segundos / 31536000:.1f} años", segundos

    @staticmethod
    def analizar_seguridad_contraseña(contraseña):
        """
        Analiza la seguridad de una contraseña
        """
        resultado = {
            "longitud": len(contraseña),
            "tiene_minusculas": any(c.islower() for c in contraseña),
            "tiene_mayusculas": any(c.isupper() for c in contraseña),
            "tiene_numeros": any(c.isdigit() for c in contraseña),
            "tiene_simbolos": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in contraseña),
            "es_comun": False,
            "fortaleza": "",
            "tiempos": {}
        }

        # Verificar si está en diccionario común
        diccionario = AtaqueFuerzaBruta.generar_diccionario_comun()
        if contraseña.lower() in [p.lower() for p in diccionario]:
            resultado["es_comun"] = True

        # Calcular tiempos para diferentes escenarios
        for escenario, velocidad in AtaqueFuerzaBruta.VELOCIDADES.items():
            tiempo_str, _ = AtaqueFuerzaBruta.calcular_tiempo_estimado(
                resultado["longitud"],
                resultado["tiene_mayusculas"],
                resultado["tiene_numeros"],
                resultado["tiene_simbolos"],
                velocidad
            )
            resultado["tiempos"][escenario] = tiempo_str

        # Determinar fortaleza
        puntuacion = 0
        if resultado["longitud"] >= 12:
            puntuacion += 3
        elif resultado["longitud"] >= 8:
            puntuacion += 2
        else:
            puntuacion += 1

        puntuacion += sum([resultado["tiene_mayusculas"],
                           resultado["tiene_numeros"],
                           resultado["tiene_simbolos"]])

        if resultado["es_comun"]:
            resultado["fortaleza"] = "MUY DÉBIL"
        elif puntuacion <= 3:
            resultado["fortaleza"] = "DÉBIL"
        elif puntuacion <= 5:
            resultado["fortaleza"] = "MODERADA"
        else:
            resultado["fortaleza"] = "FUERTE"

        return resultado

    @staticmethod
    def visualizar_comparativa_tiempos(analisis):
        """
        Crea una visualización de los tiempos estimados
        Maneja errores de renderizado gráfico
        """
        try:
            fig, ax = plt.subplots(figsize=(10, 5))

            escenarios = list(analisis["tiempos"].keys())
            # Convertir tiempos a valores numéricos para la gráfica
            tiempos_num = []
            tiempos_str_limpios = []

            for escenario in escenarios:
                tiempo_str = analisis["tiempos"][escenario]
                tiempos_str_limpios.append(tiempo_str)

                # Limpiar el string para evitar caracteres problemáticos
                try:
                    if "segundos" in tiempo_str:
                        tiempos_num.append(float(tiempo_str.split()[0]))
                    elif "minutos" in tiempo_str:
                        tiempos_num.append(float(tiempo_str.split()[0]) * 60)
                    elif "horas" in tiempo_str:
                        tiempos_num.append(float(tiempo_str.split()[0]) * 3600)
                    elif "días" in tiempo_str:
                        tiempos_num.append(float(tiempo_str.split()[0]) * 86400)
                    else:  # años
                        tiempos_num.append(float(tiempo_str.split()[0]) * 31536000)
                except (ValueError, IndexError):
                    # Si hay error al parsear, asignamos un valor por defecto
                    tiempos_num.append(3600)  # 1 hora como valor por defecto

            # Usar escala logarítmica
            colors = ['red' if t < 3600 else 'orange' if t < 86400 else 'green' for t in tiempos_num]
            bars = ax.bar(escenarios, tiempos_num, color=colors, edgecolor='black')
            ax.set_yscale('log')
            ax.set_ylabel('Tiempo (segundos, escala logarítmica)')
            ax.set_title('Tiempo estimado para romper la contraseña')

            # Añadir etiquetas con el tiempo en formato legible
            for i, (bar, tiempo_str) in enumerate(zip(bars, tiempos_str_limpios)):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.1,
                        tiempo_str, ha='center', va='bottom', rotation=45, fontsize=8)

            plt.tight_layout()
            return fig

        except Exception as e:
            # Si hay cualquier error en la gráfica, devolvemos None
            plt.close('all')  # Cerrar todas las figuras para liberar memoria
            print(f"Error al generar gráfica: {e}")  # Log del error
            return None


class AtaqueDiccionarioReglas:
    """
    Simulador de ataque de diccionario con reglas de mutación
    """

    @staticmethod
    def aplicar_reglas(palabra):
        """
        Aplica reglas comunes de mutación a una palabra base
        """
        variaciones = set()
        variaciones.add(palabra)  # La palabra original

        # Regla 1: Capitalizar primera letra
        if palabra:
            variaciones.add(palabra.capitalize())

        # Regla 2: Todo mayúsculas
        variaciones.add(palabra.upper())

        # Regla 3: Añadir números comunes al final
        for num in ["123", "1234", "2024", "2025", "69", "420", "1", "12", "12345"]:
            variaciones.add(palabra + num)

        # Regla 4: Añadir año actual
        variaciones.add(palabra + "2024")
        variaciones.add(palabra + "2025")

        # Regla 5: Duplicar palabra
        variaciones.add(palabra + palabra)

        # Regla 6: Revertir palabra
        variaciones.add(palabra[::-1])

        # Regla 7: Reemplazar letras por números (leet speak básico)
        leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
        leet_version = palabra
        for letra, num in leet_map.items():
            leet_version = leet_version.replace(letra, num)
        if leet_version != palabra:
            variaciones.add(leet_version)

        # Regla 8: Eliminar última letra
        if len(palabra) > 3:
            variaciones.add(palabra[:-1])

        # Regla 9: Añadir símbolo común
        for simbolo in ["!", "@", "#", "$", "%", "&", "*"]:
            variaciones.add(palabra + simbolo)
            variaciones.add(simbolo + palabra)

        return list(variaciones)

    @staticmethod
    def generar_diccionario_con_reglas(palabras_base, max_por_palabra=20):
        """
        Genera un diccionario completo aplicando reglas a las palabras base
        """
        diccionario_completo = []
        reglas_aplicadas = {}

        for palabra in palabras_base:
            variaciones = AtaqueDiccionarioReglas.aplicar_reglas(palabra)
            # Limitar el número de variaciones por palabra
            variaciones = variaciones[:max_por_palabra]
            diccionario_completo.extend(variaciones)
            reglas_aplicadas[palabra] = len(variaciones)

        return list(set(diccionario_completo)), reglas_aplicadas  # Eliminar duplicados

    @staticmethod
    def simular_ataque(contraseña_objetivo, palabras_base):
        """
        Simula un ataque y dice si la encontraría y con qué regla
        """
        # Primero, verificar si la contraseña está en el diccionario base
        if contraseña_objetivo in palabras_base:
            return {
                "encontrada": True,
                "regla": "Palabra base",
                "palabra_base": contraseña_objetivo,
                "intentos": palabras_base.index(contraseña_objetivo) + 1
            }

        # Si no, buscar entre las variaciones
        intentos = len(palabras_base)
        for palabra in palabras_base:
            variaciones = AtaqueDiccionarioReglas.aplicar_reglas(palabra)
            for i, var in enumerate(variaciones):
                intentos += 1
                if var == contraseña_objetivo:
                    # Identificar qué regla se aplicó
                    regla = AtaqueDiccionarioReglas._identificar_regla(palabra, contraseña_objetivo)
                    return {
                        "encontrada": True,
                        "regla": regla,
                        "palabra_base": palabra,
                        "intentos": intentos
                    }

        return {
            "encontrada": False,
            "regla": None,
            "palabra_base": None,
            "intentos": intentos
        }

    @staticmethod
    def _identificar_regla(original, variacion):
        """Identifica qué regla produjo la variación"""
        if variacion == original.capitalize():
            return "Capitalizar primera letra"
        elif variacion == original.upper():
            return "TODO MAYÚSCULAS"
        elif variacion == original + original:
            return "Duplicar palabra"
        elif variacion == original[::-1]:
            return "Invertir palabra"
        elif any(num in variacion for num in ["123", "2024", "2025"]) and original in variacion:
            return "Añadir números/año"
        elif any(sim in variacion for sim in ["!", "@", "#"]) and original in variacion:
            return "Añadir símbolos"
        else:
            # Verificar leet speak
            leet_map = {'4': 'a', '3': 'e', '1': 'i', '0': 'o', '5': 's', '7': 't'}
            posible_original = variacion
            for num, letra in leet_map.items():
                posible_original = posible_original.replace(num, letra)
            if posible_original == original:
                return "Leet speak (sustitución de letras por números)"

            return "Otra regla"

    @staticmethod
    def visualizar_estadisticas(reglas_aplicadas):
        """
        Crea una visualización de las reglas aplicadas
        """
        fig, ax = plt.subplots(figsize=(10, 5))

        palabras = list(reglas_aplicadas.keys())[:10]  # Top 10
        num_variaciones = list(reglas_aplicadas.values())[:10]

        ax.bar(palabras, num_variaciones, color='lightcoral', edgecolor='darkred')
        ax.set_xlabel('Palabra base')
        ax.set_ylabel('Número de variaciones')
        ax.set_title('Variaciones generadas por palabra base')
        ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        return fig