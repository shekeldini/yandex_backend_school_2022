import csv

from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Spaceship(Base):
    __tablename__ = 'spaceship'

    id = Column(INTEGER, primary_key=True)
    ship_number = Column(VARCHAR(50), nullable=False)
    model_id = Column(INTEGER, nullable=True)

    def __eq__(self, other):
        return self.id == other.id and \
               self.ship_number == other.ship_number and \
               self.model_id == other.model_id


def get_spaceships_from_csv():
    ships_list = []
    with open('migrations/init_data/spaceship.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)

        for id, ship_number, model_id in reader:
            ship = Spaceship()
            ship.id = int(id)
            ship.ship_number = ship_number
            ship.model_id = int(model_id)
            ships_list.append(ship)

    return ships_list
