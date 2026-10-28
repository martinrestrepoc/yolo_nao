# Detector de peluches con YOLO26 nano

Proyecto de detección de objetos que reconoce tres peluches específicos mediante
un modelo YOLO26 nano entrenado con fotografías propias etiquetadas en Roboflow.
En la cámara muestra un rectángulo alrededor de cada peluche detectado, su clase
y el nivel de confianza.

Las clases son `peluche_Juan Jose`, `peluche_martin` y `peluche_sebastian`.
El detector está preparado para estos tres peluches; no para reconocer cualquier
peluche de esas categorías.

## Requisitos

- Git y uv instalados.
- Una cámara conectada y disponible.
- Permiso de acceso a la cámara para la aplicación desde la que ejecutes Python.

El proyecto utiliza Python 3.14 o superior. Las dependencias se gestionan con uv.
El modelo ya entrenado está incluido en el repositorio, por lo que no necesitas
entrenarlo ni ejecutar el notebook para probar la cámara.

## Descargar y ejecutar

En una terminal:

```bash
git clone https://github.com/martinrestrepoc/yolo_nao.git
cd yolo_nao
uv sync
uv run python probar_camara.py
```

Se abrirá una ventana con las detecciones. Presiona `q` con esa ventana activa
para cerrar la cámara.

Si ya tienes el proyecto clonado, entra en su carpeta y ejecuta:

```bash
git pull
uv sync
uv run python probar_camara.py
```

El script utiliza la cámara de índice `0`. Si necesitas otra cámara, cambia el
número en `cv2.VideoCapture(0)` dentro de `probar_camara.py`. Si no aparece imagen,
revisa los permisos y que otra aplicación no esté ocupando la cámara.

## Entrenar un modelo nuevo

Abre `Entrenamiento_Peluches_YOLO_nano.ipynb` en VS Code con las extensiones
Python y Jupyter. Selecciona el intérprete de la carpeta `.venv` del proyecto
como kernel y ejecuta las celdas en orden.

El notebook usa `imagenes_peluchesv3/`, que contiene las imágenes y etiquetas
exportadas de Roboflow. La sección 5 inicia el entrenamiento. La primera carga
de los pesos preentrenados `yolo26n.pt` requiere internet.

Los mejores pesos se guardan en `runs/peluches/train/weights/best.pt`, la misma
ruta que usa el script de cámara. Al volver a entrenar se reemplaza el modelo
anterior en esa ruta.
