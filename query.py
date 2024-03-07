import sqlalchemy as db
import sqlalchemy.orm as orm
import model

engine = db.create_engine("sqlite+pysqlite:///albums.sqlite", echo=False)


# We now use a Session rather than a connection

with (orm.Session(engine) as session):

    # Let's get everything (echo gets irritating here, so I turned it off)

    album_query = session.query(model.Album)

    for album in album_query:
        print(f'{album.title} by {album.artist.name}, {[g.label for g in album.genres]}')

    # Now let's filter

    print('\nJust albums by Depeche Mode\n')

    artist_query = session.query(model.Album) .join(model.Artist).where(model.Artist.name == "Depeche Mode")

    for album in artist_query:
        print(f'{album.title} by {album.artist.name}, {[g.label for g in album.genres]}')

    # Now let's filter on one of our artists

    print(f'\nJust albums by Orbital\n')

    artist_query = session.query(model.Album).join(model.Artist).where(model.Artist.name == "Orbital")

    for album in artist_query:
        print(f'{album.title} by {album.artist.name}, {[g.label for g in album.genres]}')

    # And filtering via a link table!

    print('\nNow just "Electronic" music')

    genre_query = session.query(model.Album).join(model.album_genre).join(model.Genre).where(model.Genre.label == "Electronic")

    for album in genre_query:
        print(f'{album.title} by {album.artist.name}, {[g.label for g in album.genres]}')


