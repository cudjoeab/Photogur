from django.forms import CharField, PasswordInput, Form, ModelForm 

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())

class PictureForm(Form):
    title = CharField(max_length=255)
    artist = CharField(max_length=255)
    url = CharField(max_length=255) 
