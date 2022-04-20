from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
import settings

class DatabaseClient:
    def __init__(self):
        self.engine = create_engine(settings.db_connection_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = MetaData(self.engine)
        self.metadata.reflect()
