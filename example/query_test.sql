SELECT f_matchid
FROM t_gold_order
WHERE f_uid=1002922
GROUP BY f_matchid

SELECT f_uid
FROM t_gold_order
WHERE f_matchid=1179663
GROUP BY f_uid