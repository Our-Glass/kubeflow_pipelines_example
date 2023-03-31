# push bts data to sqlserver database

import pyodbc
import pandas as pd
import os


SERVER = '34.69.52.179'
DATABASE = 'master'
USERNAME = 'sa'
PASSWORD = 'h#rl7Ps1AJ74'

def get_data():
    # get data from csv file
    print('Getting data from csv file...')
    data = pd.read_csv('bts_2021_1.csv')
    return data

def connect_sql():
    # connect to sql server
    print('Connecting to SQL Server...')
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (SERVER, DATABASE, USERNAME, PASSWORD))
    #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost,1433;DATABASE=master;PWD=Adminxyz22#;UID=SA')
    print('Connected to SQL Server')
    return conn

def push_data(data, conn):
    # push data to sql server
    print('Pushing data to SQL Server...')
    cursor = conn.cursor()
    for index, row in data.iterrows():
        cursor.execute('INSERT INTO BTS VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', row['query'], row['url'], row['title'], row['upload_date'], row['channel'], row['views'], row['likes'], row['dislikes'], row['comment_count'], row['comment_text'], row['comment_author'], row['comment_date'], row['comment_likes'])
        conn.commit()
    cursor.close()
    conn.close()


def create_bts():
    # create table BTS if not exist
    conn = connect_sql()
    cursor = conn.cursor()
    print('Creating table BTS...')
    cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BTS' and xtype='U')
        CREATE TABLE BTS (
            query VARCHAR(255),
            url VARCHAR(255),
            title VARCHAR(255),
            upload_date VARCHAR(255),
            channel VARCHAR(255),
            views VARCHAR(255),
            likes VARCHAR(255),
            dislikes VARCHAR(255),
            comment_count VARCHAR(255),
            comment_text VARCHAR(255),
            comment_author VARCHAR(255),
            comment_date VARCHAR(255),
            comment_likes VARCHAR(255)
        )
    ''')
    cursor.execute("ALTER TABLE BTS ALTER COLUMN comment_text VARCHAR(MAX)")
    conn.commit()

def main():
    data = get_data()
    # create table BTS if not exist
    create_bts()
    conn = connect_sql()
    push_data(data, conn)

if __name__ == '__main__':
    main()