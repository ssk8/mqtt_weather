from datetime import datetime, timedelta
from weather_db import session, DataPoint
import pandas as pd
import matplotlib.pyplot as plt

points = session.query(DataPoint).filter(
    DataPoint.created_date.between(
        datetime.now() - timedelta(days=1), datetime.now()
    )
)

time_temp = pd.read_sql_query(points.statement, points.session.bind)

plot = time_temp.plot.line(x="created_date", y="temperature")

plt.show()