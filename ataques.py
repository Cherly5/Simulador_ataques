from collections import Counter
from matplotlib import pyplot as plt
from cifrados import Cifrados


def fuerza_bruta(texto_cifrado):
    resultados = []
    for clave in range(1, 26):
        texto_descifrado = Cifrados.cifrado_cesar(texto_cifrado, -clave)
        palabras = texto_descifrado.split()
        porcentaje_letras = sum(c.isalpha() for c in texto_descifrado) / len(
            texto_descifrado) * 100 if texto_descifrado else 0

        resultados.append({
            'Clave': clave,
            'Texto descifrado': texto_descifrado,
            'N° Palabras': len(palabras),
            '% Letras': round(porcentaje_letras, 1)
        })
    return resultados

class AtaqueFrecuencias:
    FRECUENCIAS_ESPANOL = {
        'a': 12.53, 'b': 1.42, 'c': 4.68, 'd': 5.86, 'e': 13.68,
        'f': 0.69, 'g': 1.01, 'h': 0.70, 'i': 6.25, 'j': 0.44,
        'k': 0.02, 'l': 4.97, 'm': 3.15, 'n': 6.71, 'ñ': 0.31,
        'o': 8.68, 'p': 2.51, 'q': 0.88, 'r': 6.87, 's': 7.98,
        't': 4.63, 'u': 3.93, 'v': 0.90, 'w': 0.01, 'x': 0.22,
        'y': 0.90, 'z': 0.52
    }

    @staticmethod
    def calcular_frecuencias(texto):
        letras = [c.lower() for c in texto if c.isalpha()]
        total = len(letras)
        if total == 0:
            return {}
        contador = Counter(letras)
        frecuencias = {letra: (count / total) * 100 for letra, count in contador.items()}
        return dict(sorted(frecuencias.items(), key=lambda x: x[1], reverse=True))

    @staticmethod
    def visualizar(texto_cifrado):
        frec_cifrado = AtaqueFrecuencias.calcular_frecuencias(texto_cifrado)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

        # Gráfica 1: Frecuencias en texto cifrado
        letras_cifrado = list(frec_cifrado.keys())[:10]
        frecs_cifrado = list(frec_cifrado.values())[:10]

        ax1.bar(letras_cifrado, frecs_cifrado, color='skyblue', edgecolor='navy')
        ax1.set_title('Frecuencias en Texto Cifrado', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Letras')
        ax1.set_ylabel('Frecuencia (%)')
        ax1.grid(axis='y', alpha=0.3)

        # Gráfica 2: Frecuencias en español
        letras_espanol = list(AtaqueFrecuencias.FRECUENCIAS_ESPANOL.keys())[:10]
        frecs_espanol = [AtaqueFrecuencias.FRECUENCIAS_ESPANOL[l] for l in letras_espanol]

        ax2.bar(letras_espanol, frecs_espanol, color='lightcoral', edgecolor='darkred')
        ax2.set_title('Frecuencias en Español', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Letras')
        ax2.set_ylabel('Frecuencia (%)')
        ax2.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        return fig

def encontrar_repeticiones(texto, longitud_min=3):
    texto_limpio = ''.join(c.lower() for c in texto if c.isalpha())
    repeticiones = {}

    for lon in range(longitud_min, min(6, len(texto_limpio) // 2)):
        for i in range(len(texto_limpio) - lon):
            secuencia = texto_limpio[i:i + lon]
            for j in range(i + lon, len(texto_limpio) - lon):
                if texto_limpio[j:j + lon] == secuencia:
                    distancia = j - i
                    if secuencia not in repeticiones:
                        repeticiones[secuencia] = []
                    repeticiones[secuencia].append(distancia)
    return repeticiones

def estimar_longitud_clave(repeticiones):
    distancias = []
    for secuencia, datos in repeticiones.items():
        distancias.extend(datos)

    if not distancias:
        return []

    posibles_longitudes = []
    for dist in set(distancias):
        for divisor in range(2, min(10, dist)):
            if dist % divisor == 0:
                posibles_longitudes.append(divisor)

    contador = Counter(posibles_longitudes)
    return contador.most_common()

def obtener_longitudes_mas_probables(sugerencias):
    if not sugerencias:
        return []

    # La frecuencia más alta (primer elemento porque most_common() ya ordena)
    max_frecuencia = sugerencias[0][1]

    # Filtrar todas las longitudes que tengan esa misma frecuencia
    longitudes = [
        longitud for longitud, frecuencia in sugerencias
        if frecuencia == max_frecuencia
    ]

    return longitudes
