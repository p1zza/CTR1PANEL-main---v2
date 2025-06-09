import psycopg2
from os import path

from random import randint
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="db",
            #host = "0.0.0.0",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        conn.close()
        return conn
        
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных postgres")
        print(e)

        raise

create_table_cargo = """ CREATE TABLE IF NOT EXISTS "Cargo" (
                        "id" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
                        "name" VARCHAR (50) NOT NULL,
                        "cargotype" VARCHAR(50) NOT NULL,
                        "amount" integer NOT NULL,
                        "status" BOOLEAN NOT NULL,
                        "pass" VARCHAR(4) NOT NULL,
                        "info" VARCHAR (50) NULL); """

create_table_users = """CREATE TABLE IF NOT EXISTS "Users" (
                        user_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
                        username VARCHAR (50) UNIQUE NOT NULL, 
                        password VARCHAR (50) NOT NULL, 
                        is_captain VARCHAR(1),
                        comment VARCHAR (256));"""

create_table_vagon = """ CREATE TABLE IF NOT EXISTS "Vagon" (
                        "id" INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY NOT NULL,
                        "vagontype" VARCHAR(50) NOT NULL,
                        "workers" integer NOT NULL,
                        "status" BOOLEAN NOT NULL); """

#=================
insert_into_cargo = """INSERT INTO "Cargo" (name, cargotype, amount, status, pass) VALUES 
                                        ('Свинина', 'Мясо','12',True,'1234'),
                                        ('Инструменты', 'Техника','3',True,'1234'),
                                        ('Исследования', 'Наука','17',True,'1234');"""

insert_into_users = """INSERT INTO "Users"(username,password,is_captain) VALUES
                        ('admin', 'password','1'),
                        ('user', 'user', '0');"""

insert_into_vagon = """INSERT INTO "Vagon"(vagontype,workers,status) VALUES
                        ('Head', '1','True'),
                        ('Accounting', '1', 'True'),
                        ('Cargo', '1', 'True');"""

#=======

def connect_to_mainbase():
    try:
        conn = psycopg2.connect(
            dbname="ctr1panel",
            user="postgres",
            password="postgres",
            host="db",
            #host = "0.0.0.0",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print("Ошибка подключения к ctr1panel")
        print(e)
        
#init
def createDB():
    try:
        conn = connect_to_db()
        # Создаем базу данных если не существует
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname='ctr1panel'")
            if not cur.fetchone():
                cur.execute("CREATE DATABASE ctr1panel;")
                print("База данных ctr1panel создана")
                cur.close()
        
        # Закрываем соединение с postgres
        conn.close()
        
        # Подключаемся к новой БД
        conn = psycopg2.connect(
            dbname="ctr1panel",
            user="postgres",
            password="postgres",
            host="db",
            #host = "0.0.0.0",
            port="5432"
        )

        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("CREATE DATABASE CTR1PANEL;")
        cur.execute("CREATE USER username WITH PASSWORD 'password' SUPERUSER;")
        cur.execute("GRANT ALL PRIVILEGES ON DATABASE CTR1PANEL TO username;")
        conn.commit()
        conn.close()
        print("Создана БД CTR1PANEL, добавлен пользователь Username")
        
    except psycopg2.Error as e:
        print("БД CTR1Panel с пользователем username не была создана")
        print("Error: Unable to connect to the database")
        print(e)
    
    try:
        conn = psycopg2.connect(
        dbname="ctr1panel",
        user="postgres",
        password = "postgres",
        #host = "0.0.0.0",
        host="db",
        port="5432"
        )
        cur = conn.cursor()
        cur.execute(create_table_cargo)
        cur.execute(create_table_users)
        cur.execute(create_table_vagon)
        cur.execute(insert_into_cargo)
        cur.execute(insert_into_users)
        cur.execute(insert_into_vagon)
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        print(e)

#Users
def getUsers():
    _out = []
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
        cur.execute('SELECT username FROM "Users";')
        out = cur.fetchall()
        for i in out:
            _out.append(i[0])
        return _out

def getUser(username):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('SELECT * FROM "Users" WHERE username = \'%s\';' %username)
            return cur.fetchall()

def getUserID(username):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('SELECT user_id FROM "Users" WHERE username = \'%s\';' %username)
            return cur.fetchall()

def insertUser(name,password):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('INSERT INTO "Users" (username,password,is_captain) VALUES (\'%s\',\'%s\',0);' %(name,password))
            conn.commit()

def selectUserComment(username):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('SELECT comment FROM "Users" WHERE username = %s;' %username)
            return cur.fetchall()

def updateUserComment(username,comment):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('UPDATE "Users" SET comment = \'%s\' WHERE username = \'%s\';' %(comment,username))
            conn.commit()
    

#HeadVagon
def getWorkersAmount(vagon):
    out = ""
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('SELECT workers FROM "Vagon" WHERE vagontype = %s;' % vagon)
            out = cur.fetchall()
            a = out[0]
            return a[0]

def updateWorkersAmount(workers,vagonType):
    out = 'UPDATE "Vagon" SET workers = %s WHERE vagontype = %s;' %(workers,vagonType)
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute(out)
            conn.commit()

#VagonStatus
def getVagonStatus(vagon):
    str_ = 'SELECT status FROM "Vagon" WHERE vagontype = %s;' % vagon
    out = ""
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute(str_)
            out = cur.fetchall()
    if out[0] == (True,):
        return "Чисто"
    else:
        return "Грязно"

def updateVagonStatus(status,vagonType):
    out = 'UPDATE "Vagon" SET status =%s WHERE vagontype = %s;' %(status,vagonType)
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute(out)
            conn.commit()

def getAccountingStatus(vagon):
    if getWorkersAmount('\'Head\'') > 0:
        return "Работает"
    else:
        return "Не работает, недостаточно человекочасов"
#Capitans
def updateCaptain(name):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
        cur.execute('UPDATE "Users" SET is_captain = \'1\' WHERE username = \'%s\';' %name)
        conn.commit()

def getCapitansList():
    _out = []
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('SELECT username from "Users" WHERE is_captain = \'1\';')
            out = cur.fetchall()
            for i in out:
                _out.append(i[0])
            return _out


#Cargo
def insertCargo(selectedType,cargoName,cargoAmount,cargoPass,cargoComment):
    sql = 'INSERT INTO "Cargo" ("name","cargotype","amount", "status", "pass", "info") VALUES (\'%s\',\'%s\',\'%s\',\'True\',\'%s\',\'%s\');' %(cargoName, selectedType,cargoAmount,cargoPass,cargoComment)
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
        try:
            cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(e)
            return "Database error", 500

def getCargoType(cargoType):
    conn = connect_to_mainbase()
    sql = 'SELECT cargotype from "Cargo" WHERE name = %s;' %cargoType
    with conn.cursor() as cur:
            cur.execute(sql)
            out = cur.fetchall()
            a = out[0]
            return a[0]

def getCargoTypeArray():
    _out = []
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('SELECT cargotype from "Cargo";')
            out = cur.fetchall()
            for i in out:
                _out.append(i[0])
            return _out

def getCargoNameArray(cargotype):
    _out = []
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('SELECT name from "Cargo" WHERE cargotype = %s;' %cargotype)
            out = cur.fetchall()
            for i in out:
                _out.append(i[0])
            return _out


def getAllCargoAmount():
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            cur.execute('SELECT amount from "Cargo";')
            out = cur.fetchall()
            amount = 0
            for i in out:
                amount += i[0]
            return amount

def getCargoAmount(cargoType):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            sql = 'SELECT amount from "Cargo" WHERE cargotype = %s;' %cargoType
            cur.execute(sql)
            out = cur.fetchall()
            a = out[0]
            return a[0]

def getCargoStatus(cargoType):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            sql = 'SELECT status from "Cargo" WHERE cargotype = %s;' %cargoType
            cur.execute(sql)
            out = cur.fetchall()
            a = out[0]
            return a[0]

def updateCargoStatus(cargoName):
    conn = connect_to_mainbase()
    out = 'UPDATE "Cargo" SET status = False WHERE cargotype = %s;' %(cargoName)
    with conn.cursor() as cur:
            cur.execute(out)
            conn.commit()

def updateCargoName(cargoType,cargoName):
    conn = connect_to_mainbase()
    out = 'UPDATE "Cargo" SET name = \'%s\' WHERE cargotype = %s;' %(cargoType, cargoName)
    with conn.cursor() as cur:
            cur.execute(out)
            conn.commit()

def getCargoName(cargoType):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            sql = 'SELECT name from "Cargo" WHERE cargotype = %s;' %cargoType
            cur.execute(sql)
            out = cur.fetchall()
            a = out[0]
            return a[0]

def getCargoComment(cargoName):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
            sql = 'SELECT info from "Cargo" WHERE name = \'%s\';' %cargoName
            cur.execute(sql)
            out = cur.fetchall()
            a = out[0]
            return a[0]

def getCargoPass(cargoType):
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
        sql = 'SELECT pass from "Cargo" WHERE cargotype = %s;' %cargoType
        cur.execute(sql)
        out = cur.fetchall()
        a = out[0]
        return a[0]

def updateCargoPass(cargoName,cargoPass):
    out = 'UPDATE "Cargo" SET pass =%s WHERE cargotype = %s;' %(cargoPass,cargoName)
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
        cur.execute(out)
        conn.commit()
        out = cur.fetchall()
        return out

def renewCargo():
    conn = connect_to_mainbase()
    with conn.cursor() as cur:
        cur.execute('UPDATE "Cargo" SET status = True WHERE cargotype = \'Мясо\';')
        cur.execute('UPDATE "Cargo" SET status = True WHERE cargotype = \'Техника\';')
        cur.execute('UPDATE "Cargo" SET status = True WHERE cargotype = \'Наука\';')
        conn.commit()

            
