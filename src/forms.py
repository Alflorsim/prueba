from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class registerForm(FlaskForm):
    username = StringField("Escribe tu username", validators=(DataRequired(), Length(min=4, max=25)))
    email = EmailField("Escribe tu email", validators=(DataRequired(), Length(min=4, max=25), Email()))
    password = PasswordField("Escribe tu contraseña", validators=(DataRequired(), Length(min=4, max=25)))
    submit = SubmitField("Crear usuario")

class loginForm(FlaskForm):
    username = StringField("Escribe tu username", validators=(DataRequired(), Length(min=4, max=25)))
    email = EmailField("Escribe tu email", validators=(DataRequired(), Length(min=4, max=25), Email()))
    password = PasswordField("Escribe tu contraseña", validators=(DataRequired(), Length(min=4, max=25)))
    submit = SubmitField("Crear usuario")

class contactForm(FlaskForm):
    nombre = StringField("Escribe tu nombre", validators=(DataRequired(), Length(min=4, max=25)))
    telefono = StringField("Escribe tu telefono", validators=(DataRequired(), Length(min=4, max=25)))
    descripcion = StringField("Escribe tu descripcion", validators=(DataRequired(), Length(min=4, max=255)))
    submit = SubmitField("Crear usuario")

class editcontactForm(FlaskForm):
    nombre = StringField("Escribe tu nombre", validators=(DataRequired(), Length(min=4, max=25)))
    telefono = StringField("Escribe tu telefono", validators=(DataRequired(), Length(min=4, max=25)))
    descripcion = StringField("Escribe tu descripcion", validators=(DataRequired(), Length(min=4, max=255)))
    submit = SubmitField("Crear usuario")