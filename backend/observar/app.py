from flask import Flask 
from flask import render_template, request, redirect, url_for, session                    
from flaskext.mysql import MySQL
from flask import send_from_directory   
from flask_login import LoginManager                              
import os




app = Flask(__name__)   
app.secret_key = 'your secret key'                                                         

mysql = MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost' 
app.config['MYSQL_DATABASE_USER']='root' 
app.config['MYSQL_DATABASE_PASSWORD']='' 
app.config['MYSQL_DATABASE_DB']='galeria' 
mysql.init_app(app) 

carpeta = os.path.join('uploads')
app.config['CARPETA']= carpeta                                                                  



####HOME###############################
@app.route('/')
def home():
    sql = "SELECT nombre, apellido FROM fotografos;"                                          
    conn= mysql.connect()                                                                   
    cursor= conn.cursor()                                                                   
    cursor.execute(sql)                                                                     
    galeria = cursor.fetchall()                                                                 
    conn.commit()      
    return render_template('galeria/home.html', galeria = galeria)


####MOSTRAR###############################
@app.route('/index')                                                                        
def index():
    sql = "SELECT articulo.*, fotografos.nombre, fotografos.apellido FROM fotografos INNER JOIN articulo ON fotografos.idFotografo = articulo.Fotografo;"            
    conn= mysql.connect()                                                                   
    cursor= conn.cursor()                                                                
    cursor.execute(sql)                                                                     
    galeria = cursor.fetchall()                                                     
    conn.commit()                                                                        
    return render_template('galeria/index.html', galeria = galeria)                       

#..................MOSTRAR FOTO............................#
@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

######ELIMINAR##########################
@app.route('/destroy/<int:id>')                                                             
def destroy(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    
#................ELiminacion de foto en carpeta..................
    cursor.execute("SELECT foto FROM articulo WHERE id_art=%s", id)                         
    fila = cursor.fetchall()
    print(fila)                                                                             
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))                              
#................ELiminacion de registo..................    
    cursor.execute("DELETE FROM articulo where id_art=%s", (id))
    conn.commit()
    return redirect('/index')

######EDITAR##########################
@app.route('/edit/<int:id>')
def edit(id):
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute("SELECT * FROM articulo where id_art=%s", (id))
    galeria = cursor.fetchall()
    print(galeria)
    conn.commit()
    return render_template('galeria/edit.html', galeria = galeria)

@app.route('/update', methods=['POST'])
def update():
    titulo=request.form["textNombre"]
    fotografo=request.form["textFtg"]
    foto=request.files["textFoto"]
    id=request.form["textID"]

    datos=(titulo, fotografo, id)
    sql = "UPDATE articulo SET nombre_foto=%s , Fotografo=%s WHERE id_art=%s;"    


    conn= mysql.connect()
    cursor= conn.cursor()

    if foto.filename != '':
        foto.save("uploads/" + foto.filename)

        cursor.execute("SELECT foto FROM articulo WHERE id_art=%s", id)
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
        cursor.execute("UPDATE articulo SET foto=%s WHERE id_art=%s",(foto.filename,id))

        conn.commit()

    cursor.execute(sql, datos)
    conn.commit()
    return redirect('/index')

####CREAR###############################
@app.route('/create')
def create():
    sql = "SELECT nombre, apellido FROM fotografos;"
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql)                                                                     
    nombFotog = cursor.fetchall() 
    conn.commit()
    return render_template('galeria/create.html', nombFotog = nombFotog)
                                                                                                
@app.route('/store', methods=['POST'])                                                      
def storage():
    nombre=request.form["textNombre"]
    foto=request.files["textFoto"]
    fotografo=request.form["textFtg"]

    foto.save("uploads/" + foto.filename)                                                   
    sql = "INSERT INTO articulo VALUES (NULL,%s, %s, %s);"
    datos=(nombre, fotografo, foto.filename)
    
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql, datos)                                                              
    conn.commit()
    return redirect('/index')

#########################   Pagina de formulario y login  #########################

#........................... FORMULARIO ......................................

@app.route('/formulario')
def formulario():
    sql = "SELECT * FROM fotografos;"
    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql)                                                                     
    nombFotog = cursor.fetchall()
    conn.commit()
    return render_template('galeria/formulario.html', nombFotog = nombFotog)


@app.route('/mystore', methods=['POST'])                                                      
def mystorage():
    idFotog=request.form["textIdf"]
    nombre=request.form["textNom"]
    email=request.form["textEmail"]
    apellido=request.form["textApell"]
    user=request.form["textUser"]
    password=request.form["textPass"]

    sql = "INSERT INTO fotografos VALUES (%s,%s, %s, %s);"
    datos=(idFotog,nombre, email, apellido)

    conn= mysql.connect()
    cursor= conn.cursor()
    cursor.execute(sql, datos)   

    sql1 = "INSERT INTO login VALUES (%s, %s);"
    datos1=(user, password)    

    cursor.execute(sql1, datos1)                                                              
    conn.commit()
    return redirect('/index')

#........................... LOGIN ......................................

# Route for handling the login page logic
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM login WHERE usuario = %s AND pass = %s', (username, password))
        probando = cursor.fetchall()

        
        if probando:
            session['loggedin'] = True
            session['username'] = username
            session['password'] = password #Tengo problema con esto ya que me dice q acepta tuplas o integer
            msg = 'Logged in successfully !'
            return render_template('galeria/index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('galeria/login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))














































if __name__ == '__main__':                                                                      
    app.run(debug=True)