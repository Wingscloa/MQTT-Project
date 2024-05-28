CREATE DATABASE DCUK_MQTT;

USE DCUK_MQTT;


CREATE TABLE senzory
(
  id_sen    BIGINT         NOT NULL AUTO_INCREMENT UNIQUE COMMENT 'ano',
  nazev     VARCHAR(20)    NOT NULL COMMENT 'ano',
  typ       TEXT           NOT NULL COMMENT 'ano',
  frekvence DECIMAL(10, 2) NULL     COMMENT 'ano',
  misto     VARCHAR(60)    NULL     COMMENT 'ano',
  id_stav   BIGINT         NOT NULL DEFAULT 1,
  PRIMARY KEY (id_sen)
);

CREATE TABLE stav
(
  id_stav BIGINT      NOT NULL AUTO_INCREMENT UNIQUE,
  nazev   VARCHAR(20) NULL    ,
  popis   TEXT        NULL     COMMENT 'pricina',
  barva   VARCHAR(20) NULL     COMMENT 'color v hex',
  PRIMARY KEY (id_stav)
);

CREATE TABLE zaznamy
(
  id_zaz BIGINT      NOT NULL AUTO_INCREMENT UNIQUE COMMENT 'NE',
  id_sen BIGINT      NOT NULL COMMENT 'ano',
  cas    TIMESTAMP   NOT NULL DEFAULT now() COMMENT 'NE',
  počasí VARCHAR(20) NULL     COMMENT 'NE',
  PRIMARY KEY (id_zaz)
);

ALTER TABLE zaznamy
  ADD CONSTRAINT FK_senzory_TO_zaznamy
    FOREIGN KEY (id_sen)
    REFERENCES senzory (id_sen);

ALTER TABLE senzory
  ADD CONSTRAINT FK_stav_TO_senzory
    FOREIGN KEY (id_stav)
    REFERENCES stav (id_stav);