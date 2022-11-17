import csv

from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DriverV2(Base):
    __tablename__ = 'driver'

    id = Column(INTEGER, primary_key=True)
    full_name = Column(VARCHAR(255), nullable=False)
    login = Column(VARCHAR(50), unique=True, nullable=False)
    city = Column(VARCHAR(30), nullable=True)

    def __eq__(self, other):
        return self.id == other.id and \
               self.full_name == other.full_name and \
               self.login == other.login and \
               self.city == other.city

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


def get_drivers_v2_from_csv():
    drivers_list = []
    with open('migrations/init_data/driver.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)

        for id, name, last_name, login, city in reader:
            driver = DriverV2()
            driver.id = int(id)
            driver.full_name = name + " " + last_name
            driver.login = login
            driver.city = city
            drivers_list.append(driver)

    return drivers_list
