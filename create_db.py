import sqlalchemy as db
import sqlalchemy.orm as orm
import model

engine = db.create_engine("sqlite+pysqlite:///albums.sqlite", echo=False)

# The model now provides the Base class and all of our table classes

# Now the metadata is created for our Base class

model.Base.metadata.create_all(engine)

