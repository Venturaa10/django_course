function add_carro() {
    /** Adiciona linha para adicionar carro.
     * 
     * Variaveis:
        * Container: Pega o "id" onde a coluna será adicionada.  
        * html: Código HTML contendo a "div" na qual será inserida.
        * 
     * Saídas:
        * Adiciona o código da variavel "html" quando a função é chamada. 
     * 
    */
      
    container = document.getElementById('form-carro')

    html = `<br>  
    <div class='row'> 
        <div class='col-md'> 
            <input type='text' placeholder='carro' class='form-control' name='carro' > 
        </div>
            <div class='col-md'><input type='text' placeholder='Placa' class='form-control' name='placa' >
        </div> 
            <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='ano'>
        </div> 
    </div>`

    container.innerHTML += html
}


function exibir_form(tipo) {
    /** Exibir e ocultar quando houver alguma interação com as opções para adicionar ou atualizar clientes.  
     * 
     * Variaveis:
        * add_cliente: Pega id da "div" para adicionar clientes.
        * att_cliente: Pega id da "div" para atualizar clientes.
     * 
     * Condições:
        * Se o valor do tipo igual 1, oculta a div de atualizar e exibe para adicionar cliente.
        * Se valor do tipo igual 2, oculta a div de adicionar e exibe para atualizar cliente.
        *   
     * Parametros:
        *  tipo: Representa qual opção foi selecionada pelo usuario.
    */
    add_cliente = document.getElementById('adicionar-cliente')
    att_cliente = document.getElementById('att_cliente')

    if (tipo == "1") {
        att_cliente.style.display = "none"
        add_cliente.style.display = "block"

    } else if (tipo == "2") {
        add_cliente.style.display = "none";
        att_cliente.style.display = "block"
    }

}


function dados_cliente() {
    cliente = document.getElementById('cliente-select') // Tag "select" no HTML para exibir todos os clientes cadastrados.
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value // Chave de segunrança para a execução do metodo "POST".
    id_cliente = cliente.value // Armazena id do cliente na qual foi selecionado em "select".

    data = new FormData()
    data.append('id_cliente', id_cliente)

    fetch("/clientes/atualiza_cliente/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data

    }).then(function (result) {
        return result.json()

    }).then(function (data) {
        console.log(data) // Objeto contendo as informações do cliente.
        document.getElementById('form-att-cliente').style.display = 'block' // Torna a "div" contendo as informações do cliente visivel.

        nome = document.getElementById('nome')
        nome.value = data['cliente']['nome']

        sobrenome = document.getElementById('sobrenome')
        sobrenome.value = data['cliente']['sobrenome']

        cpf = document.getElementById('cpf')
        cpf.value = data['cliente']['cpf']

        email = document.getElementById('email')
        email.value = data['cliente']['email']

        div_carros = document.getElementById('carros')
        div_carros.innerHTML = ""


        for (i = 0; i < data['carros'].length; i++) {
            console.log(data['carros'][i]['fields']['carro'])

            div_carros.innerHTML += `
            <form action='/clientes/update_carro/"${data['carros'][i]['id']}"' method='POST'>
                <div class='row'>
                    <div class='col-md'>
                        <input class='form-control' type='text' name='carro' value='${data['carros'][i]['fields']['carro']}'>
                    </div>
                    <div class='col-md'>
                        <input class='form-control' type='text' name='carro' value='${data['carros'][i]['fields']['placa']}'>
                    </div>
                    <div class='col-md'>
                        <input class='form-control' type='text' name='carro' value='${data['carros'][i]['fields']['ano']}'>
                    </div>
                    <div class='col-md'>
                        <input class='btn-success' type='submit' value='salvar'>
                    </div>
                </div><br>
            </form>`
        };
    })
}