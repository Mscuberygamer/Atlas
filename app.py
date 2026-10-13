import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "cambia-esta-clave-en-produccion")

# Configura DATABASE_URL como variable de entorno para usar MySQL.
# Ejemplo: mysql+pymysql://usuario:clave@localhost/diccionario_anatomia
database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///diccionario_demo.db"  # Permite probar la app sin instalar MySQL.
)
if database_url.startswith("mysql://"):
    database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Concepto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False, unique=True)
    categoria = db.Column(db.String(80), nullable=False)
    resumen = db.Column(db.String(300), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    funciones = db.Column(db.Text, nullable=False)
    curiosidades = db.Column(db.Text, nullable=False)
    ubicacion = db.Column(db.String(200), nullable=False)
    emoji = db.Column(db.String(12), default="🔬")
    imagen_url = db.Column(db.String(500), nullable=True)


DATOS_INICIALES = [
    dict(nombre="Corazón", categoria="Órganos", resumen="Órgano muscular que impulsa la sangre por el cuerpo.",
         descripcion="El corazón es un órgano muscular hueco que funciona como una bomba. Sus contracciones mantienen la sangre en circulación y ayudan a llevar oxígeno y nutrientes a los tejidos.",
         funciones="Bombea sangre hacia los pulmones para intercambiar gases y hacia el resto del cuerpo para distribuir oxígeno y nutrientes. También contribuye a transportar productos de desecho.",
         curiosidades="Tiene cuatro cavidades: dos aurículas y dos ventrículos.\nSus válvulas ayudan a que la sangre avance en una sola dirección.\nSu ritmo cambia según la actividad, el descanso y las emociones.",
         ubicacion="En el tórax, entre los pulmones y ligeramente hacia la izquierda.", emoji="❤️",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Heart_anterior_view.jpg"),
    dict(nombre="Cerebro", categoria="Órganos", resumen="Órgano que coordina pensamientos, sentidos, memoria y movimientos.",
         descripcion="El cerebro forma parte del sistema nervioso central. Está compuesto por miles de millones de neuronas y otras células que procesan información y coordinan numerosas actividades del organismo.",
         funciones="Interpreta información sensorial, participa en el pensamiento, el aprendizaje, la memoria, las emociones, el lenguaje y el control de movimientos voluntarios.",
         curiosidades="Las neuronas se comunican mediante señales eléctricas y químicas.\nEl cerebro necesita un suministro continuo de oxígeno y glucosa.\nDistintas regiones colaboran para realizar tareas complejas.",
         ubicacion="Dentro del cráneo, protegido por huesos, membranas y líquido cefalorraquídeo.", emoji="🧠",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Brain_human_sagittal_section.svg"),
    dict(nombre="Pulmones", categoria="Órganos", resumen="Órganos respiratorios que intercambian oxígeno y dióxido de carbono.",
         descripcion="Los pulmones son dos órganos esponjosos del sistema respiratorio. En pequeños sacos llamados alvéolos, el oxígeno pasa a la sangre y el dióxido de carbono sale de ella para ser expulsado.",
         funciones="Permiten el intercambio de gases entre el aire y la sangre y colaboran con el equilibrio ácido-base del organismo.",
         curiosidades="El pulmón derecho suele tener tres lóbulos y el izquierdo dos.\nLos alvéolos ofrecen una gran superficie para intercambiar gases.\nEl diafragma es un músculo clave para respirar.",
         ubicacion="Dentro de la caja torácica, uno a cada lado del corazón.", emoji="🫁",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Lungs_diagram_simple.svg"),
    dict(nombre="Hígado", categoria="Órganos", resumen="Órgano que procesa nutrientes, produce bilis y transforma sustancias.",
         descripcion="El hígado es una glándula grande que participa en el metabolismo y en la eliminación o transformación de diversas sustancias. También produce bilis, que ayuda a digerir las grasas.",
         funciones="Procesa nutrientes absorbidos por el intestino, almacena glucógeno, produce proteínas importantes para la sangre y metaboliza medicamentos y otras sustancias.",
         curiosidades="Tiene una notable capacidad de regeneración parcial.\nProduce bilis, que se almacena en la vesícula biliar.\nRealiza cientos de tareas metabólicas.",
         ubicacion="En la parte superior derecha del abdomen, debajo del diafragma.", emoji="🟤",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Liver_anterior_view.png"),
    dict(nombre="Estómago", categoria="Órganos", resumen="Órgano que mezcla los alimentos con jugos digestivos.",
         descripcion="El estómago es un órgano muscular del aparato digestivo. Recibe los alimentos del esófago, los mezcla y los transforma en una mezcla semilíquida antes de que pasen al intestino delgado.",
         funciones="Almacena temporalmente comida, mezcla el contenido con ácido y enzimas, e inicia la digestión de proteínas.",
         curiosidades="Su revestimiento produce moco protector.\nEl ácido gástrico ayuda a descomponer alimentos y reduce muchos microorganismos.\nEl tiempo de vaciado depende del tipo de comida.",
         ubicacion="En la parte superior del abdomen, principalmente hacia la izquierda.", emoji="🍽️",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Stomach_diagram.svg"),
    dict(nombre="Riñones", categoria="Órganos", resumen="Filtran la sangre y ayudan a regular agua, sales y presión arterial.",
         descripcion="Los riñones son dos órganos que filtran la sangre para retirar desechos y producir orina. Además, regulan el equilibrio de líquidos y electrolitos.",
         funciones="Eliminan productos de desecho, regulan agua y sales, ayudan a controlar la presión arterial y participan en la producción de glóbulos rojos mediante señales hormonales.",
         curiosidades="Cada riñón contiene alrededor de un millón de nefronas, aunque la cifra varía.\nLa orina viaja a la vejiga por los uréteres.\nTambién ayudan a mantener el equilibrio ácido-base.",
         ubicacion="En la parte posterior del abdomen, a ambos lados de la columna.", emoji="🫘",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Kidney_anatomy.jpg"),
    dict(nombre="Fémur", categoria="Huesos", resumen="Hueso del muslo y el más largo del cuerpo humano.",
         descripcion="El fémur es un hueso largo y resistente que forma el esqueleto del muslo. Se articula con la pelvis en la cadera y con la tibia y la rótula en la rodilla.",
         funciones="Soporta y transmite cargas durante la postura y el movimiento, y sirve como punto de anclaje para músculos de la cadera y la pierna.",
         curiosidades="Es generalmente el hueso más largo y uno de los más fuertes del cuerpo.\nSu extremo superior participa en la articulación de la cadera.\nLa médula ósea puede participar en la formación de células sanguíneas.",
         ubicacion="Entre la cadera y la rodilla, en el muslo.", emoji="🦴",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Femur_-_anterior_view.png"),
    dict(nombre="Cráneo", categoria="Huesos", resumen="Estructura ósea que protege el encéfalo y sostiene la cara.",
         descripcion="El cráneo está formado por varios huesos unidos, en su mayoría, por articulaciones fibrosas llamadas suturas. Protege el encéfalo y da soporte a estructuras de la cara.",
         funciones="Protege el encéfalo, alberga órganos sensoriales y proporciona superficies de inserción para músculos.",
         curiosidades="En el adulto, muchos huesos del cráneo están unidos firmemente.\nLa mandíbula es el hueso móvil principal del cráneo.\nLas suturas permiten el crecimiento del cráneo durante el desarrollo.",
         ubicacion="En la cabeza.", emoji="💀",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Human_skull_side_simplified_%28bones%29.svg"),
    dict(nombre="Bíceps braquial", categoria="Músculos", resumen="Músculo de la parte anterior del brazo que flexiona el codo.",
         descripcion="El bíceps braquial es un músculo situado en la parte frontal del brazo. Tiene dos porciones de origen y participa en movimientos del codo y del antebrazo.",
         funciones="Ayuda a flexionar el codo y a girar la palma hacia arriba mediante la supinación del antebrazo. También contribuye a ciertos movimientos del hombro.",
         curiosidades="Su nombre alude a sus dos cabezas.\nTrabaja junto con otros músculos para mover el codo.\nLos ejercicios con carga deben adaptarse a la capacidad de cada persona.",
         ubicacion="En la parte anterior del brazo, entre hombro y codo.", emoji="💪",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Biceps_brachii_muscle06.png"),
    dict(nombre="Diafragma", categoria="Músculos", resumen="Músculo principal de la respiración que separa tórax y abdomen.",
         descripcion="El diafragma es un músculo ancho con forma de cúpula que separa las cavidades torácica y abdominal. Al contraerse, desciende y facilita la entrada de aire a los pulmones.",
         funciones="Es el principal músculo inspiratorio y también participa en acciones que aumentan la presión abdominal, como toser o levantar objetos.",
         curiosidades="Se mueve de forma automática la mayor parte del tiempo.\nLos nervios frénicos controlan su contracción.\nSu movimiento cambia la presión dentro del tórax.",
         ubicacion="Debajo de los pulmones, separando tórax y abdomen.", emoji="🌬️",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Diaphragm_%28Thoracic_cavity%29.svg"),
    dict(nombre="Piel", categoria="Sistemas", resumen="Órgano que recubre el cuerpo y actúa como barrera protectora.",
         descripcion="La piel es el órgano que cubre la superficie del cuerpo. Incluye la epidermis y la dermis; debajo se encuentra el tejido subcutáneo, asociado a sus funciones.",
         funciones="Protege frente al ambiente, ayuda a regular la temperatura, permite percibir estímulos y contribuye a evitar la pérdida excesiva de agua.",
         curiosidades="Es el órgano más extenso por superficie.\nEl sudor ayuda a enfriar el cuerpo al evaporarse.\nLa piel contiene receptores sensoriales y participa en la producción de vitamina D con luz solar.",
         ubicacion="Cubre la superficie externa de todo el cuerpo.", emoji="🖐️",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Skin.png"),
    dict(nombre="Intestino delgado", categoria="Órganos", resumen="Lugar principal donde se absorben la mayoría de los nutrientes.",
         descripcion="El intestino delgado es un tubo del aparato digestivo dividido en duodeno, yeyuno e íleon. Su pared tiene pliegues y vellosidades que aumentan la superficie de absorción.",
         funciones="Completa gran parte de la digestión y absorbe nutrientes, vitaminas, minerales y buena parte del agua ingerida.",
         curiosidades="Sus vellosidades aumentan la superficie interna.\nSe comunica con el estómago y el intestino grueso.\nSus movimientos ayudan a mezclar y desplazar el contenido.",
         ubicacion="En la cavidad abdominal, entre el estómago y el intestino grueso.", emoji="〰️",
         imagen_url="https://commons.wikimedia.org/wiki/Special:FilePath/Small_intestine_diagram.svg"),
]


@app.get("/")
def index():
    q = request.args.get("q", "").strip()
    categoria = request.args.get("categoria", "").strip()
    query = Concepto.query
    if q:
        patron = f"%{q}%"
        query = query.filter(or_(
            Concepto.nombre.ilike(patron),
            Concepto.resumen.ilike(patron),
            Concepto.descripcion.ilike(patron),
            Concepto.categoria.ilike(patron)
        ))
    if categoria:
        query = query.filter_by(categoria=categoria)
    conceptos = query.order_by(Concepto.nombre.asc()).all()
    categorias = [r[0] for r in db.session.query(Concepto.categoria).distinct().order_by(Concepto.categoria).all()]
    destacado = Concepto.query.filter_by(nombre="Corazón").first()
    return render_template("index.html", conceptos=conceptos, categorias=categorias,
                           q=q, categoria=categoria, destacado=destacado)


@app.get("/api/conceptos/<int:concepto_id>")
def detalle_api(concepto_id):
    c = db.session.get(Concepto, concepto_id)
    if not c:
        return jsonify({"error": "Concepto no encontrado"}), 404
    return jsonify({k: getattr(c, k) for k in
                    ["id", "nombre", "categoria", "resumen", "descripcion",
                     "funciones", "curiosidades", "ubicacion", "emoji", "imagen_url"]})


def inicializar():
    with app.app_context():
        db.create_all()
        if Concepto.query.count() == 0:
            for dato in DATOS_INICIALES:
                db.session.add(Concepto(**dato))
            db.session.commit()


inicializar()

if __name__ == "__main__":
    app.run(debug=True)
