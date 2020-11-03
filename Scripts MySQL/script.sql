CREATE DATABASE `db_desafio`;
USE `db_desafio`;

CREATE TABLE `tb_clientes`
(
  `cliente_id` int NOT NULL AUTO_INCREMENT,
  `cliente_nome` varchar(35) NOT NULL,
  `cliente_sobrenome` varchar(35) NOT NULL,
  `cliente_email` varchar(64) NOT NULL,
  `cliente_end_com` varchar(45) NOT NULL,
  `cliente_end_res` varchar(45) DEFAULT NULL,
  `cliente_pais` varchar(20) NOT NULL,
  `cliente_estado` varchar(20) NOT NULL,
  `cliente_cidade` varchar(20) NOT NULL,
  PRIMARY KEY (`cliente_id`)
)

CREATE TABLE `tb_pedidos`
(
  `pedido_id` int NOT NULL AUTO_INCREMENT,
  `cliente_id` int NOT NULL,
  `pedido_data` date NOT NULL,
  `pedido_status` int NOT NULL,
  `pedido_valor` decimal(10,2) NOT NULL,
  PRIMARY KEY (`pedido_id`)
)
