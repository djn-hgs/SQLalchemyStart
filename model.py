import sqlalchemy as db
import sqlalchemy.orm as orm


# We no longer need a metadata object
# Now we just create an abstract Base class which has its own metadata


class Base(orm.DeclarativeBase):
    pass


album_genre = db.Table(
    "album_genre",
    Base.metadata,
    db.Column("album_id", db.Integer, db.ForeignKey("album.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True)
)


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
    genres = orm.relationship('Genre', secondary='album_genre', back_populates="albums")


class Genre(Base):
    __tablename__ = "genre"

    id = orm.mapped_column(db.Integer, primary_key=True)
    label = orm.mapped_column(db.String)

    albums = orm.relationship('Album', secondary='album_genre', back_populates="genres")

