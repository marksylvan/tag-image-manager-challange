from chalicelib.db import get_engine
from chalicelib.models import Base

db_engine = get_engine()
Base.metadata.create_all(db_engine)
print("Tables created")
