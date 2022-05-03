import os
import psycopg2
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
load_dotenv()
DATABASE_URL = os.environ['DATABASE_URL']

class DataBase():
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    
    def checkUser(self,user_id):
        user_id = str(user_id)
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="SELECT user_id FROM users where user_id = '"+user_id+"'"
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        # 事物提交
        self.conn.commit()
        if row is not None:
            return True
        else:
            return False

    def createUser(self,user_id,user_score):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""INSERT INTO users (user_id,user_score) VALUES (%(user_id)s, %(user_score)s)"""
        params = {'user_id':user_id, 'user_score':user_score}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def getUser(self,user_id):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql = "SELECT * from users WHERE user_id = '"+user_id+"'"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchone()
        json={"user_id":"","user_score":123}
        if row is not None:
            json["user_id"] = row[0]
            json["user_score"] = row[1]
            return json
    
    def SetUserScoreById(self,user_id,score):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="""UPDATE users SET user_score = (%(score)s) WHERE user_id = (%(user_id)s)"""
        params = {'score':score,'user_id':user_id}
        self.cursor.execute(sql,params)
        self.conn.commit()
    
    def getTop5Ranking(self):
        try:
            self.cursor = self.conn.cursor()
        except:
            print("連線以丟失 重連")
            self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            self.cursor = self.conn.cursor()
        sql ="Select user_id, user_score from users ORDER BY user_score desc"
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchmany(5)
        resultjson=[]
        for col in row:
            _reply =str(col[0])+" : $"+str(col[1])
            json={}
            json['id'] = col[0]
            json['score'] = col[1]
            resultjson.append(json)
        return resultjson