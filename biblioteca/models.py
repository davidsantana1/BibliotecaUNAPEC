from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    TIPO_PERSONA_CHOICES = [
        ("F", "Física"),
        ("J", "Jurídica"),
    ]

    cedula = models.CharField(max_length=11, unique=True)
    no_carnet = models.CharField(max_length=10, unique=True)
    tipo_persona = models.CharField(
        max_length=1, choices=TIPO_PERSONA_CHOICES, blank=True, default=""
    )
    estado = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="biblioteca_user_groups",  # Añade un related_name único
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="biblioteca_user_permissions",  # Añade un related_name único
        blank=True,
    )

    def __str__(self):
        return self.username  # o self.nombre si prefieres


class TipoBibliografia(models.Model):
    descripcion = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class Editora(models.Model):
    descripcion = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class Idioma(models.Model):
    descripcion = models.CharField(max_length=255)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class Autor(models.Model):
    nombre = models.CharField(max_length=255)
    pais_origen = models.CharField(max_length=255)
    idioma_nativo = models.ForeignKey(Idioma, on_delete=models.SET_NULL, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    descripcion = models.CharField(max_length=255)
    signatura_topografica = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    tipo_bibliografia = models.ForeignKey(
        TipoBibliografia, on_delete=models.SET_NULL, null=True
    )
    autores = models.ManyToManyField(Autor)
    editora = models.ForeignKey(Editora, on_delete=models.SET_NULL, null=True)
    ano_publicacion = models.PositiveIntegerField()
    ciencia = models.CharField(max_length=255)
    idioma = models.ForeignKey(Idioma, on_delete=models.SET_NULL, null=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion


class Empleado(models.Model):
    TIPOS_PERSONA = [
        ("fisica", "Física"),
        ("juridica", "Jurídica"),
    ]
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    no_carnet = models.CharField(max_length=10, unique=True)
    tipo_persona = models.CharField(max_length=10, choices=TIPOS_PERSONA)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.id})"


class PrestamoDevolucion(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    libro = models.ForeignKey(Libro, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    monto_por_dia = models.DecimalField(max_digits=6, decimal_places=2)
    cantidad_dias = models.PositiveIntegerField()
    comentario = models.TextField(null=True, blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"Prestamo {self.id} - {self.libro}"
