__author__ = 'Dengbo'

import pymysql
import configparser


class Database:

    cf = configparser.ConfigParser()
    cf.read("config.ini")
    HOST = cf.get('mysql', 'host')
    USER = cf.get('mysql', 'user')
    PWD = cf.get('mysql', 'password')
    DB = cf.get('mysql', 'db')

    def __init__(self):
        try:
            self.conn = pymysql.connect(self.HOST, self.USER, self.PWD, self.DB)
            self.cursor = self.conn.cursor()
        except:
            print("Error: connect mysql error")

    def self_sql(self, sql, param):
        try:
            self.cursor.execute(sql, param)
            self.conn.commit()
            data = self.cursor.fetchone()
            self.cursor.close()
            self.conn.close()
            return data[0]
        except:
            return -1