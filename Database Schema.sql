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

CREATE VIEW zaznamy_view AS
WITH cte AS (
    SELECT 
        id_zaz,
        id_sen,
        cas,
        LEAD(cas) OVER (PARTITION BY id_sen ORDER BY cas) AS cas2
    FROM zaznamy
)
SELECT
    id_sen,
    cas AS cas1,
    cas2,
    TIMEDIFF(cas2, cas) AS rozdil
FROM cte
WHERE cas2 IS NOT NULL
ORDER BY id_sen, cas;



ALTER TABLE zaznamy
  ADD CONSTRAINT FK_senzory_TO_zaznamy
    FOREIGN KEY (id_sen)
    REFERENCES senzory (id_sen);

ALTER TABLE senzory
  ADD CONSTRAINT FK_stav_TO_senzory
    FOREIGN KEY (id_stav)
    REFERENCES stav (id_stav);


INSERT INTO stav (nazev, popis,barva) VALUES 
('vypocet_zac', 'Tento stav indikuje, že výpočet právě začal. Všechny systémy by měly být připravené na spuštění úloh.',"#DE9A26"), 
('vypocet_pru', 'Tento stav znamená, že výpočet právě probíhá. Systémy aktivně zpracovávají data a vykonávají úlohy.','#DEB126'),
('vypocet_skoro', 'Tento stav naznačuje, že výpočet je téměř dokončen. Systémy by měly připravovat finální kroky a závěrečné operace.',"#DEC726"),
('funguje', 'Tento stav signalizuje, že vše funguje bez problémů. Systémy jsou v normálním provozu a nejsou detekovány žádné chyby.',"#5FDE26"),
('bacha', 'Tento stav upozorňuje na potenciální problém nebo varování. Systémy by měly být monitorovány, ale zatím není nutný zásah.','##7B8945'),
('neco se deje', 'Tento stav indikuje, že se v systému děje něco neočekávaného. Může být potřeba bližší analýza nebo zásah.',"#DE266C"),
('pohni', 'Tento stav znamená, že je potřeba rychlý zásah. Systémy mohou být v kritickém stavu a vyžadují okamžitou pozornost.','#FF0E00');