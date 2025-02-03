from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)
print('hola munfo')
try:
    '''mydb = mysql.connector.connect(
      host="PauloHidalgo.mysql.pythonanywhere-services.com",
      user="PauloHidalgo",
      password="estoesunabasededatos",
      database="PauloHidalgo$tareas"
    )'''
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="estoesunabasededatos",
        database="tareas",
        port=3306
    )
    message = 'Estas conectado a la db'
    mycursor = mydb.cursor()
    #for x in myresult:
      #print(x)
except mysql.connector.Error as e:
    print(e)

    myresult = ['#']
    message = 'NO estas conectado a la db'

def add_tarea(tipo,detalle):
    query = "INSERT INTO lista (tipo,detalle) VALUES (%s, %s);"
    valores = (tipo,detalle)
    mycursor.execute(query, valores)
    mydb.commit()

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        tipo = request.form['tipo']
        detalle = request.form['detalle']
        add_tarea(tipo,detalle)
        print("asdfghjklñ")
    #return 'Hola desde flask!'
    mycursor.execute("SELECT * FROM lista")
    myresult = mycursor.fetchall()
    return render_template('index.html', mensaje =  message, resul = myresult)

@app.route('/cambio', methods = ['GET','POST'])
def cambio():
    print("en cambio")
    '''if request.method == 'POST':
        tipo = request.form['tipo']
        detalle = request.form['detalle']
        add_tarea(tipo,detalle)
        print("asdfghjklñ")
    #return 'Hola desde flask!'
    mycursor.execute("SELECT * FROM lista")
    myresult = mycursor.fetchall()
    return render_template('index.html', mensaje =  message, resul = myresult)'''
    return 'hola'