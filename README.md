# Exodus Contable

Software contable de escritorio desarrollado en **Python** con interfaz gráfica en **CustomTkinter** y **programación orientada a objetos (POO)**. Proyecto académico en desarrollo.

## Estado del proyecto

En desarrollo. Está planificada una migración futura hacia una versión web.

## Funcionalidades

- Inicio de sesión con usuarios.
- Módulo principal con gestión de inventario, trabajadores, contabilidad y etiquetas.
- Almacenamiento local en archivos JSON (sin base de datos).
- Tema claro y oscuro con iconos propios.

## Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.10+ | Lenguaje principal |
| CustomTkinter | Interfaz gráfica |
| JSON | Almacenamiento de datos |
| Librerías estándar (`json`, `os`, `sys`, `getpass`, `time`) | Lectura y escritura de datos, rutas, control de ejecución y temporización |

## Requisitos

- Python 3.10 o superior
- Windows (sistema en el que se ha probado)
- `pip` para instalar CustomTkinter

## Instalación y ejecución

```bash
git clone https://github.com/UNCOMMONFITZGERALD7/EXODUS-CONTABLE.git
cd EXODUS-CONTABLE
pip install customtkinter
python Exodus_Login.py
```

Ejecuta siempre `Exodus_Login.py` y sigue el flujo normal hasta llegar al módulo principal. Así los datos se cargan correctamente y las validaciones se ejecutan en el orden esperado.

Es posible probar `Exodus_Login.py` y `Exodus_Main.py` por separado, pero algunas funciones quedan limitadas. Se recomienda solo para pruebas técnicas o revisión de la lógica interna.

## Advertencias

- **No edites los archivos `.json` a mano.** Funcionan como almacenamiento interno, y una modificación directa puede corromper la información o generar errores de ejecución.
- No alteres la estructura de carpetas.
- No elimines archivos aunque no se usen directamente.
- Todos los cambios deben hacerse desde el código fuente.

## Estructura del proyecto

```
EXODUS-CONTABLE/
├── Exodus_Login.py      # Punto de entrada: inicio de sesión
├── Exodus_Main.py       # Módulo principal
├── config.json          # Configuración
├── *.json               # Datos del sistema (usuarios, inventario, trabajadores, contabilidad, etiquetas)
├── Imageresources/      # Iconos e imágenes
├── LogLogins/           # Registros de inicio de sesión
├── to-do.txt            # Pendientes
└── README.md
```

## Contexto académico

Este proyecto hace parte de un proceso de formación. No está destinado a producción, y el código puede cambiar durante el proceso de evaluación.

## Autor

Jesús Daniel Pérez Berrocal
