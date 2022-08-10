SELECT id, name, created FROM albums
WHERE EXTRACT (YEAR FROM created) = 2018;

SELECT name, duration FROM traks
ORDER BY duration DESC LIMIT 1;

SELECT name, duration FROM traks
WHERE duration > 210
ORDER BY duration;

SELECT name, created FROM albums
WHERE EXTRACT (YEAR FROM created) BETWEEN 2018 AND 2020;

SELECT * FROM artists
WHERE name NOT LIKE '% %';

SELECT * FROM traks
WHERE name ~* '(my|мой)';
