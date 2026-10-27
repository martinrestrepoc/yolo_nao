import cv2
import random
from pathlib import Path
from ultralytics import YOLO

# model.names contiene los nombres de las clases que reconoce el modelo
# asigna un color a cada clase
model_path = Path(__file__).resolve().parent / 'runs/peluches/train/weights/best.pt'
model = YOLO(str(model_path))
colors = {
    cls_name: tuple(random.randint(0, 255) for _ in range(3))
    for cls_name in model.names.values()
}
# Abre la cámara
video_capture = cv2.VideoCapture(0)

while True:
    # ret indica si pudo obtener fotogramas
    # frame contiene los píxeles de esa imagen, llamada fotograma.
    ret, frame = video_capture.read()
    if not ret:
        print('No se pudo leer un fotograma de la cámara.')
        break

    # Analiza el fotograma con el modelo YOLO
    # verbose=False evita que el modelo imprima su resumen en la terminal.
    results = model(frame, conf=0.25, verbose=False)
    # Crea una copia del fotograma para dibujar sobre ella.
    im = frame.copy()
    # results[0] corresponde al resultado de la imagen enviada .boxes contiene sus detecciones.
    # el for procesa una detección por vuelta
    for box in results[0].boxes:
        # Obtiene las coordenadas del rectángulo

        # .tolist() convierte las coordenadas en una lista y 
        # map(int, ...) las convierte a números enteros para dibujar en píxeles.
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        # Obtiene el nombre de la clase
        cls = results[0].names[int(box.cls[0])]
        # Obtiene la confianza de la detección y la redondea a 4 decimales
        conf = round(float(box.conf[0]), 4)
        color = colors[cls]
        # Dibuja un rectángulo alrededor de la detección.
        print((x1, y1), (x2, y2), cls, conf)
        cv2.rectangle(im, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            im,
            f'{cls}-{conf * 100:.2f}%',
            (x1, max(y1 - 10, 25)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2,
            cv2.LINE_AA,
        )

    cv2.imshow('frame', im)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
