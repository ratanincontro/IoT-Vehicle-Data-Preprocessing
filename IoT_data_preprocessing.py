import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def dm(x):
    degrees = int(x) // 100
    minutes = x - 100*degrees

    return degrees, minutes

def decimal_degrees(degrees, minutes):
    return degrees + minutes/60 

def df_assign_column_names(dataset):
    
    dataset = pd.read_csv(dataset, 
                         names=['Time','Latitude','Longitude','Altitude','RPM' ,
                        'Driver Demand Torque (%)','Engine Load (%)','Engine Torque Mode','TPS (%)','Percent Load Curret Speed','Fuel Rate (L-Hr)',
                        'Vehicle Speed ','Inj Q Cur (mg-st)','Inj Q Tor (mg-st)','Boost Pressure (mBar)','Atmospheric Pressure (mBar)','Coolant Temperature (*C)',
                        'Oil Temperature (*C)','Boost Temperature (*C)','Oil Pressure (mBar)','Battery Voltage (V)','Cam Speed (rpm)',
                        'Rail Pressure (mBar)','Rail Pressure set (mBar)','MU PWM (%)','MU Vol (mm3-s)','Torque Rat','Torque (Nm)','TQ Limit Set','Main Injection (mg-st)',
                        'Pilot Injection (mg-st)','Pos 2 Injector (mg-st)',
                        'EGR Prop (%)','EGR Pos D (%)','EGR Pos A (%)','Clutch Switch','Brake Switch','Engine Grad (rpm)','param1','param2','0'])
    
    return dataset

def preprocess(dataset):

    dataset = dataset.fillna(0)

    ##################################################################

    #Search for engine stopping or file overflow
    for i in range(0,len(dataset)):
        if dataset['Latitude'][i] == 'ENG STOPPED':
            mi = i
        elif dataset['Latitude'][i] == 'FILE OVERFLOW':
            mi = i

    #Taking date and droping useless data
    date_from_sheet = dataset.iloc[-9][0]
    dataset.drop(dataset.tail(len(dataset)-mi).index,inplace = True)
    dataset = dataset.drop(dataset.columns[-1],axis=1)


    #date cleanup
    date_from_sheet = date_from_sheet.split()
    date_raw = []
    date_raw.append(date_from_sheet[2])

    for number in date_raw:
        str_number = str(number)
        date = ('{}/{}/20{}'. format(str_number[:2], str_number[2:4], str_number[4:]))

    ###################################################################

    #Time
    raw_time_converted = []
    for a in dataset['Time']:

        h = int(a[0:2])
        m = int(a[2:4])
        s = str(a[4:6])

        h = h+5
        m = m+30

        if m == 60:
            h = h+1
            m = str(00)

        elif m > 60:
            m = m - 60
            h = h + 1

        raw_time_converted.append((str(h).zfill(2))+(str(m).zfill(2))+(str(s).zfill(2)))

    raw_time_new = []

    for each_time in raw_time_converted:
        str_time = str(each_time)
        time = ('{}:{}:{}'. format(str_time[:2], str_time[2:4], str_time[4:]))
        raw_time_new.append(time)

    #combining date and time
    date_time_list = []

    for time_new in raw_time_new:
        date_time_list.append(date+' '+time_new)

    #replacing date and time in dataset
    dataset.drop('Time',axis=1)
    dataset['Time'] = (date_time_list)
    
    ###################################################################
    #Latitude and Longitude
    lat_list = []
    for i in dataset['Latitude']:
        if i != 0:
            lat_list.append(decimal_degrees(*dm(float(i))))
        elif i == 0:
            lat_list.append(0)

    long_list = []
    for i in dataset['Longitude']:
        if i != 0:
            long_list.append(decimal_degrees(*dm(float(i))))
        elif i == 0:
            long_list.append(0)

    #drop and replacing values
    dataset.drop('Latitude',axis=1)
    dataset['Latitude'] = (lat_list)

    dataset.drop('Longitude',axis=1)
    dataset['Longitude'] = (long_list)
    
    ###################################################################
    #RPM
    
    rpm_list = []

    for i in dataset['RPM']:
        if i != 0:
            old_list = []
            for j in i:
                old_list.append(j)
            rearrange = ' '+ old_list[2] + old_list[3] + old_list[0] + old_list[1]
            rpm_list.append((int(rearrange,16)*0.125))
        elif i == 0:
            rpm_list.append(0)

    #drop and replace
    dataset.drop('RPM',axis=1)
    dataset['RPM'] = (rpm_list)
    
    ###################################################################
    #Driver Demand Torque
    ddt = []
    for i in dataset['Driver Demand Torque (%)']:
        if i != 0:
            ddt.append((int(i,16))+(-125))
        else:
            ddt.append(0)

    dataset.drop('Driver Demand Torque (%)',axis=1)
    dataset['Driver Demand Torque (%)'] = (ddt)
    
    ###################################################################
    #Engine load
    engine_load = []

    for i in dataset['Engine Load (%)']:
        if i != 0:
            engine_load.append((int(i,16))+(-125))
        else:
            engine_load.append(0)

    dataset.drop('Engine Load (%)',axis=1)
    dataset['Engine Load (%)'] = (engine_load)
    
    ###################################################################
    #Engine Torque Mode
    ETMode = []

    for i in dataset['Engine Torque Mode']:
        if i != 0:
            ETMode.append(int(i,16)-125)
        else:
            ETMode.append(0)  

    dataset.drop('Engine Torque Mode',axis=1)
    dataset['Engine Torque Mode'] = (ETMode)

    ###################################################################
    #TPS %
    TPS = []

    for i in dataset['TPS (%)']:
        if i != 0:
            TPS.append((int(i,16))*0.4)
        else:
            TPS.append(0)  

    dataset.drop('TPS (%)',axis=1)
    dataset['TPS (%)'] = (TPS)

    ###################################################################
    #Load Current Speed
    LCS = []

    for i in dataset['Percent Load Curret Speed']:
        if i != 0:
            LCS.append((int(i,16))*1)
        else:
            LCS.append(0)

    dataset.drop('Percent Load Curret Speed',axis=1)
    dataset['Percent Load Curret Speed'] = (LCS)

    ###################################################################
    #Fuel Rate
    FRate = []

    for i in dataset['Fuel Rate (L-Hr)']:
        if i != 0:
            FRate.append((int(i,16))*0.05)
        else:
            FRate.append(0)

    dd = []
    for i in FRate:
        dd.append(float(i))

    FRate_featurescaled = []
    FRateOldRange = (max(dd) - min(dd))  
    FRateNewRange = (40 - 0)  
    for i in dd:
        FRateNewValue = (((i - 0) * FRateNewRange) / FRateOldRange) + 0
        FRate_featurescaled.append(FRateNewValue)

    dataset.drop('Fuel Rate (L-Hr)',axis=1)
    dataset['Fuel Rate (L-Hr)'] = (FRate_featurescaled)

    ###################################################################
    #Vehicle Speed
    VSpeed = []

    for i in dataset['Vehicle Speed ']:
        if i != 0:
            VSpeed.append((int(i,16))*0.01)
        else:
            VSpeed.append(0)

    dataset.drop('Vehicle Speed ',axis=1)
    dataset['Vehicle Speed '] = (VSpeed)
    
    ###################################################################
    #Inj Q Cur (mg-st)
    InjCur = []

    for i in dataset['Inj Q Cur (mg-st)']:
        if i != 0:
            InjCur.append((int(i,16))*0.02)
        else:
            InjCur.append(0)

    dataset.drop('Inj Q Cur (mg-st)',axis=1)
    dataset['Inj Q Cur (mg-st)'] = (InjCur)
    
    ###################################################################
    #Inj Q Tor (mg-st)
    InjTor = []

    for i in dataset['Inj Q Tor (mg-st)']:
        if i != 0:
            InjTor.append((int(i,16))*0.02)
        else:
            InjTor.append(0)      

    dataset.drop('Inj Q Tor (mg-st)',axis=1)
    dataset['Inj Q Tor (mg-st)'] = (InjTor)

    ###################################################################
    #Boost Pressure
    BPressure = []

    for i in dataset['Boost Pressure (mBar)']:
        if i != 0:
            BPressure.append((int(i,16))*1.00)
        else:
            BPressure.append(0)

    dataset.drop('Boost Pressure (mBar)',axis=1)
    dataset['Boost Pressure (mBar)'] = (BPressure)

    ###################################################################
    #Atmospheric Pressure
    AtmPressure = []

    for i in dataset['Atmospheric Pressure (mBar)']:
        if i != 0:
            AtmPressure.append((int(i,16))*1.00)
        else:
            AtmPressure.append(0)    

    dataset.drop('Atmospheric Pressure (mBar)',axis=1)
    dataset['Atmospheric Pressure (mBar)'] = (AtmPressure)

    ###################################################################
    #Coolant Temperature
    CTemp = []

    for i in dataset['Coolant Temperature (*C)']:
        if i != 0:
            CTemp.append(((int(i,16))*0.10)+(-273))
        else:
            CTemp.append(0)

    dataset.drop('Coolant Temperature (*C)',axis=1)
    dataset['Coolant Temperature (*C)'] = (CTemp)

    ###################################################################
    # Oil Temperature
    OTemp = []

    for i in dataset['Oil Temperature (*C)']:
        if i != 0:
            OTemp.append(((int(i,16))*0.10)+(-273))
        else:
            OTemp.append(0)

    dataset.drop('Oil Temperature (*C)',axis=1)
    dataset['Oil Temperature (*C)'] = (OTemp)

    ###################################################################
    #Boost Temperature
    BoostTemp = []

    for i in dataset['Boost Temperature (*C)']:
        if i != 0:
            BoostTemp.append(((int(i,16))*0.10)+(-273))
        else:
            BoostTemp.append(0)

    dataset.drop('Boost Temperature (*C)',axis=1)
    dataset['Boost Temperature (*C)'] = (BoostTemp)

    ###################################################################
    #Oil Pressure
    OilPressure = []

    for i in dataset['Oil Pressure (mBar)']:
        if 1 !=0:
            OilPressure.append(((int(i,16))*1.00)+(0))
        else:
            OilPressure.append(0)

    dataset.drop('Oil Pressure (mBar)',axis=1)
    dataset['Oil Pressure (mBar)'] = (OilPressure)

    ###################################################################
    #Battery Voltage
    BVoltage = []

    for i in dataset['Battery Voltage (V)']:
        if i != 0:
            BVoltage.append(((int(i,16))*0.02)+(0))
        else:
            BVoltage.append(0)

    dataset.drop('Battery Voltage (V)',axis=1)
    dataset['Battery Voltage (V)'] = (BVoltage)

    ###################################################################
    # Cam Speed
    CamSpeed = []

    for i in dataset['Cam Speed (rpm)']:
        if i != 0:
            CamSpeed.append(((int(i,16))*0.50)+(0))
        else:
            CamSpeed.append(0)

    dataset.drop('Cam Speed (rpm)',axis=1)
    dataset['Cam Speed (rpm)'] = (CamSpeed)

    ###################################################################
    # Rail Pressure
    RailPressure = []

    for i in dataset['Rail Pressure (mBar)']:
        if i != 0:
            RailPressure.append(((int(i,16))*100)+(0))
        else:
            RailPressure.append(0)

    dataset.drop('Rail Pressure (mBar)',axis=1)
    dataset['Rail Pressure (mBar)'] = (RailPressure)

    ###################################################################
    #Rail Pressure Set
    RailPressureSet = []

    for i in dataset['Rail Pressure set (mBar)']:
        if i != 0:
            RailPressureSet.append(((int(i,16))*100)+(0))
        else:
            RailPressure.append(0)

    dataset.drop('Rail Pressure set (mBar)',axis=1)
    dataset['Rail Pressure set (mBar)'] = (RailPressureSet)


    ###################################################################
    #MU Vol %
    MUPWM = []

    for i in dataset['MU PWM (%)']:
        if i != 0:
            MUPWM.append(((int(i,16))*0.01)+(0))
        else:
            MUPWM.append(0)

    dataset.drop('MU PWM (%)',axis=1)
    dataset['MU PWM (%)'] = (MUPWM)

    ###################################################################
    #MU Vol (mm3-s)
    MUVol = []

    for i in dataset['MU Vol (mm3-s)']:
        if i != 0:
            MUVol.append(((int(i,16))*10)+(0))
        else:
            MUVol.append(0)

    dataset.drop('MU Vol (mm3-s)',axis=1)
    dataset['MU Vol (mm3-s)'] = (MUVol)

    ###################################################################
    #Torque Rat
    TorqueRat = []

    for i in dataset['Torque Rat']:
        if i != 0:
            TorqueRat.append(((int(i,16))*0.01)+(0))
        else:
            TorqueRat.append(0)

    dataset.drop('Torque Rat',axis=1)
    dataset['Torque Rat'] = (TorqueRat)

    ###################################################################
    #Torque
    Torque = []

    for i in dataset['Torque (Nm)']:
        if i != 0:
            Torque.append(((int(i,16))*0.10)+(0))
        else:
            Torque.append(0)

    dataset.drop('Torque (Nm)',axis=1)
    dataset['Torque (Nm)'] = (Torque)

    ###################################################################
    #TQ Limit Set
    TQLimit = []

    for i in dataset['TQ Limit Set']:
        if i != 0:
            TQLimit.append(((int(i,16))*0.10)+(0))
        else:
            TQLimit.append(0)

    dataset.drop('TQ Limit Set',axis=1)
    dataset['TQ Limit Set'] = (TQLimit)

    ###################################################################
    #Main Injection (mg-st)
    MInjection = []

    for i in dataset['Main Injection (mg-st)']:
        if i != 0:
            MInjection.append(((int(i,16))*0.02)+(0))
        else:
            MInjection.append(0)

    dataset.drop('Main Injection (mg-st)',axis=1)
    dataset['Main Injection (mg-st)'] = (MInjection)

    ###################################################################
    #Pilot Injection (mg-st)
    
    PInjection = []

    for i in dataset['Pilot Injection (mg-st)']:
        iorf = isinstance(i, float)

        if iorf:
            i = int(i)
            i = str(i)

        if i != 0:
            PInjection.append((int(i,16)*0.02)+(0))
        else:
            PInjection.append(0)

    dataset.drop('Pilot Injection (mg-st)',axis=1)
    dataset['Pilot Injection (mg-st)'] = (PInjection)

    ###################################################################
    #EGR Prop (%)
    EGRProp = []

    for i in dataset['EGR Prop (%)']:
        if i != 0:
            EGRProp.append(((int(i,16))*0.01)+(0))
        else:
            EGRProp.append(0)

    dataset.drop('EGR Prop (%)',axis=1)
    dataset['EGR Prop (%)'] = (EGRProp)

    ###################################################################
    #EGR Pos D (%)
    EGRPosD = []

    for i in dataset['EGR Pos D (%)']:
        if i != 0:
            EGRPosD.append(((int(i,16))*0.01)+(0))
        else:
            EGRPosD.append(0)

    dataset.drop('EGR Pos D (%)',axis=1)
    dataset['EGR Pos D (%)'] = (EGRPosD)

    ###################################################################
    #EGR Pos A (%)
    EGRPosA = []

    for i in dataset['EGR Pos A (%)']:
        if i != 0:
            EGRPosA.append(((int(i,16))*0.01)+(0))
        else:
            EGRPosA.append(0)
            
    dataset.drop('EGR Pos A (%)',axis=1)
    dataset['EGR Pos A (%)'] = (EGRPosA)

    ###################################################################
    #Engine Grad (rpm)
    EngineGrad = []

    for i in dataset['Engine Grad (rpm)']:
        if i != 0:
            EngineGrad.append(((int(i,16))*0.50)+(0))
        else:
            EngineGrad.append(0)

    dataset.drop('Engine Grad (rpm)',axis=1)
    dataset['Engine Grad (rpm)'] = (EngineGrad)

    ###################################################################
    

    return dataset