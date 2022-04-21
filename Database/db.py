from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table
import settings

class DatabaseClient:
    def __init__(self):
        self.engine = create_engine(settings.db_connection_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = MetaData(self.engine)
        self.metadata.reflect()


Base = declarative_base()

def create_table_reflect(table_name, schema_name, db_connection):
    return Table(table_name, db_connection.metadata, autoload_with=db_connection.engine, schema=schema_name)

def recurringbuy_instructions_table(db_connection):
    class RecurringbuyInstructions(Base):
        __table__ = create_table_reflect('instructions', 'recurringbuy', db_connection)
        __mapper_args__ = {
            'primary_key': [__table__.c.Id]
        }
    return RecurringbuyInstructions

def recurringbuy_orders_table(db_connection):
    class RecurringbuyOrders(Base):
        __table__ = create_table_reflect('orders', 'recurringbuy', db_connection)
        __mapper_args__ = {
            'primary_key': [__table__.c.Id]
        }
    return RecurringbuyOrders
