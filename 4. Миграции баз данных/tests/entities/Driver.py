import csv

from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DriverV1(Base):
    __tablename__ = 'driver'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    last_name = Column(VARCHAR(50), nullable=False)
    login = Column(VARCHAR(50), unique=True, nullable=False)
    city = Column(VARCHAR(30), nullable=True)

    def __eq__(self, other):
        return self.id == other.id and \
               self.name == other.name and \
               self.last_name == other.last_name and \
               self.login == other.login and \
               self.city == other.city

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


def get_drivers_v1_from_csv():
    drivers_list = []
    with open('migrations/init_data/driver.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)

        for id, name, last_name, login, city in reader:
            driver = DriverV1()
            driver.id = int(id)
            driver.name = name
            driver.last_name = last_name
            driver.login = login
            driver.city = city
            drivers_list.append(driver)

    return drivers_list