from tools.db_connection import get_connection
import pandas as pd

def execute(sql):
    with get_connection() as conn:
        return pd.read_sql(sql, conn)
