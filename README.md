# Atlas Humano — Diccionario anatómico

Aplicación educativa web hecha con Flask, SQLAlchemy, HTML, CSS y JavaScript. Permite buscar conceptos de anatomía y consultar descripción, funciones, datos curiosos y ubicación.

## Características
- Búsqueda por nombre, categoría y descripción.
- Fichas de detalle en ventana emergente.
- Categorías de órganos, huesos, músculos y sistemas.
- Diseño adaptable a computadoras y móviles.
- 11 conceptos de ejemplo cargados automáticamente.
- SQLite para probar rápidamente; MySQL para la presentación final.
- Sin Docker.

## 1. Requisitos
- Python 3.10 o posterior.
- Para modo MySQL: MySQL Server instalado y en ejecución.
- Navegador moderno.

## 2. Preparar entorno (Windows)
Abre CMD o PowerShell dentro de la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell impide activar el entorno, usa CMD y ejecuta:
```bat
.venv\\Scripts\\activate.bat
```

## 3. Probar inmediatamente sin instalar MySQL
La aplicación usa SQLite por defecto para facilitar una primera prueba:

```powershell
python app.py
```

Abre http://127.0.0.1:5000 en tu navegador. Se creará `diccionario_demo.db` con los datos de ejemplo.

## 4. Configurar MySQL
1. Inicia MySQL Server.
2. Ejecuta el contenido de `schema.sql` desde MySQL Workbench o el cliente MySQL.
3. Crea un usuario dedicado para esta aplicación y dale permisos únicamente sobre `diccionario_anatomia`.
4. Define `DATABASE_URL` antes de ejecutar Flask. Ejemplo para PowerShell:

```powershell
$env:DATABASE_URL = "mysql+pymysql://atlas_user:TU_CLAVE@localhost/diccionario_anatomia"
python app.py
```

Reemplaza usuario y contraseña con tus datos reales. Si la contraseña tiene caracteres especiales como `@`, `:`, `/` o `#`, codifícala para URL. No subas credenciales a GitHub.

La primera vez, Flask/SQLAlchemy crea la tabla y carga los conceptos de ejemplo en la base seleccionada si está vacía.

## 5. Usarla en otras computadoras
- **Solo en la misma computadora:** entra a `http://127.0.0.1:5000`.
- **En la misma red local:** inicia Flask con `app.run(host="0.0.0.0", port=5000, debug=False)` y abre `http://IP-DE-LA-COMPUTADORA:5000` desde otra computadora. Configura el firewall cuidadosamente y no expongas el servidor directamente a Internet.
- **Desde cualquier lugar por Internet:** despliega Flask en un hosting compatible con Python y MySQL en un servidor administrado. Configura `DATABASE_URL` como variable secreta del hosting. No basta con copiar la carpeta a otra computadora: el servidor debe estar ejecutándose y ser accesible.

Para una demostración real, usa un servidor WSGI como Waitress en Windows o Gunicorn en Linux; no uses `debug=True` en producción.

## 6. Subir a GitHub
```bash
git init
git add .
git commit -m "Primera versión de Atlas Humano"
git branch -M main
git remote add origin URL_DE_TU_REPOSITORIO
git push -u origin main
```

## Nota sobre contenido e imágenes
Este proyecto es educativo, no es una herramienta de diagnóstico médico. Las ilustraciones se cargan desde Wikimedia Commons; se requiere conexión a Internet para verlas. Si una imagen externa cambia o no carga, aparece un emoji de respaldo. Revisa la licencia y atribución de cada imagen antes de redistribuir el proyecto públicamente.
