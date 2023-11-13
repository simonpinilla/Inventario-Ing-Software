from django.shortcuts import render


def login(request):
    return render(request, 'login.html')
def inventario(request):
    return render(request, 'inventario.html')

# Create your views here.
