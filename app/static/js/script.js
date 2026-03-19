async function carregarDados() {
    try {
        const resposta = await fetch("/dados");
        const dados = await resposta.json();

        // Atualizar cards
        document.getElementById("temp").innerText = dados.ultima_temperatura + " °C";
        document.getElementById("umid").innerText = dados.ultima_umidade + " %";
        document.getElementById("qtd").innerText = dados.quantidade;

        // Tabela API
        const tabelaApi = document.getElementById("tabela-api");
        tabelaApi.innerHTML = "";

        dados.api.forEach(item => {
            tabelaApi.innerHTML += `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.data}</td>
                    <td>${item.temp}</td>
                    <td>${item.umid}</td>
                </tr>
            `;
        });

        // Tabela BD
        const tabelaBd = document.getElementById("tabela-bd");
        tabelaBd.innerHTML = "";

        dados.bd.forEach(item => {
            tabelaBd.innerHTML += `
                <tr>
                    <td>${item.id}</td>
                    <td>${item.data}</td>
                    <td>${item.temp}</td>
                    <td>${item.umid}</td>
                </tr>
            `;
        });

    } catch (erro) {
        console.error("Erro ao carregar dados:", erro);
    }
}

// carregar ao abrir a página
carregarDados();