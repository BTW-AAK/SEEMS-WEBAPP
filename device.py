import tinytuya
import datetime
import pytz
import sqlite3

def write_db(dbname,tablename,dev_id,enrgy,st_time,en_time ):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO dashboard_consumption_data(device_id,energy,startime,endtime) VALUES(?,?,?,?)',(dev_id,enrgy,st_time,en_time))
    a =cursor.lastrowid

    return a

def update_row(*args):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute('UPDATE dashboard_consumption_data SET energy = WHERE id = ')
    a =cursor.lastrowid

    return a

class Device:
    def __init__(self, device_name, device_ip, device_id, device_key, device_version):
        self.device_name = device_name
        self.device_ip = device_ip
        self.device_id = device_id
        self.device_key = device_key
        self.device_version = device_version
        self.controller = None
        self.avg_power = 0
        self.device_status = False
        self.start_time = None
        self.end_time = None
        self.row_no = None

    def initialize(self):
        try:
            self.controller = tinytuya.OutletDevice(self.device_id,self.device_ip,self.device_key)
            self.controller.set_version(self.device_version)
            return True
        except:
            print("device connection failed")
            return False
        
    def is_active(self):
        data = self.controller.status()
        try:
            is_on = data['dps']['1']
        except:
            print("couldn't reach device")
            is_on = False
        return is_on, data
    
    def update(self):
        
        current_status, data = self.is_active()
        if self.device_version == '3.1':
            power_measured = data['dps']['5']
        elif self.device_version == '3.3':
            power_measured = data['dps']['19 ]']

        if current_status == True and self.device_status ==False:
            self.avg_power += power_measured
            self.device_status = True
            self.start_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            # write in new row
            self.row_no = write_db(self.device_id, power_measured, self.start_time, self.start_time)
        elif current_status and self.device_status :
            self.avg_power += power_measured
            self.avg_power /=2
            self.end_time =  datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            day_change = False
            if self.end_time.strftime("%d") != self.start_time.strftime("%d"):
                day_change=True
            duration = self.end_time - self.start_time
            duration_in_s = duration.total_seconds()
            hours = duration_in_s/3600
            hours = round(hours,4)
            energy_consumed = self.avg_power*hours

            #find energy consumption and update the row
            update_row('db_name', 'table_name', 'rowid' self.device_id, energy_consumed, self.start_time, self.end_time)
        elif current_status == False and self.device_status ==True:
            self.device_status = False
            self.end_time =  datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            day_change = False
            if self.end_time.strftime("%d") != self.start_time.strftime("%d"):
                day_change=True
            duration = self.end_time - self.start_time
            duration_in_s = duration.total_seconds()
            hours = duration_in_s/3600
            hours = round(hours,4)
            # update the same row for last time
            update_row('db_name', 'table_name', 'rowid' self.device_id, energy_consumed, self.start_time, self.end_time)
            self.avg_power = 0

        else:
            self.device_status = False
            self.avg_power = 0


        
        # if current_status and self.device_status :
        #     self.avg_power += power_measured
        #     self.avg_power /=2
        # elif current_status == True and self.device_status ==False:
        #     self.avg_power += power_measured
        #     self.avg_power /=2
        #     self.device_status = True
        #     self.start_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        # elif current_status == False and self.device_status ==True:
        #     self.device_status = False
        #     self.end_time =  datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        #     day_change = False
        #     if self.end_time.strftime("%d") != self.start_time.strftime("%d"):
        #         day_change=True
        #     duration = self.end_time - self.start_time
        #     duration_in_s = duration.total_seconds()
        #     hours = duration_in_s/3600
        #     hours = round(hours,4)
        #     #write in database the avg power
        #     self.avg_power = 0
        # else:
        #     self.device_status = False
        #     self.avg_power = 0

    
        

        

    
        