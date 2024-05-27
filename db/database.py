from sqlalchemy import create_engine
from sqlalchemy.orm import decorative_bse, sessionmaker

ENGINE = create_engine('postgresql://postgres:23042005.o@localhost/fast', echo=True)
Session = sessionmaker()
Base = decorative_base()
