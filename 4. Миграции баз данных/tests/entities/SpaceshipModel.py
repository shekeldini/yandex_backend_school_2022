import csv

from sqlalchemy import Column, INTEGER, VARCHAR
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SpaceshipModel(Base):
    __tablename__ = 'spaceship_model'

    id = Column(INTEGER, primary_key=True)
    manufacturer_id = Column(INTEGER, nullable=False)
    model_name = Column(VARCHAR(50), nullable=True)
    horsepower = Column(DOUBLE, nullable=False)

    def __eq__(self, other):
        return self.id == other.id and \
               self.manufacturer_id == other.manufacturer_id and \
               self.model_name == other.model_name and \
               self.horsepower == other.horsepower


def get_spaceship_models_from_csv():
    models_list = []
    with open('migrations/init_data/spaceship_model.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)

        for id, manufacturer_id, model_name, horsepower in reader:
            model = SpaceshipModel()
            model.id = int(id)
            model.manufacturer_id = int(manufacturer_id)
            model.model_name = model_name
            model.horsepower = float(horsepower)
            models_list.append(model)

    return models_list
