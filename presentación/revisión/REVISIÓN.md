# Revisión de la presentación

Se definió la dirección visual con UI UX Pro Max y se aplicó una revisión de
Impeccable polish sobre la implementación. La revisión preservó los datos y la
dirección editorial; no añadió afirmaciones de desempeño.

## Comprobaciones

- 15 diapositivas, índice, límites anterior/siguiente y URL por diapositiva.
- Navegación por teclado incluso después de enfocar los botones.
- Apertura y cierre con Escape de índice y notas del expositor.
- Gráfico de comparación: validación y test actualizan valores, diferencias,
  etiquetas y estado accesible. Tabla con todos los resultados como alternativa.
- Escritorio 1440×900 y 1280×720: sin desbordamiento de las 15 diapositivas.
- Móvil 375×812: sin desbordamiento horizontal; desplazamiento vertical cuando
  el contenido no cabe en una pantalla.
- Vista de impresión: las 15 diapositivas visibles, sin desbordamientos detectados.
- Apertura directa con file://: fuentes e imágenes cargadas, sin errores JavaScript.
- Movimiento reducido respetado; foco visible, nombres de botones y textos alternativos.
- Gráficas de entrenamiento construidas con el CSV, sin suavizado ni valores inventados.

## Ajustes realizados

Se sincronizaron las diferencias de puntos con el grupo elegido en el gráfico.
Se corrigió el manejo del teclado cuando un botón conserva el foco. Se eliminó
una imagen sin uso y la petición de favicon que producía un 404. Se incluyeron
las licencias de las tipografías.

El detector mecánico se ejecutó una vez. Sus alertas de interlineado y padding
no correspondían a la geometría observada en el navegador: los títulos tienen
interlineado compacto intencional, las columnas con divisor tienen espacio
interno y el cuerpo tiene interlineado 1.45. La paleta cálida es parte de la
dirección editorial; no se sustituyó por una estética de producto tecnológico.
Los cambios de ancho animados solo afectan una barra pequeña y se desactivan
con movimiento reducido.

## Límites de la comprobación

La revisión funcional se realizó en Chromium. No se probó físicamente en un
proyector ni en todos los navegadores. En móvil se prioriza lectura con scroll;
para exponer, usar escritorio en pantalla completa. GitHub es el único enlace
que requiere conexión; los archivos de evidencia se incluyen localmente.

## Actualización: los amigos de NAO

La presentación tiene ahora 14 diapositivas. Se retiraron las antiguas 13 y 15,
se conservó la sección de limitaciones y se añadió un cierre para ejecutar
probar_camara.py. Se revisaron los 14 pasos en 1440×900 y 375×812, sin
desbordamientos horizontales ni errores JavaScript. La demo usa la cámara del
computador y no se presenta como una integración ya realizada con NAO.
