import sqlalchemy as db
import sqlalchemy.orm as orm

engine = db.create_engine("sqlite+pysqlite:///albums.sqlite", echo=False)


# We no longer need a metadata object
# Now we just create an abstract Base class which has its own metadata

class Base(orm.DeclarativeBase):
    pass


# A slight tweak here - we declare column names and used mapped columns
# There is more to come here

class Artist(Base):
    __tablename__ = "artist"

    id = orm.mapped_column(db.Integer, primary_key=True)
    name = orm.mapped_column(db.String)

    # Now we have a foreign key we can do something seriously clever
    # This means that artists get an "albums" field

    albums = orm.relationship('Album', back_populates='artist')


class Album(Base):
    __tablename__ = "album"

    id = orm.mapped_column(db.Integer, primary_key=True)
    title = orm.mapped_column(db.String)
    artist_id = orm.mapped_column(db.Integer, db.ForeignKey("artist.id"))

    # ...and albums get an "artist" field

    artist = orm.relationship('Artist', back_populates='albums')


# Now the metadata is created for our Base class

Base.metadata.create_all(engine)

# We now use a Session rather than a connection

with orm.Session(engine) as session:
    # Now the magic happens
    # https://stackoverflow.com/questions/17325006/how-to-create-a-foreignkey-reference-with-sqlalchemy

    artist1 = Artist(name="Depeche Mode")

    session.add(artist1)

    new_album = Album(title="A Broken Frame", artist=artist1)

    session.add(new_album)

    # Or as a batch

    artist2 = Artist(name="Orbital")
    artist3 = Artist(name="New Order")

    session.add_all(
        [
            Album(title="Violator", artist=artist1),
            Album(title="Orbital", artist=artist2),
            Album(title="Technique", artist=artist3)
        ]
    )

    # Don't forget to commit

    session.commit()

    # Let's get everything (echo gets irritating here, so I turned it off)

    album_query = session.query(Album)

    for album in album_query:
        print(f'{album.title} by {album.artist.name}')

    # Now let's filter

    artist_query = session.query(Album).join(Artist).where(Artist.name == "Depeche Mode")

    for album in artist_query:
        print(f'{album.title} by {album.artist.name}')
