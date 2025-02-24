from flask import Flask, render_template, request
import mysql.connector
from flask import jsonify

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

def change_state(id,valor):#funcion que sirve para cambiar el estado de la tarea a terminado
    query = "UPDATE lista SET estado=%s WHERE id=%s;"

  #  UPDATE Customers
 #   SET ContactName = 'Alfred Schmidt', City= 'Frankfurt'
#WHERE CustomerID = 1;
    '''if valor == "0":
        print("se cambio a 1")
        valor = 1
    else:
        print("se cambio a 0")
        valor = 0'''
    valores = (int(valor), int(id))
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

'''@app.route('/cambio', methods = ['GET','POST'])
def cambio():
    print("en cambio")
    if request.method == 'POST':
        id = request.form['id']
        valor = request.form['valor']
        print("asdfghjklñ")
        print(id)
        print(valor)
        change_state(id,valor)
    mycursor.execute("SELECT * FROM lista")
    myresult = mycursor.fetchall()
    return render_template('index.html', mensaje =  message, resul = myresult)'''



@app.route('/cambio', methods=['POST'])
def cambio():
    print("en cambio")
    id = request.form['id']
    valor = request.form['valor']
    print("ID:", id)
    print("Nuevo Valor:", valor)
    change_state(id, valor)  # Tu función para actualizar en la base de datos

    # Responde con un JSON para evitar errores en `fetch()`
    return jsonify({"status": "success", "id": id, "valor": valor})
