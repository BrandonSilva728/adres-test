# Proyecto Django

## Se creo una pagina index en donde se encuentran tres botones:

### El primero contiene la validacion de los archivos.
    * Este proyecto es una aplicación web en **Django** que permite subir y validar archivoso, adicional a eso se valido que el formato permitido solo sea CSV o TXT.
    * Dentro de este van a poder ver un botón llamado historial que contiene el historico de cada archivo que se intento validar con su respectivo detalle.

### El segundo botón ejecuta el script para validar las facturas y retorna un reporte de la ejecución del script.

### El tercer botón muestra un historico de las facturas validadas con su respectivo detalle.

-------------

## 📌 **Requisitos técnicos**  

- **Python 3.11 o superior**  
- **Docker (opcional, si deseas ejecutar el proyecto en contenedor)**  

## 🚀 **Instalación y ejecución**  

### 1️⃣ Clonar el repositorio  

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_PROYECTO>
```

### 2️⃣ Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Linux/macOS
venv\Scripts\activate  # En Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Aplicar migraciones y ejecutar el servidor

```bash
python manage.py migrate
python manage.py runserver
```

El servidor se ejecutará en http://127.0.0.1:8000/.

---------

## 🐳 Ejecutar con Docker

Si prefieres usar Docker, sigue estos pasos:

### 1️⃣ Construir la imagen

```bash
docker build -t django_app .
```

### 2️⃣ Ejecutar el contenedor

```bash
docker run -p 8000:8000 django_app
```
