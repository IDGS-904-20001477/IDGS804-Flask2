from flask import Flask, render_template
from flask import request, flash, make_response
from flask_wtf.csrf import CSRFProtect

import forms
from cajasDinamicas import BoxForm

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
    if(request.method == 'POST' and words.validate()):
        btnGuardar = request.form.get('btnGuardar')
        btnTraducir = request.form.get('btnTraducir')
        if(btnGuardar == 'Guardar'):    
            file = open('palabras.txt', 'a')
            file.write('\n' + words.spanish.data.upper() + '\n' + words.english.data.upper())
            file.close()
        if(btnTraducir == 'Traducir'):
            opcion = request.form.get('translate')
            file = open('palabras.txt', 'r')
            palabras = [linea.rstrip('\n') for linea in file]
            if(opcion == 'spanish'):
                spanishWord = request.form.get('txtSpanish')
                for posicion in range(len(palabras)):
                    if(palabras[posicion] == spanishWord.upper()):
                        palabraEncontrada = palabras[posicion - 1]
            elif(opcion == 'english'):
                englishWord = request.form.get('txtEnglish')
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

if __name__ == "__main__":
    app.run(debug = True, port = 8080)