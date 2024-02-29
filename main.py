import sqlalchemy as db
import sqlalchemy.orm as orm

engine = db.create_engine("sqlite+pysqlite:///albums.sqlite", echo=True)

# We no longer need a metadata object
# Now we just create an abstract Base class which has its own metadata

class Base(orm.DeclarativeBase):
    pass

# A slight tweak here - we declare column names and used mapped columns
# There is more to come here

class Album(Base):
    __tablename__ = "album"

    id = orm.mapped_column(db.Integer, primary_key=True)
    name = orm.mapped_column(db.String)
    artist = orm.mapped_column(db.String)

# Now the metadata is created for our Base class

Base.metadata.create_all(engine)

# We now use a Session rather than a connection

with orm.Session(engine) as session:
    # So to add to our table we can now just create an instance and add it

    new_album = Album(name="A Broken Frame", artist="Depeche Mode")

    session.add(new_album)

    # And now we can query it "session.scalars" is always a bit odd, i think

    for album in session.scalars(db.select(Album)):
        print(f'{album.name} by {album.artist}')

    # And to add many items

    session.add_all(
        [
            Album(name="Violator", artist="Depeche Mode"),
            Album(name="Orbital", artist="Orbital"),
            Album(name="Technique", artist="New Order")
        ]
    )

    # Don't forget to commit

    session.commit()

    artist_query = db.select(Album).where(Album.artist=="Depeche Mode")

    for album in session.scalars(artist_query):
        print(f'{album.name} by {album.artist}')

