from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib import messages
from user.forms import CustomUserCreationForm
from categories.models import  Category
from products.models import Product
from django.contrib.auth.decorators import login_required



def inicio(request):
    return render(request, 'inicio.html', {
        # context
    })


def contacto(request):
    return render(request, 'contacto.html', {
        # context
    })


def nosotros(request):
    return render(request, 'nosotros.html', {
        # context
    })


def Catalogo(request):

    products = Product.objects.all().order_by('-id')

    return render(request, 'catalogo.html', {
        'message': 'Listado de productos',
        'title': 'Productos',
        'products': products,
    })


def dashboard_administrador(request):
    # Verificar si el usuario pertenece al grupo correcto
    if not request.user.groups.filter(name='Empleados').exists():
        # Si no pertenece al grupo adecuado, redirigir a la página de inicio o mostrar un error
        # Puedes cambiar 'inicio' con la URL que desees
        return redirect('inicio')

    # El usuario pertenece al grupo correcto, continuar con el procesamiento normal
    return render(request, 'DashboardAdmin.html', {
        # context
    })


def dashboard_cliente(request):
    # Verificar si el usuario pertenece al grupo correcto
    if not request.user.groups.filter(name='Clientes').exists():
        # Si no pertenece al grupo adecuado, redirigir a la página de inicio o mostrar un error
        # Puedes cambiar 'inicio' con la URL que desees
        return redirect('inicio')

    # El usuario pertenece al grupo correcto, continuar con el procesamiento normal
    return render(request, 'DashboardClient.html', {
        # context
    })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])

            # Verificar el grupo y redirigir según el grupo
            if user.groups.filter(name='Administradores').exists():
                # Redirección para administradores
                return redirect('admin:index')
            elif user.groups.filter(name='Empleados').exists():
                # Redirección para empleados
                return redirect('admin:index')
            elif user.groups.filter(name='Clientes').exists():
                # Redirección para clientes
                return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html', {})


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('inicio')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Registro.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión finalizada')
    return redirect('login')

def rContraseña(request):
    return render(request, 'plantillalogin.html', {
        # context
    })


def AnuncioR(request):
    return render(request, 'anuncioR.html', {
        # context
    })

def nuevaC(request):
    return render(request, 'nuevaC.html', {
        # context
    })

def contraseñaC(request):
    return render(request, 'contraseñaC.html', {
        # context
    })



@login_required
def perfil_usuario(request):
    
    user = request.user
    
    return render(request, 'perfil.html', {'user': user})


@login_required
def editar_informacion(request):
    usuario = request.user  
    return render(request, 'EditarPerfil.html', {'user': usuario})
@login_required
def guardar_informacion(request):
    if request.method == 'POST':
        usuario = request.user
        usuario.username = request.POST.get('username')
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.email = request.POST.get('email')
        usuario.address = request.POST.get('address')
        usuario.cell_phone = request.POST.get('cell_phone')
        usuario.save()
        return redirect('perfil_usuario')  # Redirige al perfil del usuario después de guardar los cambios
    else:
        # Manejar caso si el método no es POST
        # Puedes redirigir a algún lugar o mostrar un mensaje de error
        return redirect('editar_informacion')  # Redirigir de nuevo a la página de edición
    
