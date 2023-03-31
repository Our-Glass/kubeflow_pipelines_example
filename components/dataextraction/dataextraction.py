# get data from sql server wih pandas and save it as parquet file

import pyodbc
import pandas as pd
import kfp.components as comp
import click
import dill

def connect_sql():
    # connect to sql server
    print('Connecting to SQL Server...')
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1,1433;DATABASE=master;PWD=Adminxyz22#;UID=SA')
    print('Connected to SQL Server')
    return conn

@click.command()
@click.option('--data_file', default='/mnt/bts.data', help='Path to the data file.')
def get_data(data_file):
    # get data from sql server
    print('Getting data from SQL Server...')
    conn = connect_sql()
    data = pd.read_sql('SELECT * FROM BTS', conn)
    conn.close()
    print(data.describe())
    with open(data_file, 'w') as f:
        dill.dump(data, f)

    return


def main():
    get_data()

if __name__ == '__main__':
    main()


