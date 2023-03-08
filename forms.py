from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, RadioField, PasswordField
from wtforms import validators
from wtforms.fields import EmailField

def My_Validation(form, field):
    if len(field.data) == 0:
        raise validators.ValidationError('El campo no tiene datos')

class UserForm(Form):
    matricula = StringField('Matricula', [
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=5, max=10, message='Ingresa min 5 max 10')
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo nombre es requerido')
    ])
    apaterno = StringField('Apaterno', [
        My_Validation
    ])
    amaterno = StringField('Amaterno')
    email = EmailField('Correo')

class WordsForm(Form):
    spanish = StringField('Spanish', [validators.DataRequired(message='El campo es requerido')])
    english = StringField('English', [validators.DataRequired(message='El campo es requerido')])

class LoginForm(Form):
    username = StringField('usuario', [
        validators.DataRequired(message='El campo Usuario es requerido'),
        validators.length(min = 5, max = 20, message = 'Ingresa min 5 max 10')
    ])
    password = PasswordField('Contrasenia', [
        validators.DataRequired(message = 'El campo Contrasenia es requerido'),
        validators.length(min = 5, max = 10, message = 'El campo Contrasenia es requerido')
    ])

colores = [("negro", "Negro"), ("marron", "Marrón"), ("rojo", "Rojo"), ("naranja", "Naranja"),
                      ("amarillo", "Amarillo"), ("verde", "Verde"), ("azul", "Azul"), ("violeta", "Violeta"),
                      ("gris", "Gris"), ("blanco", "Blanco")]

tolerancia_color = [("oro", "Oro"), ("plata", "Plata")]
class ResistenciaForm(Form):
    banda1 = SelectField('Banda1', choices=[(0, 'negro'), (1, 'cafe'), (2, 'rojo'), (3, 'naranja'), (4, 'amarillo'),
               (5, 'verde'), (6, 'azul'), (7, 'violeta'), (8, 'gris'), (9, 'blanco')])
    banda2 = SelectField('Banda2', choices=[(0, 'negro'), (1, 'cafe'), (2, 'rojo'), (3, 'naranja'), (4, 'amarillo'),
               (5, 'verde'), (6, 'azul'), (7, 'violeta'), (8, 'gris'), (9, 'blanco')])
    banda3 = SelectField('Banda3', choices=[(1, 'negro'), (10, 'cafe'), (100, 'rojo'), (1000, 'naranja'), (10000, 'amarillo'),
               (100000, 'verde'), (1000000, 'azul'), (10000000, 'violeta'), (100000000, 'gris'), (1000000000, 'blanco')])
    tolerancia = RadioField('Tolerancia', choices=[(1, "Oro"), (2, "Plata"), (3, 'Ninguno')])