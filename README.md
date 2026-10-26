# YOLO nano: detector de peluches

El notebook `Entrenamiento_Peluches_YOLO.ipynb` adapta el flujo de entrenamiento
del ejemplo BCCD al dataset local `Imagenes peluches/`.

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

- Export de Roboflow: 308 imágenes de entrenamiento, 44 de validación y 22 de test.
- Se conservan los nombres e IDs de las tres clases del export.
- Se genera `runs/peluches/dataset.yaml` con rutas locales correctas, sin modificar
  el archivo exportado por Roboflow.
- Cada entrenamiento crea una carpeta `runs/peluches/nano*`; los mejores pesos
  quedan en `weights/best.pt`. La ruta exacta aparece en el notebook.
- Se incluyen curvas, evaluación de validación, evaluación final de test y
  predicciones visuales. ONNX es opcional.

El dataset contiene archivos de etiquetas vacíos. Son válidos si esas imágenes
no muestran ninguno de los tres peluches objetivo; compruébalos si esperabas
que todas las fotos fueran positivas. La distribución por clase se imprime
antes de entrenar. En particular, test tiene solo una caja de
`peluche_Juan Jose`, así que su métrica será poco representativa.

Mantén juntas las fotos casi iguales de una sesión y sus variantes aumentadas.
Usa validación para elegir parámetros y reserva test para la evaluación final.
Los resultados, pesos y cachés están excluidos de Git.
