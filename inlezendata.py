import sqlalchemy as SA
import pandas as pd

engine = SA.create_engine("mysql+pymysql://root@localhost:3306/world_population?charset=utf8mb4")

wa = "select * from country"
df= pd.read_sql(wa, engine)
print(df.head)