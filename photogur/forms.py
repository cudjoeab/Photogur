from django.forms import CharField, PasswordInput, Form, ModelForm 

class LoginForm(Form):
    username = CharField(label="User Name", max_length=64)
    password = CharField(widget=PasswordInput())