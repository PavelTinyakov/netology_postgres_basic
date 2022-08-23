--1
SELECT g.name genre, COUNT(artist_id) count_artists FROM artistsgenres ag 
JOIN genres g ON a.genre_id = g.id
GROUP BY genre
ORDER BY count_artists DESC;

--2
SELECT a.name album_name, COUNT (t.name) count_trak FROM traks t 
JOIN albums a ON t.album_id = a.id
WHERE EXTRACT (YEAR FROM a.created) BETWEEN 2019 AND 2020
GROUP BY album_name
ORDER BY count_trak DESC;

--3
SELECT a.name album_name, ROUND(AVG(t.duration), 2) avg_duration FROM traks t 
JOIN albums a ON t.album_id = a.id
GROUP BY album_name
ORDER BY avg_duration DESC;

--4
SELECT DISTINCT ar.name FROM artistsalbums ab
JOIN albums al ON ab.album_id = al.id 
JOIN artists ar ON ab.artist_id = ar.id
WHERE EXTRACT (YEAR FROM al.created) NOT IN (2020);

--5
SELECT DISTINCT c.name collection_name FROM collectionstraks ct
JOIN traks t ON ct.trak_id = t.id 
JOIN albums al ON t.album_id = al.id
JOIN artistsalbums ar_al ON al.id = ar_al.album_id
JOIN artists ar ON ar_al.artist_id = ar.id
JOIN collections c ON ct.collection_id = c.id
WHERE ar.name = 'Kiss';

--6
SELECT al.name al_name, ar.name ar_name, COUNT(g.name) count_gener FROM artistsgenres ar_g
JOIN artists ar ON ar_g.artist_id = ar.id
JOIN artistsalbums ar_al ON ar.id = ar_al.artist_id
JOIN albums al ON ar_al.album_id = al.id
JOIN genres g ON ar_g.genre_id = g.id
GROUP BY al.name, ar.name
HAVING COUNT(g.name) > 1;

--7
SELECT name FROM traks t
LEFT JOIN collectionstraks ct ON ct.trak_id = t.id
WHERE ct.collection_id IS NULL; 

--8
SELECT ar.name, t.duration FROM traks t 
JOIN artistsalbums al_id ON al_id.album_id = t.album_id
JOIN artists ar ON al_id.artist_id = ar.id
WHERE t.duration = (SELECT min(duration) FROM traks);

--9
SELECT a.name, COUNT(album_id) FROM traks t 
JOIN albums a ON a.id = t.album_id
GROUP BY a.name
HAVING COUNT(album_id) = 
	(SELECT count(album_id) count_album FROM traks
	GROUP BY album_id
	ORDER BY count_album LIMIT 1);










