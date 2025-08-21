import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
import os 

ENGINE = create_engine("sqlite:///database.db")

def consume_db(csv_file, schema_description):
    
    df = pd.read_csv(csv_file, sep=";")
    file_name = csv_file.name
    table_name = os.path.splitext(file_name)[0]
    df.to_sql(table_name, ENGINE, if_exists="replace", index=False)
    metadata = MetaData()
    sales_table = Table(table_name, metadata, autoload_with=ENGINE)

    db_information = f"""Database is ready to use with the name '{table_name}'.
    The database schema is:
    {schema_description}"""

    return df, sales_table, db_information