# Exodus Contable

## Descripción general

Exodus Contable es un proyecto académico desarrollado para el análisis y prueba del flujo de autenticación y ejecución principal del sistema.

Actualmente, el proyecto se encuentra en una fase de análisis, por lo que algunas decisiones técnicas están orientadas a facilitar la evaluación y las pruebas controladas.



## Advertencias importantes

### No modificar archivos JSON manualmente

Los archivos con extensión `.json` no deben ser editados manualmente.

* Funcionan como almacenamiento interno del sistema.
* Cualquier modificación directa puede:

* Corromper la información
* Generar errores de ejecución
* Invalidar los resultados del análisis

Toda modificación debe realizarse únicamente a través del programa.



### Ejecución recomendada del proyecto

Para un análisis completo y correcto, se recomienda:

1. Descargar el repositorio completo.
2. Ejecutar el archivo `Exodus_Login.py`.
3. Seguir el flujo normal del sistema hasta llegar al módulo principal.

Esto garantiza que:

* Los datos se carguen correctamente.
* Las validaciones se ejecuten en el orden esperado.



### Ejecución individual de módulos

De forma individual, es posible realizar pruebas separadas de:

* `Exodus_Login.py`
* `Exodus_Main.py`

Nota:

* Al ejecutar módulos de forma aislada, algunas funcionalidades pueden estar limitadas.
* Esto se recomienda únicamente para pruebas técnicas o revisión de lógica interna.



## Requisitos del sistema

* Python 3.10 o superior
* Sistema operativo Windows (probado)
* Consola o terminal habilitada



## Dependencias y librerías utilizadas

Este proyecto utiliza exclusivamente librerías estándar de Python, incluidas por defecto en la instalación oficial.

### Librerías usadas

* `json`: Lectura y escritura de datos estructurados
* `os`: Gestión de rutas, archivos y validaciones del sistema
* `sys`: Control del flujo de ejecución y salida del programa
* `getpass`: Entrada segura de contraseñas en consola
* `time`: Manejo de pausas y temporización

No se requiere la instalación de librerías externas ni el uso de `pip`.



## Estructura básica del proyecto


Exodus-Contable/
│
├── Exodus_Login.py
├── Exodus_Main.py
├── README.md
├── *.json
└── otros archivos del sistema




## Contexto académico

Este proyecto hace parte de un proceso de formación académica.

* No está destinado a uso en producción
* El código puede cambiar durante el proceso de evaluación
* Algunas validaciones pueden encontrarse en desarrollo

## Notas finales

* No alterar la estructura de carpetas
* No eliminar archivos aunque no se utilicen directamente
* No modificar manualmente los archivos de datos
* Todos los cambios deben realizarse desde el código fuente



## Autores

* Jesús Daniel Perez Berrocal
* Camilo Andres Meza De Avila
* Andres Camilo Sarmiento Leudo
