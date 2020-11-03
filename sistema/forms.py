from django import forms
#from django.contrib.auth.forms import UserCreationForm
#from .models import CustomUser
class ContactForm(forms.Form):
    mensaje = forms.CharField(max_length=500,
    widget=forms.Textarea(attrs={'rows': 2, 'cols': 75, 'placeholder':'Escribe aqui tu comentario'}), label='')
    flag = forms.CharField(widget=forms.HiddenInput())
    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        mensaje = cleaned_data.get('mensaje')
        if not mensaje:
            raise forms.ValidationError('El campo mensaje no puede estar vacío')
class ResponseForm(forms.Form):
    respuesta = forms.CharField(max_length=500,
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 75, 'placeholder':'Escribe aquí tu respuesta a este comentario'}),
        label='',)
    primarkey = forms.UUIDField(widget=forms.HiddenInput())
    flag = forms.CharField(widget=forms.HiddenInput())
    def clean(self):
        cleaned_data = super(ResponseForm, self).clean()
        respuesta = cleaned_data.get('respuesta')
        if not respuesta:
            raise forms.ValidationError('El campo respuesta no puede estar vacío')

class SignInForm(forms.Form):
    usuario = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Escribe tu nombre de usuario',
                                                        'class':'input-lg form-control'}))
    password = forms.CharField(max_length=45,
        widget=forms.PasswordInput(attrs={'placeholder': 'Escribe aqui tu contraseña','class':'input-lg form-control'}))
    flag = forms.CharField(widget=forms.HiddenInput())
    def clean(self):
        cleaned_data = super(SignInForm, self).clean()
        usuario = cleaned_data.get('usuario')
        password = cleaned_data.get('password')
        if not usuario or not password:
            raise forms.ValidationError('Los campos usuario y/o password no pueden estar vacios')

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Escribe tu nombre de usuario',
                                                        'class':'input-lg form-control'}))
    password = forms.CharField(max_length=45,
        widget=forms.PasswordInput(attrs={'placeholder': 'Escribe aqui tu contraseña','class':'input-lg form-control'}))
    password2 = forms.CharField(max_length=45,
        widget=forms.PasswordInput(attrs={'placeholder': 'Escribe otra vez tu contraseña','class':'input-lg form-control'}))
    email = forms.CharField(max_length=60, widget=forms.EmailInput(attrs={'placeholder': 'Escribe tu correo electrónico',
                                                            'class':'input-lg form-control'}))
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Escribe tu nombre(s)',
                                                            'class':'input-lg form-control'}))
    firstLastName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Escribe tu apellido paterno',
                                                            'class': 'input-lg form-control'}))

    secondLastName = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Escribe tu apellido materno',
                                                            'class': 'input-lg form-control'}))
    flag = forms.CharField(widget=forms.HiddenInput())
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')
        name = cleaned_data.get('name')
        firstLastName = cleaned_data.get('firstLastName')
        secondLastName = cleaned_data.get('secondLastName')
        if not username or not password or not password2 or not email or not name or not firstLastName or not secondLastName :
            raise forms.ValidationError('Por favor llene todos los campos')
        if password != password2:
            raise forms.ValidationError('Las contraseñas no pueden ser diferentes')
class PostForm(forms.Form):
    postTitle = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Escribe el título de la publicación',
                                                                             'class': 'input-lg form-control'}))
    postDescription = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 2, 'cols': 30, 'placeholder':'Escribe la descripción de la publicación',
                                                                                   'class':'input-lg form-control'}))
    link = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'link de la publicación',
                                                              'class': 'input-lg form-control'}))
    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        postTitle = cleaned_data.get('postTitle')
        link = cleaned_data.get('link')
        #postDescription = cleaned_data.get('postDescription')
        if not postTitle or not link:
            raise forms.ValidationError('Por favor llene todos los campos')
class CommentRepliesForm(forms.Form):
    commentid = forms.UUIDField(widget=forms.HiddenInput())
    flag = forms.CharField(widget=forms.HiddenInput())

class DateInput(forms.DateInput):
    input_type = 'date'

class SearchForm(forms.Form):
    name = forms.CharField(max_length=50,widget=forms.TextInput())
    def clean(self):
        cleaned_data = super(SearchForm, self).clean()
        name = cleaned_data.get('name')
        if not name:
            raise forms.ValidationError('Llena el campo por favor')
