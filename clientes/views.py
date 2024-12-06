from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Carro

def clientes(request):
    if request.method == 'GET':
        return render(request, 'clientes.html')
    elif request.method == 'POST':
        # Metodo POST, pega(.get) e get('Valor do atributo "name" html')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')

        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )

        cliente.save()
        # Converte as tuplas geradas pela função zip em uma lista.
        # zip -> Combina elementos de múltiplas listas em tuplas, onde cada tupla contém elementos correspondentes
        # das listas fornecidas.
        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()
            
        return HttpResponse('Teste')