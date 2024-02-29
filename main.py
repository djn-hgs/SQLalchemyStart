import sqlalchemy as db

engine = db.create_engine("sqlite:///albums.sqlite", echo=True)

metadata_obj = db.MetaData()

artist = db.Table(
    "artist",
    metadata_obj,
    db.Column("artist_id", db.Integer, primary_key=True),
    db.Column("artist_name", db.String),
)

album = db.Table(
    "album",
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("album_name", db.String),
    db.Column("artist_id", db.String, db.ForeignKey("artist.artist_id"))
)

genre = db.Table(
    "genre",
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("genre_name", db.String)
)

album_genre = db.Table(
    "album_genre",
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("album_id", db.ForeignKey("album.id")),
    db.Column("genre_id", db.ForeignKey("genre.id"))
)

metadata_obj.create_all(engine)

with engine.connect() as conn:
    # insert_cmd = sa.insert(album).values(
    #         name="Violator",
    #         artist="Depeche Mode"
    #     )

    # Let's add a few artists

    artist1_result = conn.execute(
        db.insert(artist).values(artist_name="Depeche Mode")
    )

    artist1_id, = artist1_result.inserted_primary_key

    artist2_result = conn.execute(
        db.insert(artist).values(artist_name="Orbital")
    )

    artist2_id, = artist2_result.inserted_primary_key

    artist3_result = conn.execute(
        db.insert(artist).values(artist_name="New Order")
    )

    artist3_id, = artist3_result.inserted_primary_key

    # Now some albums - we need to add individually if we want to associate a genre

    album1_result = conn.execute(
        album.insert().values(
            album_name="Speak and Spell",
            artist_id=artist1_id
        )
    )

    album1_id, = album1_result.inserted_primary_key

    album2_result = conn.execute(
        album.insert().values(
            album_name="Orbital",
            artist_id=artist2_id
        )
    )

    album2_id, = album2_result.inserted_primary_key

    insert_albums = conn.execute(
        db.insert(album),
        [
            {"album_name": "Violator", "artist_id": artist1_id},
            {"album_name": "Orbital 2", "artist_id": artist2_id},
            {"album_name": "Technique", "artist_id": artist3_id}
        ]
    )

    # And some genres

    genre1_result = conn.execute(
        genre.insert().values(
            genre_name="Electronic"
        )
    )

    genre1_id, = genre1_result.inserted_primary_key

    genre2_result = conn.execute(
        genre.insert().values(
            genre_name="Pop"
        )
    )

    genre2_id, = genre2_result.inserted_primary_key

    # Now associate an album with a genre

    album_genre_result = conn.execute(
        album_genre.insert(),
        [
            {"album_id": album1_id, "genre_id": genre1_id},
            {"album_id": album1_id, "genre_id": genre2_id},
            {"album_id": album2_id, "genre_id": genre1_id}
        ]
    )

    # A simple query using a join

    artist_album_result = conn.execute(
        db.select(album.c.album_name, artist.c.artist_name)
        .select_from(
            artist
            .join(album)
        )
    )

    for row in artist_album_result:
        print(row)

    # Now let's use our link table in the join

    artist_album_genre_result = conn.execute(
        db.select(album.c.album_name, artist.c.artist_name, genre.c.genre_name)
        .select_from(
            artist
            .join(album)
            .join(album_genre)
            .join(genre)
        )
    )

    for row in artist_album_genre_result:
        print(row)

    # And now let's throw in a filter as well

    query_result = conn.execute(
        db.select(album.c.album_name, artist.c.artist_name, genre.c.genre_name)
        .select_from(
            artist
            .join(album)
            .join(album_genre)
            .join(genre)
        )
        .filter(artist.c.artist_name == 'Depeche Mode')
    )

    for row in query_result:
        print(row)

    # Or how about this? Filter and where do exactly the same job

    query_result = conn.execute(
        db.select(album.c.album_name, artist.c.artist_name, genre.c.genre_name)
        .select_from(
            artist
            .join(album)
            .join(album_genre)
            .join(genre)
        )
        .where(genre.c.id==genre1_id)
    )

    # There is a Pycharm bug in the .where clause
    # https://github.com/sqlalchemy/sqlalchemy/issues/9337

    for row in query_result:
        print(row)

    conn.commit()
