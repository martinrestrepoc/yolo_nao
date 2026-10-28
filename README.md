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

## Preparación del dataset

Se tomaron fotografías de los tres peluches en distintos ángulos, posiciones,
distancias y lugares. En Roboflow se etiquetó cada peluche con una caja y su
clase. También se incluyeron imágenes negativas, sin ninguno de los peluches
objetivo; sus archivos de etiquetas quedan vacíos.

Primero se dividieron las **323 imágenes originales**, antes de generar
aumentos, con una proporción aproximada de 70 % para entrenamiento, 20 % para
validación y 10 % para prueba. El reparto fue de 226, 65 y 32 imágenes,
respectivamente. La división global no garantiza cantidades idénticas de cada
clase dentro de cada grupo.

Como preprocesamiento se aplicó **Auto-Orient**, que normaliza la orientación
según los metadatos de la cámara y elimina la dependencia de la rotación EXIF.
El export no incluye un redimensionamiento fijo; el notebook configura
`imgsz=640` para el entrenamiento.

Después se aplicó una **aumentación x2 únicamente a entrenamiento**: cada
original de ese grupo aporta dos imágenes en total, el original preprocesado y
una variante aumentada. Las transformaciones aleatorias configuradas fueron:

- Volteo horizontal con probabilidad del 50 %.
- Rotación entre −10° y +10°.
- Variación de brillo entre −15 % y +15 %.
- Variación de exposición entre −10 % y +10 %.
- Desenfoque gaussiano de hasta 1.5 píxeles.

El dataset exportado en formato YOLO26 y guardado en `imagenes_peluchesv3/`
quedó así:

| Grupo | Antes de aumentos | Después de aumentos |
|---|---:|---:|
| Entrenamiento | 226 | 452 |
| Validación | 65 | 65 |
| Prueba (test) | 32 | 32 |
| Total | 323 | 549 |

Por eso Roboflow muestra aproximadamente 82 % de entrenamiento, 12 % de
validación y 6 % de test al final. Cambió el porcentaje sobre el total, pero las
imágenes de validación y test no se aumentaron. Al separar primero los
originales, sus variantes aumentadas permanecen en entrenamiento. Las fotos
casi iguales de una misma sesión también deben mantenerse en un solo grupo.

Los aumentos aportan variaciones para el aprendizaje y, al aplicarse por igual
a las clases, conservan aproximadamente sus proporciones dentro de train.
No corrigen un desbalance previo ni sustituyen nuevas fotografías variadas.

Además de los aumentos ya exportados, el notebook permite variaciones moderadas
durante el entrenamiento con Ultralytics: saturación (`hsv_s=0.2`), luminosidad
(`hsv_v=0.1`), desplazamiento (`translate=0.05`) y escala (`scale=0.1`). Desactiva
la rotación adicional, el volteo horizontal adicional, los cambios de tono y
mosaic. Estos ajustes se aplican solo durante el entrenamiento y no aumentan el
número de archivos del dataset.

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
