from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods

from .forms import LoginForm



@require_http_methods(["GET", "POST"])
def login_user(request):

    if request.method == "GET":
        form = LoginForm()
        return render(request, "login.html", {'login_form': form})
    
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest(f"Formulario no válido: {form.errors}")

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Realiza la autenticación
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Registra el usuario en la sesión
            return redirect(reverse('giw_respuestas:index'))
        else:
            return HttpResponseBadRequest("Usuario o contraseña incorrectos")

@require_http_methods(["GET", "POST"])
def index(request):
    return HttpResponse("Login correcto.")