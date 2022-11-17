import csv
from datetime import datetime, time

from sqlalchemy import Column, INTEGER, VARCHAR, DATETIME
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SpaceshipRent(Base):
    __tablename__ = 'spaceship_rent'

    driver_id = Column(INTEGER, nullable=False, primary_key=True)
    spaceship_id = Column(INTEGER, nullable=False, primary_key=True)
    rent_start = Column(DATETIME, nullable=False)
    rent_end = Column(DATETIME, nullable=False)

    def __eq__(self, other):
        return self.driver_id == other.driver_id and \
               self.spaceship_id == other.spaceship_id and \
               str(self.rent_start) == str(other.rent_start) and \
               str(self.rent_end) == str(other.rent_end)


def get_spaceship_rent_from_csv():
    rent_list = []
    with open('migrations/init_data/spaceship_rent.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)

        for driver_id, spaceship_id, rent_start, rent_end in reader:
            rent = SpaceshipRent()
            rent.driver_id = int(driver_id)
            rent.spaceship_id = int(spaceship_id)
            rent.rent_start = rent_start
            rent.rent_end = rent_end
            rent_list.append(rent)

    return rent_list
