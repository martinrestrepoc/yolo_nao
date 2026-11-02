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

## Métrica y selección del mejor modelo

Usamos **mAP50-95 de validación** para seleccionar el mejor modelo. Esta métrica
evalúa la clase predicha y la ubicación de las cajas, promediando la precisión
media entre las clases y entre umbrales de superposición IoU de 0.50 a 0.95.
Es más exigente con el ajuste de las cajas que mAP50; no representa el porcentaje
de imágenes acertadas.

En el entrenamiento nano registrado, el mejor resultado ocurrió en la
**época 45**, con un mAP50-95 de validación de **0.90644** (90.644 %). El valor
puede consultarse en la columna `metrics/mAP50-95(B)` de
[runs/peluches/train/results.csv](runs/peluches/train/results.csv), incluido en
el repositorio para consultar las pérdidas y métricas de cada época.
Se entrenaron 50 épocas y `best.pt` conserva
los pesos del mejor resultado, no necesariamente los de la última época.

La validación automática después de cada época guía esa selección. Test se
reserva para la evaluación final y no participa en la elección de `best.pt`.
Las evaluaciones posteriores del notebook usan `conf=0.25`, por lo que sus
métricas pueden diferir de las registradas durante el entrenamiento. Un nuevo
entrenamiento puede obtener su mejor resultado en otra época.

## Análisis de las curvas de entrenamiento

En las gráficas del notebook nano, los errores de entrenamiento y validación
disminuyen, mientras la precisión y el recall se acercan a 1. Esto indica que
el modelo mejora tanto al reconocer los peluches como al ubicar sus cajas.
El mAP50 se estabiliza pronto y el mAP50-95 sigue aumentando, señal de que el
ajuste de las cajas continúa mejorando aunque ya se detecten los objetos.

Hacia las últimas épocas las mejoras son pequeñas. No se observa un aumento
sostenido del error de validación, por lo que las curvas no muestran una señal
clara de sobreajuste. Aun así, los resultados deben confirmarse con fotos de
sesiones nuevas: las imágenes casi iguales repartidas entre entrenamiento y
validación pueden hacer que las métricas parezcan mejores de lo que serían en
escenarios nuevos.

## Pruebas realizadas

La primera prueba usó un dataset más pequeño: 220 originales que, después de
aumentar x2 únicamente train, dieron 374 imágenes (308 de entrenamiento, 44 de
validación y 22 de test). La distribución por clase era menos equilibrada; por
ejemplo, test tenía solo una imagen del peluche de Juan José, insuficiente para
evaluar de forma representativa esa clase.

Después se amplió la colección a 323 originales y se generó el dataset actual
de 549 imágenes descrito arriba. También se probó un notebook alternativo con
balanceo exacto por clase y aumentos durante el entrenamiento con Ultralytics.
Ese experimento obtuvo un mAP50-95 de test de 0.707, frente a 0.895 del nano
actual con el export aumentado de Roboflow. Como se utilizaron divisiones y
cantidades de entrenamiento diferentes, esta comparación no permite atribuir
la diferencia únicamente a la herramienta de aumentación.

Con el mismo dataset actual se comparó **YOLO26 nano con YOLO26 medium**,
manteniendo las divisiones, los parámetros de entrenamiento y el umbral de
evaluación `conf=0.25`:

| Métrica | Nano | Medium |
|---|---:|---:|
| mAP50-95 en validación | 0.903 | 0.861 |
| mAP50-95 en test | 0.895 | 0.834 |
| mAP50 en test | 0.995 | 0.995 |

Medium no mejoró el resultado en esta ejecución: ambos alcanzaron el mismo
mAP50 en test, pero nano obtuvo mayor mAP50-95, que exige cajas más precisas.
Por eso se conservó nano como modelo del script de cámara. Esto no significa
que medium siempre rinda peor; la conclusión corresponde a estos datos y esta
configuración. Los notebooks y datasets de los experimentos alternativos se
conservan localmente y están excluidos de Git.
