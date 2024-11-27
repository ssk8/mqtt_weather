from datetime import datetime, timedelta
from weather_db import session, DataPoint

points = session.query(DataPoint).filter(
    DataPoint.created_date.between(
        datetime.now() - timedelta(minutes=10), datetime.now()
    )
)


for point in points:
    print(point)
