#!/usr/bin/env python
#coding=utf-8

import time
import config
import MySQLdb
import logging
import types

def run_sql(sql):
    '''执行sql语句,并返回结果'''
    con = None
    while True:
        try:
            con = MySQLdb.connect(config.sql_server_host,config.sql_server_username,config.sql_server_password,
                                  config.sql_server_db_name,charset=config.sql_server_db_charset)
            break
        except: 
            logging.error('Cannot connect to database,trying again')
            time.sleep(1)
    cur = con.cursor()
    try:
        if type(sql) == types.StringType:
            cur.execute(sql)
        elif type(sql) == types.ListType:
            for i in sql:
                cur.execute(i)
    except MySQLdb.OperationalError,e:
        logging.error(e)
        cur.close()
        con.close()
        return False
    con.commit()
    data = cur.fetchall()
    cur.close()
    con.close()
    return data



