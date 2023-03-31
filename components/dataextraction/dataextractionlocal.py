import kfp.components as comp
import pandas as pd
import click
import dill


@click.command()
@click.option('--data_file', default='/mnt/bts.data', help='Path to the data file.')

def get_data(data_file):
    # get data from local csv file
    print('Getting data from local csv file...')
    data = pd.read_csv('bts_2021_1.csv')
    print(data.describe())
    with open(data_file, 'w') as f:
        dill.dump(data, f)

    return


def main():
    get_data()
    

