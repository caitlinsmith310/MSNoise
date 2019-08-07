from obspy import UTCDateTime
from obspy.clients.fdsn import Client
import os

directory ='/home/csmi310/msnoise/data/'
os.chdir(directory) 

client = Client('GEONET')

Start=300
Final=366
for i in range (Start,Final):
    start = UTCDateTime(year=2017, julday=i)
    end= start+(24*60*60)
    year=start.strftime('%Y')
    Progress=i/(Final-Start)
    print('Working on day',start.julday)
    print(Progress,"%")
    
    st = client.get_waveforms(network='NZ', station='??AZ', location='*',
                               channel='HHZ,EHZ', starttime=start, endtime=end,
                               attach_response=True)
    
    pre_filt = (0.01, 0.05, 30.0, 35.0)
    st.remove_response(output='VEL', pre_filt=pre_filt, water_level=60)
    print('Remove response complete for',start)

    
    st.merge(fill_value=0)
    st.sort()
    
    for tr in st.select(station='ARAZ'):
        st.remove(tr)
    for tr in st:
        tr.write(year+'/'+tr.stats.station+'/'+tr.stats.channel+'.D/'+tr.id + ".D.%d.%d" %(start.year,start.julday), format="MSEED")
    print('Data written for',start)
