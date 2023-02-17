from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, RadioField, IntegerField
from wtforms.fields import EmailField

class BoxForm(Form):
    numeroCajas = IntegerField('Numero de cajas')
    cajas = FieldList(StringField('caja'), min_entries=1, max_entries=100)