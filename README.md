# YOLO nano: detector de peluches

## Notebook v2: balanceo y aumentos durante el entrenamiento

`Entrenamiento_Peluches_YOLO_v2.ipynb` usa `imagenes_peluchesv2/`, exportado
sin aumentos. Reúne los originales, omite duplicados exactos y reparte por clase
con semilla fija. Por defecto usa 95 originales de cada peluche: 66 para train,
19 para validación y 10 para test. Las sobrantes se registran como `unused`
sin borrarse del origen; las negativas se reparten aparte.

Ejecuta con el mismo entorno de uv. Revisa primero las secciones 1–5; la sección
6 inicia el entrenamiento con aumentos de Ultralytics solo sobre train.
`SESSION_BY_SOURCE` permite mantener juntas fotos de una misma sesión; sin
esa información, cada original se trata como un grupo independiente. El notebook
actual admite una sola clase por imagen y avisa si encuentra varias.

Los datos preparados y su registro `split_manifest.csv` quedan en
`runs/peluchesv2/dataset/`. Los resultados usan `train`, `val`, `test` y `predict`
dentro de `runs/peluchesv2/`. El modelo final queda en
`runs/peluchesv2/train/weights/best.pt`. El script de cámara conserva el modelo v1
hasta que cambies su ruta. Después de reiniciar el kernel, puedes reevaluar v2
ejecutando los imports, la sección 1 y luego las secciones 8 y 9.

Como se reorganizan las fotos, entrena desde `yolo26n.pt`, no desde el modelo v1.
No uses este test para comparar con v1: puede contener fotos que v1 ya vio.

El notebook `Entrenamiento_Peluches_YOLO_nano.ipynb` adapta el flujo de entrenamiento
del ejemplo BCCD al dataset local `imagenes_peluchesv3/`, que ya incluye aumentos de Roboflow.

## Ejecutar con uv

Desde la raíz del repositorio:

```bash
uv sync
```

Abre el notebook en VS Code con las extensiones Python y Jupyter. En **Select
Kernel → Python Environments**, selecciona `.venv/bin/python` del proyecto.
`ipykernel` está declarado como dependencia de desarrollo y se instala con
`uv sync`; no instales las dependencias con `pip` en las celdas.

Ejecuta las celdas en orden. Primero revisan las imágenes y etiquetas y muestran
ejemplos con cajas. La celda `model.train(...)` inicia el entrenamiento real.
La primera carga de `yolo26n.pt` requiere internet.

El notebook elige CUDA, MPS o CPU según lo disponible en PyTorch. En CPU puede
tardar considerablemente. Puedes ajustar dispositivo, épocas, resolución y
lote en la sección de configuración.

## Datos y resultados

- Export de Roboflow: 452 imágenes de entrenamiento, 65 de validación y 32 de test (dataset v3).
- Se conservan los nombres e IDs de las tres clases del export.
- Se genera `runs/peluches/dataset.yaml` con rutas locales correctas, sin modificar
  el archivo exportado por Roboflow.
- El modelo actual queda en `runs/peluches/train/weights/best.pt`.
- Se usan carpetas fijas `train`, `val`, `test` y `predict` dentro de
  `runs/peluches/`. Las ejecuciones siguientes reutilizan esas carpetas.
- Al finalizar el entrenamiento se conserva solo `best.pt`.
- Se incluyen curvas, evaluación de validación, evaluación final de test y
  predicciones visuales. ONNX es opcional.

El dataset contiene archivos de etiquetas vacíos. Son válidos si esas imágenes
no muestran ninguno de los tres peluches objetivo; compruébalos si esperabas
que todas las fotos fueran positivas. La distribución por clase se imprime
antes de entrenar. En v3, test tiene 8 cajas de Juan José, 8 de Martín y 13 de
Sebastián; los conteos por grupo todavía no son exactamente iguales.

Mantén juntas las fotos casi iguales de una sesión y sus variantes aumentadas.
Usa validación para elegir parámetros y reserva test para la evaluación final.
Los resultados, cachés y demás pesos están excluidos de Git, excepto
`runs/peluches/train/weights/best.pt`, que se incluye para poder usar el modelo
nano sin volver a entrenarlo al clonar.

Para probarlo después de clonar, desde la raíz del proyecto ejecuta:

```bash
uv sync
uv run python probar_camara.py
```

Presiona `q` para cerrar la cámara. Solo necesitas ejecutar el entrenamiento
del notebook si deseas generar un modelo nuevo.

## Comparación nano y medium con el dataset v3

`Entrenamiento_Peluches_YOLO_nano.ipynb` conserva el entrenamiento actual con
`yolo26n.pt` en `runs/peluches/`.
`Entrenamiento_Peluches_YOLO_medium.ipynb` repite el flujo con `yolo26m.pt` y
resultados en `runs/peluches_medium/`. El modelo medium quedará en
`runs/peluches_medium/train/weights/best.pt`.

Ejecuta medium con un kernel nuevo o reiniciado, en orden. Ambos usan
`imagenes_peluchesv3`, las mismas divisiones de datos, épocas máximas, paciencia,
resolución, lote, semilla, aumentos y umbral de evaluación. Medium necesita más
memoria; si reduces el lote, registra esa diferencia. Compara las métricas de
validación, las cajas y la velocidad; reserva test para la comparación final.
El script de cámara sigue apuntando al nano hasta que cambies la ruta.
