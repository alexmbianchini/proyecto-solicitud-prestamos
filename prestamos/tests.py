from django.test import TestCase
from django.contrib.auth.models import User
from .models import Solicitante
# Create your tests here.

class InicioSesionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuariotest', password='passusuariotest')

    def test_iniciar_sesion_exito(self):
        respuesta = self.client.post('/login/', {'username': 'usuariotest', 'password':  'passusuariotest'})
        self.assertEquals(respuesta.status_code, 302)

    def test_iniciar_sesion_falla(self):
        respuesta = self.client.post('/login/', {'username': 'otrousuario', 'password': 'otrapass'})
        self.assertEquals(respuesta.status_code, 200)
        self.assertContains(respuesta, 'El usuario o la contraseña son incorrectos')



class SolicitudPrestamo(TestCase):
    def test_solicitud_prestamo_exito(self):
        respuesta = self.client.post('/pedido-prestamo/', {'dni': '41525402', 'nombre': 'Alex', 'apellido': 'Bianchini', 'genero': 'M', 'email': 'alex@gmail.com', 'monto': 150000})
        self.assertEquals(respuesta.status_code, 200)

    def test_solicitud_prestamo_fallo_verificaciones(self):
        respuesta = self.client.post('/pedido-prestamo/', {'dni': '4152', 'nombre': 'Alex4', 'apellido': 'Bianchini4', 'genero': 'H', 'email': 'alexgmail.com', 'monto': 150000})
        self.assertEquals(respuesta.status_code, 200)

        self.assertTrue('errores' in respuesta.context)

        self.assertContains(respuesta, 'El DNI debe tener entre 7 y 8 caracteres.')


class EditarPrestamo(TestCase):
    def setUp(self):
        self.solicitante = Solicitante.objects.create(dni='41525402', nombre='Alex', apellido='Bianchini', genero='M', email='alex@gmail.com', monto=15000)

    def test_edicion_solicitante_exito(self):
        respuesta = self.client.post(f'/listado-prestamos/{self.solicitante.id}/', {'dni': '26643518', 'nombre': 'Alex Maximiliano', 'apellido': 'Bianchini', 'genero': 'M', 'email': 'alex@hotmail.com', 'monto': 80000})
        self.assertEquals(respuesta.status_code, 302)

        solicitante_editado = Solicitante.objects.get(id=self.solicitante.id)
        self.assertEquals(solicitante_editado.dni, 26643518)
        self.assertEquals(solicitante_editado.nombre, 'Alex Maximiliano')
        self.assertEquals(solicitante_editado.email, 'alex@hotmail.com')
        self.assertEquals(solicitante_editado.monto, 80000)