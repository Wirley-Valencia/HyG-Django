from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.contrib import messages
from user.forms import CustomUserCreationForm


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
                return redirect('dashboard_administrador')
            elif user.groups.filter(name='Clientes').exists():
                # Redirección para clientes
                return redirect('dashboard_cliente')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html', {})


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Cambia 'home' con la URL a la que quieras redirigir después del registro
            return redirect('inicio')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Registro.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión finalizada')
    return redirect('login')
