from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Carro
import re
from django.core import serializers
import json

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
    if request.method == "GET":
        clientes_list = Cliente.objects.all()
        return render(request, 'clientes.html', {'clientes': clientes_list})
    
    elif request.method == "POST":
        # Metodo POST, pega(.get) e get('Valor do atributo "name" html')
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        carros = request.POST.getlist('carro')
        placas = request.POST.getlist('placa')
        anos = request.POST.getlist('ano')

        cliente = Cliente.objects.filter(cpf=cpf)

        if cliente.exists():
            return render(request, 'clientes.html', {'nome': nome, 'sobrenome': sobrenome, 'email': email, 'carros': zip(carros, placas, anos) })

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

    

def att_cliente(request):
    '''
    - id_cliente: Recebe um metodo post.

    - cliente: Pega todos os objetos do model de "Cliente", e filtra os clientes com base no id do cliente.

    - clientes_json: Recebe os dados de um objeto Django e converte para dicionario em python.

    - carros: Pega e filtra os carros onde o atributo "cliente" em models é igual ao filter (id do cliente). 
        Retorna uma QuerySet, por isso é usado "[0]" para acessar o objeto contendo os carros.

    - carros_json_iter: List Comprehesion.
        - Pecorre a lista contendo os carros do cliente.
        - Cria um dicionario com as chaves:
            - "fields" : Recebe o valor carro['fields'] contendo as informações do carro.
            - "id" : Recebe o valor de carro['pk'], id do carro.

    Funções:
        - json.loads: 
            - Converte a string Json gerada pela serialização em objeto Python.

        - serializers.serialize:
            - Parametros: 
            1º: formatado da saída como Json.
            2º: Queryset contendo um objeto do modelo Cliente.

        
    - [0] - Acessa o primeiro elemento da lista.
    - ['fields'] - Acessa a chave fields do dicionario que contém os dados do objeto do modelo.
    '''

    # print('teste')
    id_cliente = request.POST.get('id_cliente')
    cliente = Cliente.objects.filter(id=id_cliente)
    carros = Carro.objects.filter(cliente=cliente[0]) 

    clientes_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    carros_json = json.loads(serializers.serialize('json', carros))

    carros_json_iter = [ {'fields': carro['fields'], 'id':carro['pk']} for carro in carros_json]

    data = {'cliente': clientes_json, 'carros': carros_json}

    print(clientes_json)
    print(carros_json)
    print(carros_json_iter)

    return JsonResponse(data)