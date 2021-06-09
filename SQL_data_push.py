import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd

##############################################################################################

def rds_push(df, host_ , username ,user_password, database_name):
    try:
        conn = mysql.connect(host=host_, database=database_name, user=username, password=user_password)
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()

            print("You're connected to database: ", record)
            print('Creating table....')

            cursor.execute("CREATE TABLE single_vehicle_data(Sl_NO INT, TIME_ DATETIME, Latitude FLOAT, Longitude FLOAT, Altitude FLOAT, RPM FLOAT, Driver_Demand_Torque FLOAT, Engine_Load FLOAT ,    Engine_Torque_Mode FLOAT ,    TPS FLOAT ,    Percent_Load_Curret_Speed FLOAT ,    Fuel_Rate FLOAT ,    VEHICLE_SPEED FLOAT ,    Inj_Q_Cur FLOAT ,    Inj_Q_Tor FLOAT ,    Boost_Pressure FLOAT,    Atmospheric_Pressure  FLOAT,    Coolant_Temperature FLOAT,    Oil_Temperature FLOAT,    Boost_Temperature FLOAT,    Oil_Pressure FLOAT,    Battery_Voltage FLOAT,    Cam_Speed FLOAT,    Rail_Pressure FLOAT,    Rail_Pressure_set FLOAT,    MU_PWM FLOAT,    MU_Vol FLOAT,    Torque_Rat FLOAT,    Torque FLOAT,    TQ_Limit_Set FLOAT,    Main_Injection FLOAT,    Pilot_Injection FLOAT,    Pos_2_Injector FLOAT,	EGR_Prop FLOAT,    EGR_Pos_D FLOAT,    EGR_Pos_A FLOAT,    Clutch_Switch FLOAT ,    Brake_Switch FLOAT,    Engine_Grad FLOAT,    param1 VARCHAR(100) ,    param2 VARCHAR(100) )")
            print("Table is created....")

            for i,row in df.iterrows():
                sql = "INSERT INTO vehicle_data.single_vehicle_data VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, tuple(row))
                print("Record inserted")
                conn.commit()
    except Error as e:
                print("Error while connecting to MySQL", e)

###############################################################################################