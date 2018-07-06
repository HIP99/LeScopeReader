from ROOT import gROOT, TFile, TGraph
from itertools import izip_longest, imap
from struct import unpack, calcsize
from scipy.signal import butter, lfilter, freqz, iirfilter, iirdesign
import numpy as np
import matplotlib.pyplot as plt
import time

import sys

inputFileName = str(sys.argv[1])
outputFileName = inputFileName + ".root"
print "Input file : ", inputFileName
print "Output file : ", outputFileName

params_pattern = '=IBdddd' # (num_samples, sample_bytes, v_off, v_scale, h_off, h_scale, [samples]) ...
struct_size = calcsize(params_pattern)
print "Struct size : ", str(struct_size)

file = TFile(outputFileName, "recreate")

with open(inputFileName,"rb") as f:
    areaList = []
    totVolt = np.zeros(10002)
    totFiltVolt = np.zeros(10002)
    totFreq = np.zeros(1251)
    totFft = np.zeros(1251,dtype=np.complex_)
    countThings = 0

#    notchb,notcha = simple_notch([340000,360000],2499999.97078,7)
#    notch2b,notch2a = simple_notch([820000,850000],2499999.97078,7)
#    notch3b,notch3a = simple_notch([1000000,1200000],2499999.97078,7)
    
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
#        print v_off
#        print numSamples

        dataList=np.fromfile(f,dt,numSamples)
        sampList=np.arange(numSamples)
        voltList=np.multiply(dataList,v_scale)
        voltList=voltList-v_off
#        totVolt+=voltList
        countThings+=1
        timeList=np.multiply(sampList,h_scale)        
        timeList=timeList-h_off
        graphName = "graph" + str(countThings)
#        print graphName
        graph = TGraph(numSamples, timeList, voltList)
        graph.Write(graphName)


print "Total number of waveforms processed : ", countThings
#        print voltList
#        print timeList

        # Filter requirements.
#        order = 6
#        fs = 1./h_scale       # sample rate, Hz
#        cutoff = 600000  # desired cutoff frequency of the filter, Hz


#        voltList = butter_lowpass_filter(voltList, cutoff, fs, order)
#        filtvoltList = lfilter(notchb,notcha,voltList)
#        filtvoltList = lfilter(notch2b,notch2a,filtvoltList)
#        filtvoltList = lfilter(notch3b,notch3a,filtvoltList)
#        totFiltVolt+=filtvoltList
#        n = len(voltList) # length of the signal
#        k = np.arange(n)
#        T = n*h_scale
#        frq = k/T # two sides frequency range
#        frq = frq[range(n/2)] # one side frequency range
#        print n,T,h_scale,len(frq)

        
#        Y = np.fft.fft(filtvoltList)/n # fft computing and normalization
#        Y = Y[range(n/2)]

#        totFft+=Y;
#        totFreq+=frq;
        
#        fig, ax = plt.subplots(2, 1)
#        ax[0].plot(timeList,voltList,"b",timeList,filtvoltList,"r")
#        ax[0].set_xlabel('Time')
#        ax[0].set_ylabel('Amplitude')
#        ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
#        ax[1].set_xlabel('Freq (Hz)')
#        ax[1].set_ylabel('|Y(freq)|')
#        plt.pause(1)

 #   totFreq/=countThings
 #   totFft/=countThings
 #   totVolt/=countThings
 #   totFiltVolt/=countThings

 #   fig, ax = plt.subplots(3, 1)
 #   ax[0].plot(timeList,totVolt,"b",timeList,totFiltVolt,"r")
 #   ax[0].set_xlabel('Time')
 #   ax[0].set_ylabel('Amplitude')

 #   Y2 = np.fft.fft(voltList)/n # fft computing and normalization
 #   Y2 = Y[range(n/2)]

 #   ax[1].plot(totFreq,abs(Y2),'r') # plotting the spectrum
 #   ax[1].set_xlabel('Freq (Hz)')
 #   ax[1].set_ylabel('|Y(freq)|')

    
 #   ax[2].plot(totFreq,abs(totFft),'r') # plotting the spectrum
 #   ax[2].set_xlabel('Freq (Hz)')
 #   ax[2].set_ylabel('|Y(freq)|')



    
 #   plt.show()
        
