import time
import math
import sqlite3
# add = create, get = conclusion

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addRev(self, name, revi, carbrand):
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO rev VALUES(NULL, ?, ?, ?, ?)", (name, revi, carbrand, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления Отзыва в БД " + str(e))
            return False
        return True

    def getRev(self):
        try:
            self.__cur.execute(f"SELECT name, revi, carbrand, time FROM rev")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка " + str(e))

        return (False, False)

    def addPost(self, title, text, url):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res ['count'] > 0:
                print("Статья с таким url уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)", (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка addPost добавления Отзыва в БД " + str(e))
            return False
        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}'")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка getPost получения статьи из БД "+str(e))

        return (False, False)

    def getPostAnonce(self):
        try:
            self.__cur.execute(f"SELECT title, text, url, time FROM posts ORDER BY time DESC ")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка " + str(e))
        return (False, False)

    def getServAnonce(self):
        try:
            self.__cur.execute(f"SELECT title, text, url FROM services ")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка " + str(e))
        return (False, False)

    def getServ(self, alias):
        try:
            self.__cur.execute(f"SELECT title, text FROM services WHERE url LIKE '{alias}'")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка getServ получения статьи из БД " + str(e))

        return (False, False)

    def getTests(self):
        try:
            self.__cur.execute(f"SELECT name, text FROM test")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка " + str(e))

        return (False, False)