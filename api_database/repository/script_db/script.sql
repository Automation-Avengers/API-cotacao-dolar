-- Banco de Dados MySQL
-- Apagar o banco de dados
drop database banco;
-- Criar o banco de dados
create database banco;
-- Atribuir os privilégios de acesso aos objetos do banco
-- para o usuário root
GRANT ALL PRIVILEGES ON banco.* TO 'root' @'localhost';
-- Acesar o banco de dados: banco
USE banco;
-- Criar a tabela: usuario

CREATE TABLE produto(
    id int AUTO_INCREMENT,
    descricao varchar(50) NOT NULL,
    unidade varchar(5) NOT NULL,
    quantidade DECIMAL(10,2) NOT NULL,
    preco_real DECIMAL(10,2) NOT NULL,
    preco_dolar DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id)
);

