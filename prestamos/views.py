from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import login as auth_login, logout, authenticate
from .forms import FormularioSolicitante
from .models import Solicitante
import requests

moni_api_url = 'https://api.moni.com.ar/api/v4/scoring/pre-score/'
moni_api_credential = 'ZGpzOTAzaWZuc2Zpb25kZnNubm5u'

def listadoPrestamos(request):
    solicitantes = Solicitante.objects.all()
    return render(request, 'listadoPrestamos.html', {'solicitantes': solicitantes})

def cerrarSesion(request):
    logout(request)
    return redirect('home')

def iniciarSesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('listado-prestamos')

        else:
            return render(request, 'iniciarSesion.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o la contraseña son incorrectos'
            })
    else:
        return render(request, 'iniciarSesion.html', {'form': AuthenticationForm})

def consultarAPI(dni):
    url_api = f'{moni_api_url}{dni}'
    headers = {'credential': moni_api_credential}
    try:
        response = requests.get(url_api, headers=headers)
        return response.json()

    except requests.RequestException as e:
        raise Exception(f'Error al consultar la API: {e}')


def pedidoPrestamos(request):
    if request.method == 'POST':
        form = FormularioSolicitante(request.POST)
        if form.is_valid():
            dni = request.POST['dni']

            resultado_api = consultarAPI(dni)
            aprobado = resultado_api.get('status') == 'approve'

            Solicitante.objects.create(
                dni=dni,
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                genero=request.POST['genero'],
                email=request.POST['email'],
                monto=request.POST['monto'],
                aprobado=aprobado
            )

            mensaje = 'Su préstamo ha sido aprobado!' if aprobado else 'Su préstamo ha sido rechazado!'

            return render(request, 'formularioPrestamo.html', {'form': FormularioSolicitante, 'mensaje': mensaje})

        else:
            errores = form.errors
            return render(request, 'formularioPrestamo.html', {'form': form, 'errores': errores})
    else:
        return render(request, 'formularioPrestamo.html', {'form': FormularioSolicitante})

def editarSolicitante(request, solicitante_id):
    solicitante = get_object_or_404(Solicitante, pk=solicitante_id)
    if request.method == 'POST':
        formulario = FormularioSolicitante(request.POST, instance=solicitante)
        if formulario.is_valid():
            formulario.save()
            return redirect('listado-prestamos')
        else:
            return render(request, 'editarSolicitante.html', {'form': formulario, 'solicitante': solicitante})

    else:
        formulario = FormularioSolicitante(instance=solicitante)
        return render(request, 'editarSolicitante.html', {'form': formulario, 'solicitante': solicitante})

def eliminarSolicitud(request, solicitante_id):
    solicitante = get_object_or_404(Solicitante, pk=solicitante_id)
    if request.method == 'POST':
        solicitante.delete()
        return redirect('listado-prestamos')
    else:
        return HttpResponseBadRequest("Solicitud incorrecta")