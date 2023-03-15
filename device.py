import tinytuya
import datetime
import pytz

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
            # create a new row in database
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
            #find energy consumption and update the row 
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

    
        

        

    
        