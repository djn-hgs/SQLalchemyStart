import datetime

import sqlalchemy as db
import sqlalchemy.orm as orm

engine = db.create_engine("sqlite+pysqlite:///albums.sqlite", echo=False)


# We no longer need a metadata object
# Now we just create an abstract Base class which has its own metadata

class Base(orm.DeclarativeBase):
    pass

# album_genre = db.Table(
#     "album_genre",
#     Base.metadata,
#     db.Column("album_id", db.Integer, db.ForeignKey("album.id"), primary_key=True),
#     db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True)
# )

class AlbumGenre(Base):
    __tablename__ = "album_genre"

    album_id: orm.Mapped[int] = orm.mapped_column(db.ForeignKey("album.id"), primary_key=True)
    genre_id: orm.Mapped[int] = orm.mapped_column(db.ForeignKey("genre.id"), primary_key=True)


# A slight tweak here - we declare column names and used mapped columns
# There is more to come here

class Artist(Base):
    __tablename__ = "artist"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]

    # Now we have a foreign key we can do something seriously clever
    # This means that artists get an "albums" field

    albums = orm.relationship('Album', back_populates='artist')


class Album(Base):
    __tablename__ = "album"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    title: orm.Mapped[str]
    artist_id: orm.Mapped[int] = orm.mapped_column(db.ForeignKey("artist.id"))

    # ...and albums get an "artist" field

    artist = orm.relationship('Artist', back_populates='albums')
    genres = orm.relationship('Genre', secondary='album_genre', back_populates="albums")

class Genre(Base):
    __tablename__ = "genre"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    label: orm.Mapped[str]

    albums = orm.relationship('Album', secondary='album_genre', back_populates="genres")


# Now the metadata is created for our Base class

Base.metadata.create_all(engine)

# We now use a Session rather than a connection

with (orm.Session(engine) as session):
    # Now the magic happens
    # https://stackoverflow.com/questions/17325006/how-to-create-a-foreignkey-reference-with-sqlalchemy

    # Let's have some genres

    genre1 = Genre(label="Pop")

    session.add(genre1)

    genre2 = Genre(label="Electronic")

    session.add(genre2)

    # And some artists

    artist1 = Artist(name="Depeche Mode")
    artist2 = Artist(name="Orbital")
    artist3 = Artist(name="New Order")

    session.add_all([artist1, artist2, artist3])

    # And an album with artist and genre

    album1 = Album(title="A Broken Frame", artist=artist1)
    album1.genres.append(genre1)
    album1.genres.append(genre2)

    session.add(album1)

    # Or as a batch

    session.add_all(
        [
            Album(title="Violator", artist=artist1),
            Album(title="Orbital", artist=artist2, genres=[genre2]),
            Album(title="Technique", artist=artist3)
        ]
    )

    # Don't forget to commit

    session.commit()

    # Let's get everything (echo gets irritating here, so I turned it off)

    album_query = session.query(Album)

    for album in album_query:
        print(f'{album.title} by {album.artist.name}, {[g.label for g in album.genres]}')

    # Now let's filter

    print('\nJust albums by Depeche Mode\n')

    artist_query = session.query(Album) .join(Artist).where(Artist.name == "Depeche Mode")

    for album in artist_query:
        print(f'{album.title} by {album.artist.name}, {[g.label for g in album.genres]}')

    # Now let's filter on one of our artists

    print(f'\nJust albums by {artist2}\n')

    artist_query = session.query(Album).where(Album.artist == artist2)

    for album in artist_query:
        print(f'{album.title} by {album.artist.name}, {[g.label for g in album.genres]}')

    # And filtering via a link table!

    print('\nNow just "Electronic" music')

    genre_query = session.query(Album).join(AlbumGenre).join(Genre).where(Genre.label == "Electronic")

    for album in genre_query:
        print(f'{album.title} by {album.artist.name}, {[g.label for g in album.genres]}')


