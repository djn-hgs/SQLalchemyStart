import sqlalchemy as sqla

engine = sqla.create_engine("sqlite+pysqlite:///albums.sqlite", echo=True)

metadata_obj = sqla.MetaData()

album = sqla.Table(
    "album",
    metadata_obj,
    sqla.Column("id", sqla.Integer, primary_key=True),
    sqla.Column("name", sqla.String),
    sqla.Column("artist", sqla.String)
)

metadata_obj.create_all(engine)

with engine.connect() as conn:
    # insert_cmd = sa.insert(album).values(
    #         name="Violator",
    #         artist="Depeche Mode"
    #     )

    insert_result = conn.execute(
        sqla.insert(album),
        [
            {
                "name": "Violator",
                "artist": "Depeche Mode"
            }
        ]
    )

    # print(insert_result.inserted_primary_key)

    insert_more = conn.execute(
        sqla.insert(album),
        [
            {"name": "Orbital", "artist": "Orbital"},
            {"name": "Technique", "artist": "New Order"}
        ]
    )

    query_result = conn.execute(
        sqla.select(album)
    )

    for row in query_result:
        print(row)

    conn.commit()

