  
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# settings
app.secret_key = "mysecretkey"

#Metodo para mi pagina principal
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM materias')
    data = cur.fetchall()
    cur.close()
    return render_template("index.html", materias = data)

@app.route('/add_materia', methods=['POST'])
def add_materia():
    if request.method == 'POST':
        nombre = request.form['nombre']
        calificacion = request.form['calificacion']
        estatus = request.form['estatus']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO materias (nombre, calificacion, estatus) VALUES (%s,%s,%s)", (nombre, calificacion, estatus))
        mysql.connection.commit()
        flash("Materia agregada satisfactoriamente")
        return redirect(url_for("Index"))

#Metodo para obtener el contacto a editar
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_materia(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM materias WHERE id_materia = %s", (id,))
    data = cur.fetchall()
    cur.close()
    return render_template('editar.html', materia = data[0])

#Metodo para editar el contacto 
@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        calificacion = request.form['calificacion']
        estatus = request.form['estatus']
        cur = mysql.connection.cursor()
        cur.execute("""UPDATE materias SET nombre = %s, calificacion = %s, estatus = %s WHERE id_materia = %s """, (nombre, calificacion, estatus, id))
        flash("Edicion realizada correctamente")
        mysql.connection.commit()
        return redirect(url_for('Index'))

#Metodo para borrar un registro
@app.route('/delete/<string:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM materias WHERE id_materia = {0}'.format(id))
    mysql.connection.commit()
    flash("Materia eliminada satisfactoriamente")
    return redirect(url_for('Index'))

# Conexion a Mysql 
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'calificaciones'
mysql = MySQL(app)

if __name__ == "__main__":
    app.run(port=3000, debug=True)