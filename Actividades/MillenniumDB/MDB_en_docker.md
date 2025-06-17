# Instalación MillenniumDB Docker

## 1. Compilar imagen

```bash
docker build -t mdb .
```

## 2. Crear una base de datos

Asumiendo que existe un archivo con datos en `./data/my_data.qm`, el siguiente comando creará una base de datos en `./data/my_db`

```bash
docker run --rm \
    --volume "$PWD"/data:/data \
    mdb \
    mdb import \
    /data/my_data.qm \
    /data/my_db
```

En caso que se quiera eliminar una base de datos, simplemente se debe eliminar el directorio:

```bash
rm -rf ./data/my_db
```

## 3. Iniciar un servidor

Una vez creada la base de datos se puede iniciar el servidor

```bash
docker run --rm \
    --volume "$PWD"/data:/data \
    -p 1234:1234 \
    -p 4321:4321 \
    mdb \
    mdb server \
    /data/my_db
```
