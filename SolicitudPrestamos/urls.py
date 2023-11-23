from django.contrib import admin
from django.urls import path
from prestamos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.iniciarSesion, name='home'),
    path('listado-prestamos/', views.listadoPrestamos, name='listado-prestamos'),
    path('listado-prestamos/<int:solicitante_id>/', views.editarSolicitante, name='editar-solicitante'),
    path('listado-prestamos/<int:solicitante_id>/delete', views.eliminarSolicitud, name='eliminar-solicitud'),
    path('logout/', views.cerrarSesion, name='logout'),
    path('login/', views.iniciarSesion, name='login'),
    path('pedido-prestamo/', views.pedidoPrestamos, name='pedido-prestamo')
]
