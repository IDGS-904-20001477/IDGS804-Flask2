from flask import Flask, render_template
from flask import request, flash, make_response
from flask_wtf.csrf import CSRFProtect

import forms
from cajasDinamicas import BoxForm
from forms import ResistenciaForm
import json

app = Flask(__name__)
csrf = CSRFProtect()
app.config['SECRET_KEY']="Esta es una clave encriptada"
csrf.init_app(app)
@app.route('/formprueba')
def formprueba():

    return render_template("formprueba.html")

@app.route('/Alumnos', methods=['GET', 'POST'])
def Alumnos():
    reg_alum = forms.UserForm(request.form)
    datos = list()
    if(request.method == 'POST'and reg_alum.validate()):
        datos.append(reg_alum.matricula.data)
        datos.append(reg_alum.nombre.data)
        print(reg_alum.matricula.data)
        print(reg_alum.nombre.data)

    return render_template('Alumnos.html', form = reg_alum, datos = datos)

@app.route('/cajas', methods=['GET', 'POST'])
def cajas():
    if(request.method == 'POST'):
        form1 = BoxForm(request.form)
        return render_template('cajasDinamicas.html', form=form1)
    else:
        form1 = BoxForm()
        return render_template('cajasDinamicas.html', form=form1)
    
@app.route('/resultados', methods=['POST'])
def resultados():
    form1 = BoxForm(request.form)
    numeros = [int(numero) for numero in form1.cajas.data]
    

    getRepetNums = lambda i, numeros: len([num for num in numeros if num == i])
    numRepetidos = [(i, getRepetNums(i, numeros)) for i in set(numeros) if getRepetNums(i, numeros) > 1]

    return render_template('resultadoCajas.html', numeros=numeros, minNum=min(numeros), maxNum=max(numeros), promedio=sum(numeros) / len(numeros), numRepetidos=numRepetidos)

@app.route('/traductor', methods=['GET', 'POST'])
def traductor():
    words = forms.WordsForm(request.form)
    palabraEncontrada = ''
    if(request.method == 'POST'):
        btnGuardar = request.form.get('btnGuardar')
        btnTraducir = request.form.get('btnTraducir')
        if(btnGuardar == 'Guardar' and words.validate()):
            file = open('palabras.txt', 'a')
            file.write('\n' + words.spanish.data.upper() + '\n' + words.english.data.upper())
            file.close()
        if(btnTraducir == 'Traducir'):
            palabraEncontrada = 'No existe una coincidencia'
            opcion = request.form.get('translate')
            file = open('palabras.txt', 'r')
            palabras = [linea.rstrip('\n') for linea in file]
            if(opcion == 'spanish'):
                spanishWord = request.form.get('txtText')
                for posicion in range(len(palabras)):
                    if(palabras[posicion] == spanishWord.upper()):
                        palabraEncontrada = palabras[posicion - 1]
            elif(opcion == 'english'):
                englishWord = request.form.get('txtText')
                for posicion in range(len(palabras)):
                    if(palabras[posicion] == englishWord.upper()):
                        palabraEncontrada = palabras[posicion + 1]
                        print(palabraEncontrada)

    return render_template('traductor.html', form = words, palabraEncontrada = palabraEncontrada)

@app.route('/cookie', methods=['GET', 'POST'])
def cookie():
    reg_user = forms.LoginForm(request.form)
    response = make_response(render_template('cookie.html', form = reg_user))

    if(request.method == 'POST' and reg_user.validate()):
        user = reg_user.username.data
        password = reg_user.password.data
        datos = user + '@' + password
        success_message = 'Bienvenido {}'.format(user)
        response.set_cookie('datos_usuario', datos)
        flash(success_message)
    return response

@app.route('/resistencias')
def index():
    form = ResistenciaForm(request.form)
    return render_template('resistencias.html', form=form)

@app.route('/resistencias', methods=['POST'])
def calcular():
    banda1 = request.form['banda1']
    banda2 = request.form['banda2']
    banda3 = request.form['banda3']
    tolerancia = request.form['tolerancia']
    colors = ['negro', 'cafe', 'rojo', 'naranja', 'amarillo',
               'verde', 'azul', 'violeta', 'gris', 'blanco']
    concat = str(banda1) + str(banda2)
    valor = float(concat) * float(banda3)

    if tolerancia == '1':
        valor_min = valor - (valor * 0.05)
        valor_max = valor + (valor * 0.05)
    elif tolerancia == '2':
        valor_min = valor - (valor * 0.1)
        valor_max = valor + (valor * 0.1)
    else:
        valor_min = valor * 0.2
        valor_max = valor * 0.2

    filename='registros.json'
    
    with open(filename, 'r') as f:
        data = json.load(f)

    if isinstance(data, list):
        data.append({'valor': str(valor), 
            'min': str(valor_min), 
            'max': str(valor_max), 
            'color1': colors[int(banda1)], 
            'color2': colors[int(banda2)], 
            'color3': colors[len(banda3)-1]})
    else:
        data = [{'valor': str(valor), 
            'min': str(valor_min), 
            'max': str(valor_max), 
            'color1': colors[int(banda1)], 
            'color2': colors[int(banda2)], 
            'color3': colors[len(banda3)-1]}]

    with open(filename, 'w') as f:
        json.dump(data, f)

    return render_template('resistencias.html', history=data)



if __name__ == "__main__":
    app.run(debug = True, port = 8080)