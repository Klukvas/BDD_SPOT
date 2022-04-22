from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Numeric
import settings


class DatabaseClient:
    def __init__(self):
        self.engine = create_engine(settings.db_connection_string)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = MetaData(self.engine)
        self.metadata.reflect()


# function needed to client.metadata.tables.values() returns all tables
def get_db_client():
    Base = declarative_base()
    db_client = DatabaseClient()

    def create_table_reflect(table_name, schema_name):
        return Table(table_name, db_client.metadata, autoload_with=db_client.engine, schema=schema_name)

    class RecurringbuyInstructions(Base):
        __table__ = create_table_reflect('instructions', 'recurringbuy')
        __mapper_args__ = {
            'primary_key': [__table__.c.Id]
        }

    class RecurringbuyOrders(Base):
        __table__ = create_table_reflect('orders', 'recurringbuy')
        __mapper_args__ = {
            'primary_key': [__table__.c.Id]
        }

    # needed for db_client to return float instead of Decimal.decimal while querying
    for table in db_client.metadata.tables.values():
        for column in table.columns.values():
            if isinstance(column.type, Numeric):
                column.type.asdecimal = False

    return {'db_client': db_client, 'recurringbuy.instructions': RecurringbuyInstructions,
            'recurringbuy.orders': RecurringbuyOrders}

if __name__ == '__main__':
    client = get_db_client()['d']