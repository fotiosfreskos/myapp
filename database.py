import mysql.connector
import sys

def Connect():
    conn= None
    try:
        conn=mysql.connector.Connect(
            host='xxx.xxx.xxx.xxx',
            username='root',
            password='password123',
            database='database'
        )
        print('Connected')
    
    except:
        print('Error',sys.exc_info())

    finally:
        return conn
    
Connect()