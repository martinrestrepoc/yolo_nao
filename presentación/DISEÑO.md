# Diseño de la presentación

## Encargo y contenido

Presentación HTML en español basada en el README del proyecto. La audiencia se
asume académica, familiarizada con el proyecto pero no necesariamente con YOLO.
El objetivo es explicar el proceso y respaldar la elección de nano sin afirmar
que un modelo mayor siempre rinde peor. No se inventan integrantes ni institución.

## Dirección definida con UI UX Pro Max

Se consultaron el sistema visual, gráficas de comparación y navegación web.
La referencia pertinente fue Swiss Modernism: retícula clara, alineación,
composición editorial y jerarquía tipográfica. Los patrones de portfolio y
cyberpunk devueltos por búsquedas generales no correspondían al encargo y no se
aplicaron. La consulta específica de comparación recomendó barras con etiquetas
directas; se usan barras horizontales con escala 0–100 y una tabla equivalente.

La presentación adopta papel cálido (#f4f1e9), tinta verde oscura (#202f2b),
verde (#34634e) y terracota (#ad462b). El color viene del entorno de las fotos y
ayuda a separar datos, sin hacer del proyecto una interfaz de ciencia ficción.
Barlow Condensed aporta títulos compactos; Fira Sans sostiene texto y datos.
Las fuentes se alojan en assets/fonts para uso sin conexión.

## Composición y navegación

Una idea por diapositiva. Fotografías auténticas, cifras grandes solo cuando
son la evidencia central y diagramas de datos editables. Sin paneles decorativos
repetidos. El navegador debe abrir index.html directamente, sin instalación.

Flechas y espacio avanzan, Home/End van a los extremos, I abre el índice,
N muestra notas del expositor, F activa pantalla completa y P imprime.
La URL conserva la diapositiva. Botones con foco visible, movimiento reducido,
contenido desplazable en móvil e impresión en formato de diapositivas.

## Restricciones de verdad

El split precede al aumento x2; validación y test no se aumentan. 323 originales
pasan a 549 imágenes: 452/65/32. La época 45 y 0.90644 pertenecen a validación
durante entrenamiento; 0.903 es la reevaluación posterior a conf=0.25.
Los tres tamaños comparten dataset; el experimento de balanceo exacto usa una
división diferente. Las fotos casi iguales no se agruparon automáticamente.
Las muestras de inferencia son estáticas, no una cámara activa en la web.

## Revisión posterior

Aplicar Impeccable polish al HTML ya construido: revisar contraste, jerarquía,
contenidos, teclado, límites de navegación, vista móvil y versión de impresión.
Registrar la revisión en revisión/ sin modificar el diseño por recomendaciones
que contradigan la finalidad de una presentación.

## Ajuste de narrativa

El usuario definió a los peluches como los amigos que NAO quiere reconocer.
Se enfoca la portada y las clases en ese objetivo, sin afirmar que el detector
ya esté integrado en el robot. Se eliminaron las diapositivas originales 13 y
15. El cierre actual invita a la demostración con probar_camara.py mediante un
comando copiable. La presentación tiene 14 diapositivas.
