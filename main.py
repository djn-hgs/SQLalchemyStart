import sqlalchemy as db

engine = db.create_engine("sqlite+pysqlite:///albums.sqlite", echo=True)

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

metadata_obj.create_all(engine)

with engine.connect() as conn:
    # insert_cmd = sa.insert(album).values(
    #         name="Violator",
    #         artist="Depeche Mode"
    #     )

    item1_result = conn.execute(
        db.insert(artist).values(artist_name="Depeche Mode")
    )

    item1_id, = item1_result.inserted_primary_key

    item2_result = conn.execute(
        db.insert(artist).values(artist_name="Orbital")
    )

    item2_id, = item2_result.inserted_primary_key

    item3_result = conn.execute(
        db.insert(artist).values(artist_name="New Order")
    )

    item3_id, = item3_result.inserted_primary_key

    first_album = conn.execute(
        album.insert().values(
            album_name="Speak and Spell",
            artist_id=item1_id
        )
    )

    insert_albums = conn.execute(
        db.insert(album),
        [
            {"album_name": "Violator", "artist_id": item1_id},
            {"album_name": "Orbital", "artist_id": item2_id},
            {"album_name": "Technique", "artist_id": item3_id}
        ]
    )

    query_result = conn.execute(
        db.select(album.c.album_name, artist.c.artist_name).select_from(db.join(artist, album))
    )

    for row in query_result:
        print(row)

    conn.commit()

