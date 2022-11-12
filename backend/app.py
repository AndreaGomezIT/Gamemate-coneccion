from flask import Flask 
from flask import render_template, request, redirect, url_for                    
from flaskext.mysql import MySQL
from flask import send_from_directory                                 
import os

app = Flask(__name__)                                                              
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost' 
app.config['MYSQL_DATABASE_USER']='root' 
app.config['MYSQL_DATABASE_PASSWORD']='' 
app.config['MYSQL_DATABASE_DB']='gamemate' 
mysql.init_app(app) 

carpeta = os.path.join('uploads')
app.config['CARPETA']= carpeta                                                                  




@app.route('/')
def home():
    return render_template('html/index.html')




######################## Formulario/Crear #############################################
@app.route('/formulario')
def registrar():
    return render_template('html/formulario.html')

@app.route('/store', methods=['POST'])                                                      
def store():
    nickname=request.form["user"]
    nombre=request.form["Nombre"]
    apellido=request.form["surname"]
    fechaNacimiento=request.form["bday"]
    provincia=request.form["prov"]
    horario=request.form["Horario"]
    email=request.form["email"]
    password=request.form["password"]
    foto=request.files["textFoto"]
    descripcion=request.form["descripcion"]    
    
    foto.save("uploads/" + foto.filename)                                                 
    sql = "INSERT INTO usuarios VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    datos=(nickname,nombre,apellido,fechaNacimiento,provincia,horario,email,password,foto.filename,descripcion)
    
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql, datos)                                                              
    conn.commit()
    return redirect('/')

######################## Login #############################################
@app.route('/login')
def login():
    return render_template('html/login.html')















if __name__ == '__main__':                                                                      
    app.run(debug=True)





