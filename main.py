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
    # We have to add items individually if we want to know their autoincrement key
    # There is no workaround for this

    item1_result = conn.execute(
        db.insert(artist).values(artist_name="Depeche Mode")
    )

    # Notice that the result inserted_primary_key is a tuple, so the "," is really important

    item1_id, = item1_result.inserted_primary_key

    item2_result = conn.execute(
        db.insert(artist).values(artist_name="Orbital")
    )

    item2_id, = item2_result.inserted_primary_key

    item3_result = conn.execute(
        db.insert(artist).values(artist_name="New Order")
    )

    item3_id, = item3_result.inserted_primary_key

    # Inserting one album, using the artist id received above

    first_album = conn.execute(
        album.insert().values(
            album_name="Speak and Spell",
            artist_id=item1_id
        )
    )

    # Inserting many albums

    insert_albums = conn.execute(
        db.insert(album),
        [
            {"album_name": "Violator", "artist_id": item1_id},
            {"album_name": "Orbital", "artist_id": item2_id},
            {"album_name": "Technique", "artist_id": item3_id}
        ]
    )

    # Now let's get some information using a join

    query_result = conn.execute(
        db.select(db.join(artist, album))
    )

    for row in query_result:
        print(row)

    # Another approach to getting information using a join
    # Note that we already declared the Foreign Keys so this "just works"

    query_result = conn.execute(
        db.select(artist.join(album))
    )

    for row in query_result:
        print(row)

    # Now let's get some information using a join but restricting the columns
    # The ".c" part is selecting columns - I always think it looks like magic

    query_result = conn.execute(
        db.select(album.c.album_name, artist.c.artist_name).select_from(artist.join(album))
    )

    for row in query_result:
        print(row)

    # And now let's restrict the list using a filter - time to move to multiple lines methinks...

    query_result = conn.execute(
        db.select(album.c.album_name)
        .select_from(artist.join(album))
        .filter(artist.c.artist_name == "Depeche Mode")
    )

    for row in query_result:
        print(row)

    conn.commit()

