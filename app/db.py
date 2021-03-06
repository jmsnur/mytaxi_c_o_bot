import mysql.connector
from mysql.connector import errorcode
from datetime import datetime, timedelta
from secret_config import *


def get_day_cancel(date):
    sql = f"""SELECT TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(from_adres, ',',1), ' ',1)) REGION,
                     DATE_FORMAT(date,'%W') DAY,
                     COUNT(*) ORDERS
              FROM max_taxi_incoming_orders
              WHERE status = '8'
              AND date BETWEEN DATE_SUB(DATE_FORMAT('{date}', '%Y-%m-%d'), INTERVAL 1 day) AND '{date}'
              GROUP BY 1,2
              ORDER BY 3 DESC, 1"""

    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PWD,
            database=DB
        )

        mycur = conn.cursor()

        mycur = conn.cursor()
        mycur.execute(sql)
        result = mycur.fetchall()
        if len(result) == 0:
            msg = 'Check the date again, the result is empty'
        else:
            mesg = ''
            for i in range(len(result)):
                raw = f'{result[i][1]} |  {result[i][2]}  | {result[i][0]}\n'
                mesg += raw

            msg = f'{date}\n   DAY   | CANCELED | REGION\n'
            msg += mesg

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            msg = "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            msg = "Database does not exist"
        else:
            msg = err

    conn.commit()
    mycur.close()
    return msg

# date = '2019-11-29'
# get_day_cancel(date)


def month_stat(date_m):
    date = f'{date_m}-01'
    sql = f"""SELECT T1.client_id,
                     T3.AVG_COST,
                     T1.S_ORDER_FREQ,
                     T2.C_ORDER_FREQ,
                     T3.AVG_DR_DIS,
                     T3.AVG_DR_TIME
                FROM (SELECT client_id,
                             (AMOUNT/COUNT(*)) S_ORDER_FREQ
                        FROM
                             (SELECT DATE_FORMAT(date, '%Y-%m-%d') DATE,
                                     DATE_FORMAT(date, '%W') WEEKDAY,
                                     COUNT(*) AMOUNT,
                                     client_id
                                FROM max_taxi_incoming_orders
                               WHERE status = 7
                                 AND date BETWEEN '{date}' AND DATE_ADD('{date}', INTERVAL 1 MONTH)
                            GROUP BY 1,4) as tbl
            GROUP BY 1) AS T1
                JOIN (SELECT client_id,
                             (AMOUNT/COUNT(*)) C_ORDER_FREQ
                        FROM
                             (SELECT DATE_FORMAT(date, '%Y-%m-%d') DATE,
                                     DATE_FORMAT(date, '%W') WEEKDAY,
                                     COUNT(*) AMOUNT,
                                     client_id
                                FROM max_taxi_incoming_orders
                               WHERE status = 8
                                 AND date BETWEEN '{date}' AND DATE_ADD('{date}', INTERVAL 1 MONTH)
                            GROUP BY 1,4) as tbl
                        GROUP BY 1) AS T2
                  ON T2.client_id = T1.client_id
                JOIN (SELECT o.client_id,
                             AVG(total_cost) AVG_COST,
                             AVG(driving_time) AVG_DR_TIME,
                             AVG(driving_distance) AVG_DR_DIS
                        FROM max_taxi_orders_details d
                        JOIN max_taxi_incoming_orders o
                          ON o.id = d.order_id
                         AND o.date BETWEEN '{date}' AND DATE_ADD('{date}', INTERVAL 1 MONTH)
                    GROUP BY 1) AS T3
                  ON T3.client_id = T1.client_id
            ORDER BY 2 DESC;"""

    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PWD,
            database=DB
        )

        mycur = conn.cursor()

        mycur = conn.cursor()
        mycur.execute(sql)
        result = mycur.fetchall()

        if len(result) == 0:
            msg = 'Check the date again, the result is empty'
        else:
            mesg = ''
            for i in range(len(result)):
                raw = f'  {result[i][0]}  | {round(result[i][2],2)} | {round(result[i][3],2)} | {round(result[i][1],2)} | {round(result[i][4],2)} | {round(result[i][5],2)}\n'
                mesg += raw

            msg = f'{date}\nCLIENT_ID|S_O_F |C_O_F | AVG_COST |AVG_DR_DIS|AVG_DR_MIN\n'
            msg += mesg
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            msg = "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            msg = "Database does not exist"
        else:
            msg = err

    conn.commit()
    mycur.close()
    return msg


def interval_req(date_interval):

    string = date_interval
    str_1 = string[:10]
    str_2 = string[11:]

    date1 = datetime.strptime(str_1, "%Y/%m/%d")
    date2 = datetime.strptime(str_2, "%Y/%m/%d")
    
    sql = f"""SELECT client_id,
                     date TIME
                FROM max_taxi_incoming_orders
               WHERE status='8'
                 AND client_id IS NOT NULL
                 AND date BETWEEN '{date1}' AND '{date2}'
            GROUP BY 1,2
            ORDER BY 1,2 DESC;"""


    try:
        conn = mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PWD,
            database=DB
        )

        mycur = conn.cursor()
        mycur.execute(sql)
        result = mycur.fetchall()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            raise "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            raise "Database does not exist"
        else:
            raise err

    conn.commit()
    mycur.close()
    return result
