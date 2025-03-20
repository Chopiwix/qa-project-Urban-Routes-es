# Urban Routes Automation

## Descripción del Proyecto

Este proyecto consiste en la automatización de pruebas para la plataforma web **Urban Routes**, un servicio que permite a los usuarios solicitar taxis mediante una interfaz gráfica. El objetivo es automatizar todo el flujo de solicitud de un taxi, desde la selección de direcciones hasta el pago y envío de un mensaje al conductor.

## Tecnologías y Técnicas Utilizadas
- **Python 3.11.9**
- **Selenium**: Para la automatización de la interacción con el navegador.
- **Pytest**: Como framework para la ejecución de pruebas automatizadas.
- **WebDriver** (Google Chrome): Para la simulación de la interacción del navegador.
- **XPath Selectors**: Para la identificación precisa de elementos en la interfaz web.
- **JavaScript Click Handling**: Para asegurar que los elementos sean correctamente activados cuando existan problemas con elementos superpuestos.
- **Entornos Virtuales**: Para un manejo limpio de las dependencias.

## Instalación del Entorno
1. Clona este repositorio en tu máquina local.
2. Crea un entorno virtual y actívalo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   .\venv\Scripts\activate  # Para Windows
   ```
3. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

## Estructura del Proyecto
- `main.py`: Contiene el código principal de las pruebas automatizadas.
- `data.py`: Contiene las configuraciones y datos utilizados durante las pruebas (URL, número de teléfono, etc.).
- `requirements.txt`: Archivo con las dependencias necesarias (Selenium, Pytest).

## Ejecución de Pruebas
Para ejecutar las pruebas, utiliza el siguiente comando en la raíz del proyecto:
```bash
pytest main.py
```
Este comando ejecutará todas las pruebas contenidas en `main.py` y mostrará un reporte detallado de los resultados.

## Recomendaciones
- Asegúrate de tener **Google Chrome** instalado y actualizado.
- Verifica que el `chromedriver` sea compatible con la versión de Chrome instalada.
- Si deseas ver el navegador mientras se realizan las pruebas, comenta las líneas relacionadas con `headless` en las configuraciones del WebDriver.

## Contacto
Si tienes alguna duda o problema con el proyecto, no dudes en contactarme.

