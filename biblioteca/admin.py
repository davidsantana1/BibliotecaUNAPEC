from django.contrib import admin
from .models import (
    User,
    TipoBibliografia,
    Editora,
    Idioma,
    Autor,
    Libro,
    Empleado,
    PrestamoDevolucion,
)

# Register your models here.
admin.site.register(User)
admin.site.register(TipoBibliografia)
admin.site.register(Editora)
admin.site.register(Idioma)
admin.site.register(Autor)
admin.site.register(Libro)
admin.site.register(Empleado)
admin.site.register(PrestamoDevolucion)
