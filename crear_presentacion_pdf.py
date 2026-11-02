from pathlib import Path
import base64
import io
import json
import textwrap

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'presentacion'
OUT.mkdir(exist_ok=True)
PDF = OUT / 'Presentacion_Deteccion_Peluches_YOLO.pdf'
BG, WHITE, MUTED, CYAN = '#101D32', '#F4F7FC', '#B5C5D9', '#39D8BE'
plt.rcParams.update({'font.family':'DejaVu Sans', 'text.color':WHITE, 'font.size':16})
slides = []

def slide(title, subtitle=''):
    f = plt.figure(figsize=(16,9), facecolor=BG)
    f.text(.055,.915,title,fontsize=29,weight='bold',va='top')
    if subtitle: f.text(.055,.845,subtitle,fontsize=15,color=MUTED,va='top')
    f.text(.055,.035,'UNIVERSIDAD EIA  /  FUNDAMENTOS DE INTELIGENCIA ARTIFICIAL',fontsize=9,color=MUTED)
    f.text(.945,.035,f'{len(slides)+1:02}',ha='right',fontsize=11,color=CYAN)
    slides.append(f)
    return f

def text(f,x,y,s,size=21,color=WHITE,width=48):
    lines='\n'.join(textwrap.fill(p,width=width) if p else '' for p in s.split('\n'))
    f.text(x,y,lines,fontsize=size,color=color,va='top',linespacing=1.5)

def card(f,x,y,w,h,title,body):
    f.add_artist(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.012',transform=f.transFigure,
                              facecolor='#1C304B',edgecolor='none',zorder=0))
    text(f,x+.018,y+h-.025,title,21,CYAN,width=int(w*75))
    text(f,x+.018,y+h-.11,body,17,width=int(w*84))

def source(f,s):
    f.text(.055,.078,s,fontsize=9,color=MUTED)

nb=json.loads((ROOT/'Entrenamiento_Peluches_YOLO_nano.ipynb').read_text(encoding='utf-8'))
embedded=[]
for c in nb['cells']:
    for o in c.get('outputs',[]):
        data=o.get('data',{}).get('image/png')
        if data:
            if isinstance(data,list): data=''.join(data)
            embedded.append(Image.open(io.BytesIO(base64.b64decode(data))).convert('RGB'))

f=slide('Reconocimiento de peluches con YOLO26 nano','Proyecto de visión artificial · Universidad EIA')
text(f,.06,.73,'Reconocer cuál de los\ntres peluches aparece',32,width=36)
text(f,.06,.55,'Un modelo entrenado con datos propios.',19,MUTED,width=42)
text(f,.06,.45,'INTEGRANTES',15,CYAN,width=42)
text(f,.06,.395,'Martin Restrepo\nSebastian Giraldo\nMiguel Zuleta\nJuan Jose Jaramillo\nJulian Mora\nSantiago Zuluaga',18,width=42)
text(f,.06,.12,'Datos → entrenamiento → validación → prueba',16,CYAN,width=70)
if embedded:
    ax=f.add_axes([.56,.28,.39,.46]); ax.imshow(embedded[0]); ax.axis('off')
    f.text(.57,.235,'Ejemplos etiquetados del notebook',fontsize=11,color=MUTED)

f=slide('El problema: reconocer cuál peluche aparece','Objetivo del proyecto: identificar cuál de los tres peluches se observa')
for x,t,b in [(.06,'Juan José','Clase 0\npeluche_Juan Jose'),(.365,'Martín','Clase 1\npeluche_martin'),(.67,'Sebastián','Clase 2\npeluche_sebastian')]:
    card(f,x,.42,.27,.32,t,b)
text(f,.065,.30,'Respuesta buscada: el nombre del peluche.',24,CYAN,width=70)
text(f,.065,.20,'YOLO también dibuja cajas como parte de su salida.\nEl objetivo del trabajo es reconocer el peluche.',18,MUTED,width=90)

f=slide('El recorrido completo del proyecto','De las fotografías a la evaluación del modelo que reconoce los peluches')
items=[('01 · Fotografiar','Capturar variedad de ángulos, distancias y fondos.'),('02 · Etiquetar','Marcar las cajas y clases en Roboflow.'),('03 · Preparar','Separar datos y aumentar solo entrenamiento.'),('04 · Entrenar','Ajustar los pesos con las imágenes de entrenamiento.'),('05 · Validar','Evaluar tras cada época y guardar el mejor modelo.'),('06 · Probar','Evaluar el modelo elegido con las imágenes de test.')]
for i,(t,b) in enumerate(items): card(f,.06+(i%3)*.305,.47-(i//3)*.30,.27,.245,t,b)
source(f,'Entrenamiento y validación se repiten por época. Validación y test no actualizan los pesos.')

f=slide('323 fotografías originales → 549 imágenes finales','Primero se separaron los originales; después se aumentó entrenamiento')
ax=f.add_axes([.08,.24,.56,.50],facecolor=BG)
import numpy as np
x=np.arange(3)
ax.bar(x-.17,[226,65,32],.32,color='#637C9E',label='Originales')
ax.bar(x+.17,[452,65,32],.32,color=CYAN,label='Finales')
for i,(a,b) in enumerate(zip([226,65,32],[452,65,32])):
    ax.text(i-.17,a+10,str(a),ha='center',fontsize=15); ax.text(i+.17,b+10,str(b),ha='center',fontsize=15)
ax.set_xticks(x,['Entrenamiento','Validación','Test']); ax.set_ylim(0,530)
ax.tick_params(colors=WHITE); ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color(MUTED); ax.set_yticks([]); ax.legend(frameon=False,fontsize=13)
text(f,.69,.69,'226 × 2 = 452',27,CYAN,width=20)
text(f,.69,.55,'Validación y test conservan su tamaño.',20,width=22)
text(f,.69,.36,'Negativas incluidas:\n36 train · 4 valid · 3 test',17,MUTED,width=27)
source(f,'Fuente: README.md y conteos del dataset. Las negativas ya están incluidas en los totales.')

f=slide('Etiquetado y variaciones de las imágenes','Aprendizaje supervisado: cada ejemplo tiene una respuesta correcta')
card(f,.06,.36,.42,.39,'Una caja en cinco valores','clase · centro_x · centro_y · ancho · alto\nEjemplo: 1  0.50  0.50  0.40  0.60\nCoordenadas relativas entre 0 y 1.')
card(f,.52,.36,.42,.39,'Aumentos en Roboflow','Volteo horizontal: 50 %\nRotación: ±10° · brillo: ±15 %\nExposición: ±10 % · desenfoque: hasta 1,5 px')
text(f,.07,.24,'Auto-Orient corrige la orientación. Cada original de train aporta una variante.',18,MUTED,width=92)
source(f,'Fuente: imagenes_peluchesv3/README.roboflow.txt. Etiqueta de ejemplo ilustrativa.')

f=slide('Notebook: preparar y comprobar antes de entrenar','Entrenamiento_Peluches_YOLO_nano.ipynb · Secciones 1–4')
card(f,.06,.43,.42,.31,'Configurar','Localizar carpetas. Elegir CUDA, MPS o CPU. Crear un YAML local con las rutas y clases.')
card(f,.52,.43,.42,.31,'Comprobar','Leer imágenes y etiquetas. Verificar clases y coordenadas. Buscar duplicados exactos con SHA256.')
text(f,.07,.31,'Inspección visual: seis fotografías con sus cajas reales.',23,CYAN,width=77)
text(f,.07,.20,'El hash no detecta fotos casi iguales. La revisión visual sigue siendo necesaria.',18,MUTED,width=88)

f=slide('Entrenar: adaptar conocimientos visuales previos','Sección 5 · Transferencia de aprendizaje desde yolo26n.pt')
card(f,.06,.42,.42,.33,'Configuración','50 épocas · imágenes de 640\nLotes de 4 · patience = 10\nSemilla = 42 · validación activada')
card(f,.52,.42,.42,.33,'Qué ocurre en cada lote','Predecir → comparar con etiquetas\nCalcular pérdida → actualizar pesos\nRepetir con más ejemplos')
text(f,.07,.30,'Validar mide el desempeño sin actualizar los pesos.',23,CYAN,width=77)
text(f,.07,.20,'Registro: 50 épocas en ≈15,9 min sobre Apple M5 Pro / MPS.',18,MUTED,width=88)
source(f,'Fuente: salidas guardadas del notebook. El tiempo depende del equipo utilizado.')

f=slide('Guardar el mejor modelo y revisar el aprendizaje','Secciones 5–6 · Del entrenamiento al archivo que utilizará la cámara')
text(f,.07,.72,'best.pt',43,CYAN,width=20)
text(f,.07,.59,'Pesos seleccionados según validación.\nNo necesariamente los de la última época.',22,width=43)
text(f,.07,.37,'Tamaño: ≈5,44 MB\nruns/peluches/train/weights/best.pt',17,MUTED,width=51)
card(f,.57,.34,.37,.40,'Qué revisar','Curvas de pérdidas y métricas.\nEjemplos de los lotes.\nSi train mejora y validación empeora, puede haber sobreajuste.')
text(f,.07,.20,'La cámara carga estos pesos: no necesita volver a entrenar.',20,CYAN,width=84)

f=slide('Evaluar el modelo utilizado para reconocer peluches','Métricas de YOLO: consideran la clase y las cajas que produce el detector')
for x,y,t,b in [(.06,.49,'Precisión','De las detecciones producidas, ¿cuántas son correctas?'),(.52,.49,'Recall','De los objetos presentes, ¿cuántos encuentra?'),(.06,.18,'IoU','Área compartida entre cajas dividida por su unión.'),(.52,.18,'mAP50–95','Resume detección con exigencias de IoU entre 0,50 y 0,95.')]:
    card(f,x,y,.42,.25,t,b)
source(f,'mAP no es porcentaje de imágenes correctas. Confianza es una puntuación, no una probabilidad garantizada.')

f=slide('Resultados registrados del modelo','Evaluación de best.pt con conf = 0,25 · No es una ejecución nueva')
ax=f.add_axes([.06,.36,.88,.38]); ax.axis('off')
tbl=ax.table(cellText=[['Validación','1,000','1,000','0,995','0,903'],['Test','0,996','1,000','0,995','0,895']],colLabels=['Conjunto','Precisión','Recall','mAP50','mAP50–95'],cellLoc='center',bbox=[0,0,1,1])
tbl.auto_set_font_size(False); tbl.set_fontsize(19)
for (r,c),cell in tbl.get_celld().items():
    cell.set_facecolor('#24435D' if r==0 else '#1C304B'); cell.set_edgecolor(BG); cell.get_text().set_color(CYAN if r==0 else WHITE)
text(f,.07,.26,'Validación: 65 imágenes / 61 objetos. Test: 32 imágenes / 29 objetos.',19,MUTED,width=90)
source(f,'Fuente: evaluaciones explícitas de las secciones 7 y 8 del notebook; salidas guardadas.')

f=slide('Resultados de YOLO para cada peluche','mAP50–95 por clase · Esta métrica también evalúa el ajuste de las cajas')
ax=f.add_axes([.18,.25,.72,.49],facecolor=BG)
y=np.arange(3)
for offset,vals,col,label in [(-.17,[.958,.894,.857],'#637C9E','Validación'),(.17,[.941,.893,.850],CYAN,'Test')]:
    ax.barh(y+offset,vals,height=.30,color=col,label=label)
    for yi,v in zip(y+offset,vals): ax.text(v+.012,yi,f'{v:.3f}',va='center',fontsize=14)
ax.set_yticks(y,['Juan José','Martín','Sebastián']); ax.invert_yaxis(); ax.set_xlim(0,1.06)
ax.set_xticks([0,.25,.5,.75,1]); ax.tick_params(colors=WHITE)
for sp in ax.spines.values(): sp.set_visible(False)
ax.legend(loc='upper center',bbox_to_anchor=(.5,-.13),ncol=2,frameon=False,fontsize=14)
source(f,'Fuente: salidas guardadas del notebook. Escala de 0 a 1.')

f=slide('Predicciones: observar qué responde el detector','Sección 9 · Dos ejemplos por clase, seleccionados del conjunto de test')
if embedded:
    ax=f.add_axes([.15,.17,.70,.61]); ax.imshow(embedded[-1]); ax.axis('off')
source(f,'Imagen real de la salida guardada del notebook. Las etiquetas se usan para seleccionar ejemplos, no como entrada al detector.')

with PdfPages(PDF,metadata={'Title':'Reconocimiento de peluches con YOLO26 nano','Author':'Martin Restrepo; Sebastian Giraldo; Miguel Zuleta; Juan Jose Jaramillo; Julian Mora; Santiago Zuluaga','Subject':'Fundamentos de Inteligencia Artificial'}) as pdf:
    for i,f in enumerate(slides):
        pdf.savefig(f,facecolor=f.get_facecolor())
        if i in (0,1,2,3,9,11): f.savefig(OUT/f'vista_{i+1:02}.png',dpi=90,facecolor=f.get_facecolor())
        plt.close(f)
print(f'PDF: {PDF}\nDiapositivas: {len(slides)}\nBytes: {PDF.stat().st_size}')
