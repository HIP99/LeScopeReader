from itertools import izip_longest, imap
from struct import unpack, calcsize
import numpy as np
import matplotlib.pyplot as plt
import time

params_pattern = '=IBdddd' # (num_samples, sample_bytes, v_off, v_scale, h_off, h_scale, [samples]) ...
struct_size = calcsize(params_pattern)
print struct_size

#with open("/unix/creamtea/scopeStuff/test2.ch3.traces","rb") as f:
with open("/unix/creamtea/scopeStuff/test950V_5V_5ns.ch3.traces","rb") as f:
    areaList = []
    while True:
        header = f.read(struct_size)
        if not header: break
        sHeader = unpack(params_pattern,header)
        numSamples=sHeader[0]
        bytesPerSample=sHeader[1]
        v_off=sHeader[2]
        v_scale=sHeader[3]
        h_off=sHeader[4]
        h_scale=sHeader[5]
        dt=np.dtype('>i1')
        dataList=np.fromfile(f,dt,numSamples)
        sampList=np.arange(numSamples)
        voltList=np.multiply(dataList,v_scale)
        timeList=np.multiply(sampList,h_scale)        
        timeList+=h_off
        area=np.trapz(voltList,timeList)
        areaList.append(area)

#    print areaList
    areaMean=np.mean(areaList)
    areaStd=np.std(areaList)
    print areaMean,areaStd
    print (areaMean/areaStd)*(areaMean/areaStd)

    # the histogram of the data
    n, bins, patches = plt.hist(areaList, 50, normed=0, facecolor='g', alpha=0.75)

    plt.xlabel('Area Under Waveform')
    plt.ylabel('Events')
    plt.title('Histogram of Charge')
    plt.grid(True)
    plt.show()



        
