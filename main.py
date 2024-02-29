import sqlalchemy as db

engine = db.create_engine("sqlite+pysqlite:///albums.sqlite", echo=True)

metadata_obj = db.MetaData()

album = db.Table(
    "album",
    metadata_obj,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.String),
    db.Column("artist", db.String)
)

metadata_obj.create_all(engine)

with engine.connect() as conn:
    # insert_cmd = sa.insert(album).values(
    #         name="Violator",
    #         artist="Depeche Mode"
    #     )

    insert_result = conn.execute(
        db.insert(album),
        [
            {
                "name": "Violator",
                "artist": "Depeche Mode"
            }
        ]
    )

    # print(insert_result.inserted_primary_key)

    insert_more = conn.execute(
        db.insert(album),
        [
            {"name": "Orbital", "artist": "Orbital"},
            {"name": "Technique", "artist": "New Order"}
        ]
    )

    query_result = conn.execute(
        db.select(album)
    )

    for row in query_result:
        print(row)

    conn.commit()

