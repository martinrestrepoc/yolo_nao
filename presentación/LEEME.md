# Los amigos de NAO

Abre `index.html` con Chrome, Edge, Firefox o Safari. No requiere instalar
paquetes ni iniciar un servidor. Conserva toda esta carpeta al compartirla:
el HTML usa los estilos, el JavaScript, las fotos y las fuentes locales.

## Controles

- Flechas izquierda/derecha o espacio: cambiar de diapositiva.
- Home / End: primera / última.
- I: índice con acceso a las 14 diapositivas.
- N: notas del expositor de la diapositiva actual.
- F: pantalla completa, cuando el navegador lo permita.
- P: imprimir todas las diapositivas o guardarlas como PDF.
- Esc: cerrar el índice, las notas o la ayuda.

En móvil el contenido de cada diapositiva puede desplazarse verticalmente;
los botones inferiores permanecen disponibles. También se puede deslizar
horizontalmente para cambiar de diapositiva.

Para imprimir, utiliza orientación horizontal, respeta el tamaño definido por
la página y activa los gráficos de fondo si tu navegador lo solicita.

## Archivos

- `index.html`: las 14 diapositivas y las notas del expositor.
- `styles.css`: diseño, adaptación a móvil e impresión.
- `presentation.js`: navegación y gráficas interactivas.
- `data.js`: métricas y series del entrenamiento utilizadas en las gráficas.
- `assets/`: fotografías y tipografías incluidas para uso sin conexión.
- `assets/sources.json`: procedencia de las imágenes del proyecto.
- `assets/fonts/`: archivos de fuente, procedencia y licencias OFL.
- `fuentes/README-proyecto.md`: copia del README usado como base.
- `fuentes/results-nano.csv`: los 50 registros del entrenamiento nano.
- `DISEÑO.md`: dirección visual definida con UI UX Pro Max.
- `revisión/`: revisión de Impeccable y capturas de comprobación.

Las fotos con cajas son predicciones estáticas existentes del proyecto.
La presentación no enciende la cámara ni ejecuta Python. Para la demostración
real se usa el comando `uv run python probar_camara.py` desde el repo.

La portada y todas las cifras proceden de los archivos locales del proyecto.
No se generan cifras de ejemplo. La mejor época del entrenamiento y la
reevaluación posterior con conf=0.25 se distinguen en las diapositivas y notas.

La presentación enmarca a los peluches como los amigos que NAO quiere reconocer.
La última diapositiva invita a ejecutar el script y permite copiar el comando.
La demostración usa la cámara del computador; no implica integración con el robot.
