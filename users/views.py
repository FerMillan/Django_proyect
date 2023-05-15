import users
from users.models import Usuarios
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic.edit import UpdateView

# Forms
from .forms import CreateUsuarioForm, UsuarioLoginForm, UpdateUsuarioForm

### CLase View que sirve para Registrar un Usuario Nuevo (no Administrador)
class SignUp(View):
    """Página para crear una cuenta de Cliente"""
    
    # template = "users/create_client.html"
    
    def get(self, request):
        form = CreateUsuarioForm()
        context = {'form': form}
        return render(request, "accounts/signup.html", context)
        
    def post(self, request):
        form = CreateUsuarioForm(request.POST)
        
        if form.is_valid():            
            user = form.instance.tipo ='5'
            user = form.save()
            login(request, user)
            return redirect('home')
            
        else:
            return render( request, "accounts/signup.html", {'form': form})

### Clase View para poder iniciar sesión
class Login(View):
    """Página de inicio de sesion"""
    
    template = "accounts/login.html"

    def get(self, request):
        form = UsuarioLoginForm()
        context = {"form": form}
        #return render(request, self.template, context)
        return render(request, "accounts/login.html", {'form': form})

    def post(self, request):
        form = UsuarioLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd.get('username'), password=cd.get('password') )
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('home')
            else:
                messages.info(request, 
                              'Los datos no son correctos. Intenta de nuevo')
                return render(request, self.template, {'form': form,
                                                "contrib_messages":messages})
        else:
            messages.info(request, 'Asegurate de llenar los campos correctamente')
            return render(request, self.template, {'form': form, 'contrib_messages': messages})

### Clase View para poder cerrar sesión
class Logout(View):
    """Página de inicio de sesion"""
    template = "accounts/login.html"
    
    def get(self, request):
        logout(request)
        return redirect('home')

    def post(self, request):
        logout(request)
        return redirect('home')

### Clase View para mostrar la información del perfil
@login_required(login_url="/accounts/login/")
def perfil(request, pk,*args, **kwargs):
    data = Usuarios.objects.all()
    context = {"data": data}
    return render(request, "accounts/perfil.html", context)

@login_required(login_url="/accounts/login/")
def editar_perfil(request, pk):

    perfil = Usuarios.objects.get(id=pk)
    form_up = UpdateUsuarioForm(instance=perfil)
    context = {'form_up': form_up}
    if request.method == 'POST':
        form_up = UpdateUsuarioForm(request.POST, request.FILES, instance=perfil)
        if form_up.is_valid():
            # guardar perfil en la BD
            instance = form_up.save(commit=False)
            # instance.usuario = request.user
            instance.save()
            return redirect(f'/accounts/perfil/{perfil.id}')
    return render(request, "accounts/editar_perfil.html", context)

@login_required(login_url="/accounts/login/")
def crear_perfil(request, pk):

    perfil = Usuarios.objects.get(id=pk)
    form = UpdateUsuarioForm(instance=perfil)
    context = {'form': form}
    if request.method == 'POST':
        form = UpdateUsuarioForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            # guardar perfil en la BD
            instance = form.save(commit=False)
            # instance.usuario = request.user
            instance.save()
            return redirect(f'/accounts/perfil/{perfil.id}')
    return render(request, "accounts/crear_perfil.html", context)