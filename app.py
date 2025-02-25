from flask import Flask, render_template, request, jsonify,redirect, url_for
import mysql.connector

app = Flask(__name__)
print('hola mundo')

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
    valores = (int(valor), int(id))
    mycursor.execute(query, valores)
    mydb.commit()

def delete_element(id):#funcion que sirve para cambiar el estado de la tarea a terminado
    try:
        if not mydb.is_connected():
            mydb.reconnect()  # Reconecta si está desconectado

        query = "DELETE FROM lista WHERE id=%s;"
        valores = (int(id),)
        mycursor.execute(query, valores)
        mydb.commit()

    except mysql.connector.Error as err:
        print(f"Error en MySQL: {err}")  # Muestra errores en la consola

def update_tarea(id_tarea, tipo, detalle):
    query = "UPDATE lista SET tipo=%s, detalle=%s WHERE id=%s"
    mycursor.execute(query, (tipo, detalle, id_tarea))
    mydb.commit()
    #cursor.close()
    #conn.close()

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        tipo = request.form['tipo']
        detalle = request.form['detalle']
        add_tarea(tipo,detalle)
        return redirect(url_for('index'))
    mycursor.execute("SELECT * FROM lista")
    myresult = mycursor.fetchall()
    return render_template('index.html', mensaje =  message, resul = myresult)


@app.route('/cambio', methods=['POST'])

def cambio():
    #print("en cambio")
    id = request.form['id']
    valor = request.form['valor']
    #print("ID:", id)
    #print("Nuevo Valor:", valor)
    change_state(id, valor)  # Tu función para actualizar en la base de datos

    # Responde con un JSON para evitar errores en `fetch()`
    return (jsonify({"status": "success", "id": id, "valor": valor}))

@ app.route('/eliminar', methods=['POST'])
def eliminar():
    #print("en eliminacion")
    id = request.form['id']
    #print("ID:", id)
    delete_element(id)  # Tu función para actualizar en la base de datos

    # Responde con un JSON para evitar errores en `fetch()`
    return (jsonify({"status": "success", "id": id}))

@ app.route('/modificar', methods=['POST'])
def modificar():
    print("en modificacion")
    id = request.form['id']
    tipo = request.form['tipo']
    detalle = request.form['detalle']

    # Lógica para actualizar en la base de datos
    update_tarea(id, tipo, detalle)

    #return render_template('editar.html', id=id_tarea, tipo=tipo, detalle=detalle)
    return (jsonify({"status": "success", "id": id}))
