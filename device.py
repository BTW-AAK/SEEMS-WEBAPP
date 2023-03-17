import tinytuya
import datetime
import pytz
import sqlite3

def write_db(dev_id,enrgy,st_time,en_time ):
    enrgy = round(enrgy,4)
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO dashboard_consumption_data(device_id,energy,starttime,endtime) VALUES(?,?,?,?)',(dev_id,enrgy,st_time,en_time))
    
    a =cursor.lastrowid
    conn.commit()
    cursor.close()
    print("written, energy: ",enrgy)
    return a

def update_row(row_no,dev_id,energy,st_time,en_time):
    energy = round(energy,4)
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute('UPDATE dashboard_consumption_data SET energy =?, endtime =? WHERE id =? ',(energy,en_time,row_no))
    
    a =cursor.lastrowid
    conn.commit()
    cursor.close()
    print("updated, energy: ",energy)
    return a

class Device:
    def __init__(self, device_name, device_ip, device_id, device_key, device_version):
        self.device_name = device_name
        self.device_ip = device_ip
        self.device_id = device_id
        self.device_key = device_key
        self.device_version = float(device_version)
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
        except Exception as e:
            print("device connection failed")
            print(e)
            return False
        
    def is_active(self):
        data = self.controller.status()
        try:
            is_on = data['dps']['1']
        except Exception as e:
            
            print("couldn't reach device")
            print(e)
            is_on = False
        return is_on, data
    
    def update(self):
        
        current_status, data = self.is_active()
        
        power_measured = 0
        try:
            if self.device_version == 3.1:
                power_measured = data['dps']['5']
            elif self.device_version == 3.3:
                power_measured = data['dps']['19']
        except:
            print("dps not in data")
            current_status = False
        
        power_measured /=10000  

        if current_status == True and self.device_status ==False:
            self.avg_power += power_measured
            self.device_status = True
            self.start_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            # write in new row
            self.row_no = write_db(self.device_id, 0, self.start_time, self.start_time)
        elif current_status and self.device_status :
            self.avg_power += power_measured
            self.avg_power /=2
            self.end_time =  datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            day_change = False
            if self.end_time.strftime("%d") != self.start_time.strftime("%d"):
                day_change=True
            
            if not day_change:
                duration = self.end_time - self.start_time
                duration_in_s = duration.total_seconds()
                hours = duration_in_s/3600
                
                
                hours = round(hours,4)
                energy_consumed = self.avg_power*hours
                
                #find energy consumption and update the row
                update_row( self.row_no ,self.device_id, energy_consumed, self.start_time, self.end_time)
            else:

                n_end = datetime.datetime(datetime.date.today().year, datetime.date.today().month,datetime.date.today().day, 11,59,59)

                #Energy from start time to n_end
                duration = n_end - self.start_time
                duration_in_s = duration.total_seconds()
                hours = duration_in_s/3600
                hours = round(hours,4)
                energy_consumed = self.avg_power*hours
                update_row( self.row_no ,self.device_id, energy_consumed, self.start_time, n_end)

                #Energy from n_end to end time
                duration = self.end_time-n_end
                duration_in_s=duration.total_seconds
                hours = duration_in_s/3600
                hours = round(hours,4)
                energy_consumed=self.avg_power*hours
                self.row_no = write_db( self.device_id, energy_consumed, n_end, self.end_time)
                
        elif current_status == False and self.device_status ==True:
            self.device_status = False
            self.end_time =  datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            day_change = False
            if self.end_time.strftime("%d") != self.start_time.strftime("%d"):
                day_change=True
            if not day_change:
                duration = self.end_time - self.start_time
                duration_in_s = duration.total_seconds()
                hours = duration_in_s/3600
                hours = round(hours,4)
                energy_consumed = self.avg_power*hours
                
                #find energy consumption and update the row
                update_row( self.row_no ,self.device_id, energy_consumed, self.start_time, self.end_time)
            else:

                n_end = datetime.datetime(datetime.date.today().year, datetime.date.today().month,datetime.date.today().day, 11,59,59)

                #Energy from start time to n_end
                duration = n_end - self.start_time
                duration_in_s = duration.total_seconds()
                hours = duration_in_s/3600
                hours = round(hours,4)
                energy_consumed = self.avg_power*hours
                update_row( self.row_no ,self.device_id, energy_consumed, self.start_time, n_end)

                #Energy from n_end to end time
                duration = self.end_time-n_end
                duration_in_s=duration.total_seconds
                hours = duration_in_s/3600
                hours = round(hours,4)
                energy_consumed=self.avg_power*hours
                self.row_no = write_db( self.device_id, energy_consumed, n_end, self.end_time)
            
            self.avg_power = 0

        else:
            self.device_status = False
            self.avg_power = 0


        
        
    
        

        

    
        