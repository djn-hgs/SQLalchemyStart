import sqlalchemy as db
import sqlalchemy.orm as orm
import model

engine = db.create_engine("sqlite+pysqlite:///albums.sqlite", echo=False)

# The model now provides the Base class and all of our table classes

# Now the metadata is created for our Base class

model.Base.metadata.create_all(engine)


# We now use a Session rather than a connection

with (orm.Session(engine) as session):
    # Now the magic happens
    # https://stackoverflow.com/questions/17325006/how-to-create-a-foreignkey-reference-with-sqlalchemy

    # Let's have some genres

    genre1 = model.Genre(label="Pop")

    session.add(genre1)

    genre2 = model.Genre(label="Electronic")

    session.add(genre2)

    # And some artists

    artist1 = model.Artist(name="Depeche Mode")
    artist2 = model.Artist(name="Orbital")
    artist3 = model.Artist(name="New Order")

    session.add_all([artist1, artist2, artist3])

    # And an album with artist and genre

    album1 = model.Album(title="A Broken Frame", artist=artist1)
    album1.genres.append(genre1)
    album1.genres.append(genre2)

    session.add(album1)

    # Or as a batch

    session.add_all(
        [
            model.Album(title="Violator", artist=artist1),
            model.Album(title="Orbital", artist=artist2, genres=[genre2]),
            model.Album(title="Technique", artist=artist3)
        ]
    )

    # Don't forget to commit

    session.commit()
