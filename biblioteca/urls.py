from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # URLs para Bibliografías
    path("bibliografias/", views.tipo_bibliografia_list, name="tipo_bibliografia_list"),
    path(
        "bibliografias/crear/",
        views.tipo_bibliografia_create,
        name="tipo_bibliografia_create",
    ),
    path(
        "bibliografias/<int:pk>/editar/",
        views.tipo_bibliografia_update,
        name="tipo_bibliografia_update",
    ),
    path(
        "bibliografias/<int:pk>/eliminar/",
        views.tipo_bibliografia_delete,
        name="tipo_bibliografia_delete",
    ),
    # URLs para Editoras
    path("editoras/", views.editora_list, name="editora_list"),
    path("editoras/crear/", views.editora_create, name="editora_create"),
    path("editoras/<int:pk>/editar/", views.editora_update, name="editora_update"),
    path("editoras/<int:pk>/eliminar/", views.editora_delete, name="editora_delete"),
    # URLs para Idiomas
    path("idiomas/", views.idioma_list, name="idioma_list"),
    path("idiomas/nuevo/", views.idioma_create, name="idioma_create"),
    path("idiomas/<int:pk>/editar/", views.idioma_update, name="idioma_update"),
    path("idiomas/<int:pk>/eliminar/", views.idioma_delete, name="idioma_delete"),
    # URLs para Autores
    path("autores/", views.autor_list, name="autor_list"),
    path("autores/nuevo/", views.autor_create, name="autor_create"),
    path("autores/<int:pk>/editar/", views.autor_update, name="autor_update"),
    path("autores/<int:pk>/eliminar/", views.autor_delete, name="autor_delete"),
    # URLs para Libros
    path("libros/", views.libro_list, name="libro_list"),
    path("libros/nuevo/", views.libro_create, name="libro_create"),
    path("libros/<int:pk>/editar/", views.libro_update, name="libro_update"),
    path("libros/<int:pk>/eliminar/", views.libro_delete, name="libro_delete"),
    # URLs para Empleados
    path("empleados/", views.empleado_list, name="empleado_list"),
    path("empleados/nuevo/", views.empleado_create, name="empleado_create"),
    path("empleados/<int:pk>/editar/", views.empleado_update, name="empleado_update"),
    path("empleados/<int:pk>/eliminar/", views.empleado_delete, name="empleado_delete"),
    # URLs para Préstamos
    path("prestamos/", views.prestamo_list, name="prestamo_list"),
    path("prestamos/nuevo/", views.prestamo_create, name="prestamo_create"),
    path("prestamos/<int:pk>/editar/", views.prestamo_update, name="prestamo_update"),
    path("prestamos/<int:pk>/eliminar/", views.prestamo_delete, name="prestamo_delete"),
    path("buscar_libros/", views.buscar_libros, name="buscar_libros"),
    path('reporte_rentas/', views.reporte_rentas, name='reporte_rentas')
]
