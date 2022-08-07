CREATE TABLE IF NOT EXISTS Artists (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genres (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS ArtistsGenres (
	artist_id INTEGER NOT NULL REFERENCES Artists(id),
	genre_id INTEGER NOT NULL REFERENCES Genres(id),
	CONSTRAINT artist_genre_pk PRIMARY KEY (artist_id, genre_id)
);

CREATE TABLE IF NOT EXISTS Albums (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	created DATE
);

CREATE TABLE IF NOT EXISTS ArtistsAlbums (
	artist_id INTEGER NOT NULL REFERENCES Artists(id),
	album_id INTEGER NOT NULL REFERENCES Albums(id),
	CONSTRAINT artist_album_pk PRIMARY KEY (artist_id, album_id)
);

CREATE TABLE IF NOT EXISTS Collections (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	created DATE
);

CREATE TABLE IF NOT EXISTS Traks (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	album_id INTEGER REFERENCES Albums(id),
	duration SMALLINT NOT NULL 
);

CREATE TABLE IF NOT EXISTS CollectionsTraks (
	collection_id INTEGER NOT NULL REFERENCES Collections(id),
	trak_id INTEGER NOT NULL REFERENCES Traks(id),
	CONSTRAINT collection_trak_pk PRIMARY KEY (collection_id, trak_id)
);
