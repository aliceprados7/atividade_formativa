const botaoConexao = document.getElementById("conexao")
let input = document.getElementById("ip");
// funcão responsável port buscar os dados
async function carregarDados() {
    let ipServidor = input.value;

    if(ipServidor){
        try {
        // acessa a url rodando localmente para puxar os dados do banco de dados
        const resposta = await fetch(`http://${ipServidor}:5000/`); 
        const json = await resposta.json();
        // variavel que recebe os dados
        const listaRegistros = json.dados;
        // variavel que recebe os ultimos dados enviados 
        const ultimoRegistro = listaRegistros.at(-1);

        // caso exista dados
        if (listaRegistros.length > 0) {
            // altera os valores do front-end
            document.getElementById("temp").innerText = ultimoRegistro.temperatura + " °C";
            document.getElementById("umid").innerText = ultimoRegistro.umidade + " %";
            document.getElementById("qtd").innerText = listaRegistros.length; // recebe o tamanho do json, ou seja, a quantidade de dados enviados

            const tabelaBd = document.getElementById("tabela-bd");
            tabelaBd.innerHTML = "";
            // cria novos elementos dentro da tabela
            listaRegistros.forEach(item => {
                tabelaBd.innerHTML += `
                    <tr>
                        <td>${item.id}</td>
                        <td>${item.data_hora}</td>
                        <td>${item.temperatura} °C</td>
                        <td>${item.umidade} %</td>
                    </tr>
                `;
            });
        }
        // recebe os dados recebidos pela função readThingSpeak, cujo lê os dados da nuvem
        const respostaTS = await fetch(`http://${ipServidor}:5000/dados`);
        const jsonTS = await respostaTS.json();
        // controle para escrita na tabea
        if (jsonTS.status === "sucesso") {
            const tabelaApi = document.getElementById("tabela-api");
            tabelaApi.innerHTML = "";
            // atualiza a respectiva tabela
            jsonTS.dados.forEach((item, index) => {
                tabelaApi.innerHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${item.data_hora}</td>
                        <td>${item.temperatura} °C</td>
                        <td>${item.umidade} %</td>
                    </tr>
                `;
            });
        }

    } catch (erro) {
        alert("Erro ao carregar dados. Verifique a conexão e a porta conectada", erro);
    }
    }


    
}

carregarDados();