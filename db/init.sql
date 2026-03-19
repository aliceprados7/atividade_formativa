
use monitoramento;

create table registros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_hora DATETIME 
    temperatura DECIMAL (5, 2) NOT NULL,
    umidade DECIMAL (5, 2) NOT NULL,
    origem_dado VARCHAR (50) NOT NULL,
    data_insercao DATETIME DEFAULT CURRENT_TIMESTAMP
);
