import random
import string

class Cifrados:
    """Clase con implementaciones de cifrados clásicos"""

    @staticmethod
    def cifrado_cesar(texto, desplazamiento):
        resultado = ""
        for caracter in texto:
            if caracter.isalpha():
                mayus = caracter.isupper()
                caracter = caracter.lower()
                codigo = ord(caracter) - 97
                nuevo_codigo = (codigo + desplazamiento) % 26
                nuevo_caracter = chr(nuevo_codigo + 97)
                if mayus:
                    nuevo_caracter = nuevo_caracter.upper()
                resultado += nuevo_caracter
            else:
                resultado += caracter
        return resultado

    @staticmethod
    def cifrado_sustitucion(texto, clave_sustitucion=None):
        if clave_sustitucion is None:
            alfabeto = list(string.ascii_lowercase)
            mezclado = alfabeto.copy()
            random.shuffle(mezclado)
            clave_sustitucion = dict(zip(alfabeto, mezclado))

        resultado = ""
        for caracter in texto:
            if caracter.isalpha():
                mayus = caracter.isupper()
                caracter = caracter.lower()
                if caracter in clave_sustitucion:
                    nuevo = clave_sustitucion[caracter]
                    if mayus:
                        nuevo = nuevo.upper()
                    resultado += nuevo
                else:
                    resultado += caracter
            else:
                resultado += caracter
        return resultado, clave_sustitucion

    @staticmethod
    def cifrado_vigenere(texto, clave):
        resultado = ""
        clave = clave.lower()
        indice_clave = 0

        for caracter in texto:
            if caracter.isalpha():
                mayus = caracter.isupper()
                caracter = caracter.lower()
                desplazamiento = ord(clave[indice_clave % len(clave)]) - 97
                codigo = ord(caracter) - 97
                nuevo_codigo = (codigo + desplazamiento) % 26
                nuevo_caracter = chr(nuevo_codigo + 97)
                if mayus:
                    nuevo_caracter = nuevo_caracter.upper()
                resultado += nuevo_caracter
                indice_clave += 1
            else:
                resultado += caracter

        return resultado