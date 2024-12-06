function add_carro(){

    container = document.getElementById("form-carro")

    html = "<br> <div class='row'> <div class='col-md'> <input type='text' placeholder='carro' class='form-control' name='carro'></div> <div class='col-md'><input type='text' placeholder='Placa' class='form-control' name='placa'></div> <div class='col-md'> <input type='number' placeholder='ano' class='form-control' name='ano'></div> </div>";

    // Inserir o conteudo html (os inputs para adicionar as info. do carro) dentro do conteudo do container.
    container.innerHTML += html


}