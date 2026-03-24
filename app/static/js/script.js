async function carregarDados() {
    try {
        const resposta = await fetch("http://localhost:5000/"); 
        const json = await resposta.json();
        const listaRegistros = json.dados; 
        const ultimoRegistro = listaRegistros.at(-1);

        if (listaRegistros.length > 0) {
         
            document.getElementById("temp").innerText = ultimoRegistro.temperatura + " °C";
            document.getElementById("umid").innerText = ultimoRegistro.umidade + " %";
            document.getElementById("qtd").innerText = listaRegistros.length;

            const tabelaBd = document.getElementById("tabela-bd");
            tabelaBd.innerHTML = "";

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

        const respostaTS = await fetch("http://localhost:5000/dados");
        const jsonTS = await respostaTS.json();
        
        if (jsonTS.status === "sucesso") {
            const tabelaApi = document.getElementById("tabela-api");
            tabelaApi.innerHTML = "";
            
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
        console.error("Erro ao carregar dados:", erro);
    }
}

carregarDados();