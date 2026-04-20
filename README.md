# Rishine

RiShine es una pagina web donde podras consultar eventos educativos o ser promotor para crear, publicar y gestionar tus propios eventos de forma mas facil.

## Requisitos

- Python 3.12+
- pip
- Servidor MySQL 8+

## Instalacion local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Luego crea tu archivo local de variables desde el ejemplo:

```bash
copy .env.example .env
```

## Configuracion MySQL

Configura estas variables en tu `.env` antes de ejecutar migraciones:

```bash
DJANGO_SECRET_KEY=tu_clave_secreta
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

MYSQL_DATABASE=rishine_db
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

Asegurate de que la base `rishine_db` exista en MySQL y que el usuario tenga permisos.

## Ejecutar proyecto

```bash
python Rishine/manage.py migrate
python Rishine/manage.py runserver
```

## Notas de colaboracion

- No subir la carpeta `.venv/`, archivos `.env` ni `db.sqlite3`.
- Mantener dependencias actualizadas en `requirements.txt` cuando cambien.
