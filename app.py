from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import time
import random
import json

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "finalpython"
client = MongoClient(
    "mongodb://deyxon:mafalu04@ds157956.mlab.com:57956/finalpython")
db = client.finalpython
app.secret_key = 'myscretkey'


@app.route('/')
def Index():
    return render_template('index.html')


@app.route('/guarda', methods=['POST'])
def add_guarda():
    if request.method == 'POST':
        idg = request.form['idg']
        nombre = request.form['nombreg']
        newGuarda = {
            "nombre": nombre,
            "id": idg,
            "infracciones": []
        }
        guarda = db.guardas.insert_one(newGuarda)
        flash('Guarda guardado correctamente')
        return redirect(url_for('Index'))


@app.route('/lst-guards')
def List():
    data = []
    cursor = db.guardas.find()
    for doc in cursor:
        data.append(doc)
    return render_template('lst-guardas.html', guarda=data)


@app.route('/detail-guarda/<id>')
def AddInfra(id):
    data = []
    print(id)
    guarda = db.guardas.find_one({"id": id})
    return render_template('add-infra.html', guarda=guarda)


@app.route('/view-guarda/<id>')
def ViewInfo(id):
    guarda = db.guardas.find_one({"id": id})
    return render_template('view.info.html', guarda=guarda)


@app.route('/summary')
def Summary():
    data = []
    cocepto1 = 0
    cocepto2 = 0
    cocepto3 = 0
    cocepto4 = 0
    cocepto5 = 0
    cursor = db.infracciones.find()
    for doc in cursor:
        data.append(json.dumps(doc))
    for concepto in data:
        print(data)
        if concepto == "Exceso de Velocidad":
            cocepto1 = cocepto1 + 1
        if concepto == "Sin pase":
            cocepto2 = cocepto2 + 1
        if concepto == "Conducir bajo la influencia del alcohol":
            cocepto3 = cocepto3 + 1
        if concepto == "Revisión Técnica vencida o rechazada":
            cocepto4 = cocepto4 + 1
        if concepto == "Conducir vehículo sin placa patente":
            cocepto5 = cocepto5 + 1
    print(cocepto1)
    print(cocepto2)
    print(cocepto3)
    print(cocepto4)
    print(cocepto5)
    return render_template('summary.html', data=data)


@app.route('/add-info/<id>/<nombre>', methods=['POST'])
def addinfra(id, nombre):
    if request.method == 'POST':
        print(request.form['placa'])
        documentToSupdate = {
            "id": random.randrange(1000),
            "placa": request.form['placa'],
            "identificacion": request.form['identificacion'],
            "fecha": time.strftime("%d/%m/%y"),
            "nombre": request.form['nombre'],
            "valor": request.form['valor'],
            "concepto": request.form['concepto']
        }
    guardas = db.guardas.update_one(
        {"id": id}, {"$push": {"infracciones": documentToSupdate}})
    documentToinf = {
        "id": random.randrange(1000),
        "placa": request.form['placa'],
        "identificacion": request.form['identificacion'],
        "fecha": time.strftime("%d/%m/%y"),
        "nombre": request.form['nombre'],
        "valor": request.form['valor'],
        "concepto": request.form['concepto'],
        "idguarda": id,
        "nombreg": nombre
    }
    db.infracciones.insert_one(documentToinf)
    return redirect(url_for('List'))


if __name__ == '__main__':
    app.run(port=4800, debug=True)
