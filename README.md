
# Simulador de Ataques Criptográficos

## Descripción

Este proyecto es un simulador de ataques criptográficos desarrollado en Python. Permite a los usuarios experimentar y aprender sobre diferentes tipos de cifrados y cómo pueden ser vulnerados mediante diversos ataques. La aplicación cuenta con una interfaz gráfica que facilita la selección de algoritmos de cifrado, la introducción de datos y la visualización de los resultados de los ataques.

## Características

- **Interfaz Gráfica de Usuario (GUI):** Una interfaz intuitiva construida con `streamlit` para una fácil interacción.
- **Variedad de Cifrados:** Implementación de varios algoritmos de cifrado clásicos.
- **Simulación de Ataques:** Demostración de varios métodos de ataque clásicos y modernos, para entender las vulnerabilidades de los cifrados.
- **Educativo:** Diseñado como una herramienta de aprendizaje para estudiantes y entusiastas de la ciberseguridad.

## Instalación

Para ejecutar este proyecto, necesitarás tener Python instalado. Luego, puedes clonar el repositorio e instalar las dependencias.

1. **Clona el repositorio:**
   ```bash
   git clone <URL-del-repositorio>
   cd Simulador_ataques
   ```

2. **Crea un entorno virtual (recomendado):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows usa `.venv\Scripts\activate`
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r Requirements.txt
   ```

## Uso

Para iniciar la aplicación, ejecuta el siguiente comando en la raíz del proyecto:

```bash
streamlit run main.py
```

La ventana principal te permitirá seleccionar un tipo de cifrado, ingresar el texto a cifrar y una clave. Después de cifrar el texto, podrás elegir un tipo de ataque para intentar descifrar el mensaje.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
Simulador_ataques/
├── main.py               # Punto de entrada principal y GUI
├── cifrados.py           # Implementación de los algoritmos de cifrado
├── ataques.py            # Implementación de los ataques a cifrados clásicos
├── ataques_modernos.py   # Implementación de los ataques a cifrados modernos
├── Requirements.txt      # Dependencias del proyecto
└── ...
```

- `main.py`: Contiene el código de la interfaz gráfica y la lógica principal de la aplicación.
- `cifrados.py`: Define las clases y funciones para los diferentes algoritmos de cifrado.
- `ataques.py` y `ataques_modernos.py`: Contienen las funciones que simulan los ataques a los textos cifrados o contraseñas.
- `Requirements.txt`: Lista todas las librerías de Python necesarias para que el proyecto funcione correctamente.

## Dependencias

El proyecto utiliza las siguientes librerías:

- streamlit
- matplotlib
- numpy

Puedes instalarlas todas con el archivo `Requirements.txt` como se mencionó anteriormente.
