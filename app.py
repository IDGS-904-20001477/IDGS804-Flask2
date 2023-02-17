from flask import Flask, render_template
from flask import request
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
def alumnos():
    reg_alum = forms.UserForm(request.form)
    if(request.method == 'POST'):
        print(reg_alum.matricula.data)
        print(reg_alum.nombre.data)
    return render_template('Alumnos.html', form=reg_alum)

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
    
    numRepetidos = []

    for i in set(numeros):
        rep = len([num for num in numeros if num == i])
        if rep > 1:
            numRepetidos.append((i, rep))

    return render_template('resultadoCajas.html', numeros=numeros, minNum=min(numeros), maxNum=max(numeros), promedio=sum(numeros) / len(numeros), numRepetidos=numRepetidos)


if __name__ == "__main__":
    app.run(debug = True, port = 8080)