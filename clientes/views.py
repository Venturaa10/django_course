from django.shortcuts import render
from django.http import HttpResponse
from .models import Cliente, Carro
import re

def clientes(request):
    ''' 
    Condições: 
    - Verifica se cliente já existe de acordo com o cpf.
    - Verifica se email está de acordo com o padrão fornecido pelo regex.

    Funções:
    - zip: Combina elementos de múltiplas listas em tuplas, onde cada tupla contém elementos correspondentes das listas fornecidas.

    Retornos:
    - Se algum campo estiver invalido, renderiza o template novamente e todos os campos já preenchidos pelo usuario, exceto a campo invalido.
    - Retorna HttpResponse quando todos os campos validos.
    '''
    if request.method == 'GET':
        return render(request, 'clientes.html')
    
    elif request.method == 'POST':
        # Metodo POST, pega(.get) e get('Valor do atributo "name" html')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')

        cliente = Cliente.objects.filter(cpf=cpf) 

        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        if cliente.exists():
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas, anos)}) 

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'cpf': cpf, 'carros': zip(carros, placas, anos)}) 

        cliente = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            email = email,
            cpf = cpf
        )

        cliente.save()

        # Converte as tuplas geradas pela função zip em uma lista.
        for carro, placa, ano in zip(carros, placas, anos):
            car = Carro(carro=carro, placa=placa, ano=ano, cliente=cliente)
            car.save()
            
        return HttpResponse('Teste')