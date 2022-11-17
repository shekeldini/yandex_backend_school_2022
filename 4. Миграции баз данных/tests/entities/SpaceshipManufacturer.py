import csv

from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SpaceshipManufacturerV1(Base):
    __tablename__ = 'spaceship_manufacturer'

    id = Column(INTEGER, primary_key=True)
    company_name = Column(VARCHAR(50), nullable=False)
    country = Column(VARCHAR(50), nullable=True)
    nasdaq_code = Column(VARCHAR(50), nullable=True)

    def __eq__(self, other):
        return self.id == other.id and \
               self.company_name == other.company_name and \
               self.country == other.country and \
               self.nasdaq_code == other.nasdaq_code



def get_spaceship_manufacturers_v1_from_csv():
    manufacturers_list = []
    with open('migrations/init_data/spaceship_manufacturer.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)

        for id, company_name, country, nasdaq_code in reader:
            manufacturer = SpaceshipManufacturerV1()
            manufacturer.id = int(id)
            manufacturer.company_name = company_name
            manufacturer.country = country
            manufacturer.nasdaq_code = nasdaq_code
            manufacturers_list.append(manufacturer)

    return manufacturers_list

