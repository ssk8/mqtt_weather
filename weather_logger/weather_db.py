import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime

engine = sa.create_engine("sqlite:///weather.db")

Session = so.sessionmaker(bind=engine)
session = Session()

Base = so.declarative_base()


class DataPoint(Base):
    __tablename__ = "data_points"
    created_date = sa.Column(sa.DateTime, default=datetime.now, primary_key=True)
    topic = sa.Column(sa.String(60))
    temperature = sa.Column(sa.Float(), nullable=True)
    pressure = sa.Column(sa.Float(), nullable=True)
    humidity = sa.Column(sa.Float(), nullable=True)

    def __repr__(self):
        return f"{datetime.now():%H:%M:%S} - {self.topic}: temp:{self.temperature}°C, press:{self.pressure} hPa, humid:{self.humidity}%"


Base.metadata.create_all(engine)
