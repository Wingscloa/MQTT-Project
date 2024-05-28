INSERT INTO stav (nazev, popis,barva) VALUES 
('vypocet_zac', 'Tento stav indikuje, že výpočet právě začal. Všechny systémy by měly být připravené na spuštění úloh.',"#DE9A26"), 
('vypocet_pru', 'Tento stav znamená, že výpočet právě probíhá. Systémy aktivně zpracovávají data a vykonávají úlohy.','#DEB126'),
('vypocet_skoro', 'Tento stav naznačuje, že výpočet je téměř dokončen. Systémy by měly připravovat finální kroky a závěrečné operace.',"#DEC726"),
('funguje', 'Tento stav signalizuje, že vše funguje bez problémů. Systémy jsou v normálním provozu a nejsou detekovány žádné chyby.',"#5FDE26"),
('bacha', 'Tento stav upozorňuje na potenciální problém nebo varování. Systémy by měly být monitorovány, ale zatím není nutný zásah.','##7B8945'),
('neco se deje', 'Tento stav indikuje, že se v systému děje něco neočekávaného. Může být potřeba bližší analýza nebo zásah.',"#DE266C"),
('pohni', 'Tento stav znamená, že je potřeba rychlý zásah. Systémy mohou být v kritickém stavu a vyžadují okamžitou pozornost.','#FF0E00');