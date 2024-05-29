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
