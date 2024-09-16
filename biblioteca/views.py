from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import ModelForm
from django.db import IntegrityError
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

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


class NewTipoBibliografiaForm(ModelForm):
    class Meta:
        model = TipoBibliografia
        fields = ["descripcion", "estado"]
        widgets = {
            "descripcion": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "estado": forms.CheckboxInput(attrs={"class": "form-check-input mb-2"}),
        }


class NewEditoraForm(ModelForm):
    class Meta:
        model = Editora
        fields = ["descripcion", "estado"]
        widgets = {
            "descripcion": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "estado": forms.CheckboxInput(attrs={"class": "form-check-input mb-2"}),
        }


class NewIdiomaForm(ModelForm):
    class Meta:
        model = Idioma
        fields = ["descripcion", "estado"]
        widgets = {
            "descripcion": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "estado": forms.CheckboxInput(attrs={"class": "form-check-input mb-2"}),
        }


class NewAutorForm(ModelForm):
    class Meta:
        model = Autor
        fields = ["nombre", "pais_origen", "idioma_nativo", "estado"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "pais_origen": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "idioma_nativo": forms.Select(attrs={"class": "form-select mb-2"}),
            "estado": forms.CheckboxInput(attrs={"class": "form-check-input mb-2"}),
        }


class NewLibroForm(ModelForm):
    class Meta:
        model = Libro
        fields = [
            "descripcion",
            "signatura_topografica",
            "isbn",
            "tipo_bibliografia",
            "autores",
            "editora",
            "ano_publicacion",
            "ciencia",
            "idioma",
            "estado",
        ]
        widgets = {
            "descripcion": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "signatura_topografica": forms.TextInput(
                attrs={"class": "form-control mb-2"}
            ),
            "isbn": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "tipo_bibliografia": forms.Select(attrs={"class": "form-select mb-2"}),
            "autores": forms.SelectMultiple(attrs={"class": "form-control mb-2"}),
            "editora": forms.Select(attrs={"class": "form-select mb-2"}),
            "ano_publicacion": forms.NumberInput(attrs={"class": "form-control mb-2"}),
            "ciencia": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "idioma": forms.Select(attrs={"class": "form-select mb-2"}),
            "estado": forms.CheckboxInput(attrs={"class": "form-check-input mb-2"}),
        }
        labels = {
            "descripcion": "Descripción",
            "signatura_topografica": "Signatura Topográfica",
            "tipo_bibliografia": "Tipo de Bibliografía",
            "ano_publicacion": "Año de publicación",
        }


class NewUsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "cedula",
            "no_carnet",
            "tipo_persona",
            "password",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "Nombre de Usuario"}
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control mb-2",
                    "placeholder": "Correo Electrónico",
                }
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control mb-2", "placeholder": "Contraseña"}
            ),
            "cedula": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "Cédula"}
            ),
            "no_carnet": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "Número de Carnet"}
            ),
            "tipo_persona": forms.Select(attrs={"class": "form-select mb-2"}),
            "estado": forms.CheckboxInput(attrs={"class": "form-check-input mb-2"}),
        }

    def __init__(self, *args, **kwargs):
        super(NewUsuarioForm, self).__init__(*args, **kwargs)
        if not self.fields["tipo_persona"].choices[0][0]:  # Si ya no hay opción vacía
            self.fields["tipo_persona"].choices = [
                ("", "Seleccione el Tipo de Persona")
            ] + list(self.fields["tipo_persona"].choices)[1:]
        for field in self.fields.values():
            field.label = False


class NewEmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ["nombre", "cedula", "no_carnet", "tipo_persona", "estado"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "cedula": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "no_carnet": forms.TextInput(attrs={"class": "form-control mb-2"}),
            "tipo_persona": forms.Select(attrs={"class": "form-select mb-2"}),
            "estado": forms.CheckboxInput(attrs={"class": "form-check-input mb-2"}),
        }


class NewPrestamoDevolucionForm(forms.ModelForm):
    class Meta:
        model = PrestamoDevolucion
        fields = [
            "empleado",
            "libro",
            "usuario",
            "fecha_prestamo",
            "fecha_devolucion",
            "monto_por_dia",
            "cantidad_dias",
            "comentario",
            "estado",
        ]
        widgets = {
            "empleado": forms.Select(attrs={"class": "form-select mb-2"}),
            "libro": forms.Select(attrs={"class": "form-select mb-2"}),
            "usuario": forms.Select(attrs={"class": "form-select mb-2"}),
            "fecha_prestamo": forms.DateInput(
                attrs={"class": "form-control mb-2", "type": "date"}
            ),
            "fecha_devolucion": forms.DateInput(
                attrs={"class": "form-control mb-2", "type": "date"}
            ),
            "monto_por_dia": forms.NumberInput(attrs={"class": "form-control mb-2"}),
            "cantidad_dias": forms.NumberInput(attrs={"class": "form-control mb-2"}),
            "comentario": forms.Textarea(attrs={"class": "form-control mb-2"}),
            "estado": forms.CheckboxInput(attrs={"class": "form-check-input mb-2"}),
        }


class BusquedaLibroForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Usuario",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Fecha de Inicio",
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Fecha Fin",
    )
    ciencia = forms.CharField(
        required=False,
        label="Ciencia",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class ReporteRentasForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    tipo_bibliografia = forms.ModelChoiceField(
        queryset=TipoBibliografia.objects.all(),
        required=False,
        empty_label="Todos los tipos",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    idioma = forms.ModelChoiceField(
        queryset=Idioma.objects.all(),
        required=False,
        empty_label="Todos los idiomas",
        widget=forms.Select(attrs={"class": "form-select"}),
    )


# Create your views here.
def index(request):
    return render(request, "biblioteca/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "biblioteca/login.html",
                {"message": "Nombre de usuario o contraseña inválidos."},
            )
    else:
        return render(request, "biblioteca/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request,
                "biblioteca/register.html",
                {"message": "Las contraseñas deben ser iguales."},
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "biblioteca/register.html",
                {"message": "Este nombre de usuario ya está siendo utilizado."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        form = NewUsuarioForm()
        return render(request, "biblioteca/register.html", {"form": form})


# Tipo Bibliografias
@login_required
def tipo_bibliografia_list(request):
    bibliografias = TipoBibliografia.objects.all()
    return render(
        request,
        "biblioteca/bibliografias/tipo_bibliografia_list.html",
        {"bibliografias": bibliografias},
    )


@login_required
def tipo_bibliografia_create(request):
    if request.method == "POST":
        form = NewTipoBibliografiaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("tipo_bibliografia_list"))
    else:
        form = NewTipoBibliografiaForm()
    return render(
        request, "biblioteca/bibliografias/tipo_bibliografia_form.html", {"form": form}
    )


@login_required
def tipo_bibliografia_update(request, pk):
    bibliografia = get_object_or_404(TipoBibliografia, pk=pk)
    if request.method == "POST":
        form = NewTipoBibliografiaForm(request.POST, instance=bibliografia)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("tipo_bibliografia_list"))
    else:
        form = NewTipoBibliografiaForm(instance=bibliografia)
    return render(
        request, "biblioteca/bibliografias/tipo_bibliografia_form.html", {"form": form}
    )


@login_required
def tipo_bibliografia_delete(request, pk):
    bibliografia = get_object_or_404(TipoBibliografia, pk=pk)
    if request.method == "POST":
        bibliografia.delete()
        return HttpResponseRedirect(reverse("tipo_bibliografia_list"))
    return render(
        request,
        "biblioteca/bibliografias/tipo_bibliografia_confirm_delete.html",
        {"object": bibliografia},
    )


@login_required
def editora_list(request):
    editoras = Editora.objects.all()
    return render(
        request, "biblioteca/editoras/editora_list.html", {"editoras": editoras}
    )


@login_required
def editora_create(request):
    if request.method == "POST":
        form = NewEditoraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("editora_list")
    else:
        form = NewEditoraForm()
    return render(request, "biblioteca/editoras/editora_form.html", {"form": form})


@login_required
def editora_update(request, pk):
    editora = get_object_or_404(Editora, pk=pk)
    if request.method == "POST":
        form = NewEditoraForm(request.POST, instance=editora)
        if form.is_valid():
            form.save()
            return redirect("editora_list")
    else:
        form = NewEditoraForm(instance=editora)
    return render(request, "biblioteca/editoras/editora_form.html", {"form": form})


@login_required
def editora_delete(request, pk):
    editora = get_object_or_404(Editora, pk=pk)
    if request.method == "POST":
        editora.delete()
        return redirect("editora_list")
    return render(
        request, "biblioteca/editoras/editora_confirm_delete.html", {"object": editora}
    )


# Idioma
@login_required
def idioma_list(request):
    idiomas = Idioma.objects.all()
    return render(request, "biblioteca/idiomas/idioma_list.html", {"idiomas": idiomas})


@login_required
def idioma_create(request):
    if request.method == "POST":
        form = NewIdiomaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("idioma_list")
    else:
        form = NewIdiomaForm()
    return render(request, "biblioteca/idiomas/idioma_form.html", {"form": form})


@login_required
def idioma_update(request, pk):
    idioma = get_object_or_404(Idioma, pk=pk)
    if request.method == "POST":
        form = NewIdiomaForm(request.POST, instance=idioma)
        if form.is_valid():
            form.save()
            return redirect("idioma_list")
    else:
        form = NewIdiomaForm(instance=idioma)
    return render(request, "biblioteca/idiomas/idioma_form.html", {"form": form})


@login_required
def idioma_delete(request, pk):
    idioma = get_object_or_404(Idioma, pk=pk)
    if request.method == "POST":
        idioma.delete()
        return redirect("idioma_list")
    return render(
        request, "biblioteca/idiomas/idioma_confirm_delete.html", {"idioma": idioma}
    )


# Autores
@login_required
def autor_list(request):
    autores = Autor.objects.all()
    return render(request, "biblioteca/autores/autor_list.html", {"autores": autores})


@login_required
def autor_create(request):
    if request.method == "POST":
        form = NewAutorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("autor_list")
    else:
        form = NewAutorForm()
    return render(request, "biblioteca/autores/autor_form.html", {"form": form})


@login_required
def autor_update(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == "POST":
        form = NewAutorForm(request.POST, instance=autor)
        if form.is_valid():
            form.save()
            return redirect("autor_list")
    else:
        form = NewAutorForm(instance=autor)
    return render(request, "biblioteca/autores/autor_form.html", {"form": form})


@login_required
def autor_delete(request, pk):
    autor = get_object_or_404(Autor, pk=pk)
    if request.method == "POST":
        autor.delete()
        return redirect("autor_list")
    return render(
        request, "biblioteca/autores/autor_confirm_delete.html", {"autor": autor}
    )


# Libros
@login_required
def libro_list(request):
    libros = Libro.objects.all()
    return render(request, "biblioteca/libros/libro_list.html", {"libros": libros})


@login_required
def libro_create(request):
    if request.method == "POST":
        form = NewLibroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("libro_list")
    else:
        form = NewLibroForm()
    return render(request, "biblioteca/libros/libro_form.html", {"form": form})


@login_required
def libro_update(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        form = NewLibroForm(request.POST, instance=libro)
        if form.is_valid():
            form.save()
            return redirect("libro_list")
    else:
        form = NewLibroForm(instance=libro)
    return render(request, "biblioteca/libros/libro_form.html", {"form": form})


@login_required
def libro_delete(request, pk):
    libro = get_object_or_404(Libro, pk=pk)
    if request.method == "POST":
        libro.delete()
        return redirect("libro_list")
    return render(
        request, "biblioteca/libros/libro_confirm_delete.html", {"libro": libro}
    )


# Empleados
@login_required
def empleado_list(request):
    empleados = Empleado.objects.all()
    return render(
        request, "biblioteca/empleados/empleado_list.html", {"empleados": empleados}
    )


@login_required
def empleado_create(request):
    if request.method == "POST":
        form = NewEmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("empleado_list")
    else:
        form = NewEmpleadoForm()
    return render(request, "biblioteca/empleados/empleado_form.html", {"form": form})


@login_required
def empleado_update(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        form = NewEmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect("empleado_list")
    else:
        form = NewEmpleadoForm(instance=empleado)
    return render(request, "biblioteca/empleados/empleado_form.html", {"form": form})


@login_required
def empleado_delete(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        empleado.delete()
        return redirect("empleado_list")
    return render(
        request,
        "biblioteca/empleados/empleado_confirm_delete.html",
        {"empleado": empleado},
    )


# Préstamos y Devoluciones


@login_required
def prestamo_list(request):
    prestamos = PrestamoDevolucion.objects.all()
    return render(
        request, "biblioteca/prestamos/prestamo_list.html", {"prestamos": prestamos}
    )


@login_required
def prestamo_create(request):
    if request.method == "POST":
        print("Correcto")
        form = NewPrestamoDevolucionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("prestamo_list")
    else:
        form = NewPrestamoDevolucionForm()
    return render(request, "biblioteca/prestamos/prestamo_form.html", {"form": form})


@login_required
def prestamo_update(request, pk):
    prestamo = get_object_or_404(PrestamoDevolucion, pk=pk)
    if request.method == "POST":
        form = NewPrestamoDevolucionForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect("prestamo_list")
    else:
        form = NewPrestamoDevolucionForm(instance=prestamo)
    return render(request, "biblioteca/prestamos/prestamo_form.html", {"form": form})


@login_required
def prestamo_delete(request, pk):
    prestamo = get_object_or_404(PrestamoDevolucion, pk=pk)
    if request.method == "POST":
        prestamo.delete()
        return redirect("prestamo_list")
    return render(
        request,
        "biblioteca/prestamos/prestamo_confirm_delete.html",
        {"prestamo": prestamo},
    )


@login_required
def buscar_libros(request):
    prestamos = (
        PrestamoDevolucion.objects.all()
    )  # Consulta inicial de todos los préstamos
    form = BusquedaLibroForm(request.GET or None)  # Maneja el formulario

    if form.is_valid():
        # Filtros
        usuario = form.cleaned_data.get("usuario")
        fecha_inicio = form.cleaned_data.get("fecha_inicio")
        fecha_fin = form.cleaned_data.get("fecha_fin")
        ciencia = form.cleaned_data.get("ciencia")

        if usuario:
            prestamos = prestamos.filter(usuario=usuario)

        if fecha_inicio:
            prestamos = prestamos.filter(fecha_prestamo=fecha_inicio)

        if fecha_fin:
            prestamos = prestamos.filter(fecha_devolucion=fecha_fin)

        if ciencia:
            prestamos = prestamos.filter(libro__ciencia__icontains=ciencia)

    context = {"form": form, "prestamos": prestamos}

    return render(request, "biblioteca/buscar_libros.html", context)


@login_required
def reporte_rentas(request):
    form = ReporteRentasForm(request.GET or None)
    prestamos = PrestamoDevolucion.objects.all()

    if form.is_valid():
        fecha_inicio = form.cleaned_data.get("fecha_inicio")
        fecha_fin = form.cleaned_data.get("fecha_fin")
        tipo_bibliografia = form.cleaned_data.get("tipo_bibliografia")
        idioma = form.cleaned_data.get("idioma")

        if fecha_inicio:
            prestamos = prestamos.filter(fecha_prestamo=fecha_inicio)
        if fecha_fin:
            prestamos = prestamos.filter(fecha_devolucion=fecha_fin)
        if tipo_bibliografia:
            prestamos = prestamos.filter(libro__tipo_bibliografia=tipo_bibliografia)
        if idioma:
            prestamos = prestamos.filter(libro__idioma=idioma)

    return render(
        request,
        "biblioteca/reporte_rentas.html",
        {"form": form, "prestamos": prestamos},
    )
