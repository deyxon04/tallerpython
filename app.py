from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

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


@app.route('/addinf/<string:id>')
def AddInfra(id):
    guarda = db.guardas.update_one({'_id':id}, {"name":"name"})
    # newGuarda = {
    #     "nombre": nombre,
    #     "id": idg,
    #     "infracciones": []
    # }
    print(id)
    return  render_template('add-infra.html')


if __name__ == '__main__':
    app.run(port=3000, debug=True)
