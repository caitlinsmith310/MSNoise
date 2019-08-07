from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import os
from datetime import date, timedelta

directory ='/home/csmi310/msnoise/data/'
os.chdir(directory) 

client = Client('GEONET')


today=UTCDateTime(date.today())
days=timedelta(days=1)

for d in range(-9,-8):
    start=UTCDateTime(today+d*days)
    end=start+24*60*60
    year=start.strftime('%Y')
    print('Getting data for:',start)
    st = client.get_waveforms(network='NZ', station='??AZ', location='*',channel='EHZ',  starttime=start, endtime=end, attach_response=True)

    pre_filt = (0.01, 0.05, 30.0, 35.0)
    st.remove_response(output='VEL', pre_filt=pre_filt, water_level=60)

    
    st.merge(fill_value=0)
    st.sort()
    
    for tr in st.select(station='ARAZ'):
        st.remove(tr)
    for tr in st:
        tr.write(year+'/'+tr.stats.station+'/'+tr.stats.channel+'.D/'+tr.id + ".D.%d.%d" %(start.year,start.julday), format="MSEED")
    print('Data written for',start)
