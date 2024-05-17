import os
import sys
import time
import string
import struct
import socket
import numpy
import config
import pickle
import numpy as np  
from lecroy import LeCroyScope
from lecroy import LeCroyWaveformChannel

# sys.path.insert(0, '/home/hpumphrey/pySineNoise')
# from PyPurityTools import PyPurityTools as ppt

# def getAmp(arr):
#     amp = 0
#     for i in range(len(arr)):
#         amp+=max(np.max(arr[i]),abs(np.min(arr[i])))
#     return amp/len(arr)

def fetch(filename, nevents, nsequence, trigchannel, triglevel, voltdiv):
    '''
    Fetch and save waveform traces from the oscilloscope.
    '''
    scope = LeCroyScope(config.ip, timeout=config.timeout)
    scope.clear()
    scope.set_sequence_mode(nsequence)
    channels = scope.get_channels()
    print(channels)
    settings = scope.get_settings()
    print(settings)

    # print trigchannel, triglevel, voltdiv
    commands = {}
    
    if (trigchannel != 999 ):
        commands['TRIG_SELECT'] = 'TRSE EDGE,SR,C'+str(trigchannel)+',HT,OFF'

    if (triglevel != 999 ):
        commands['C2:TRIG_LEVEL'] = 'C2:TRLV '+str(triglevel)+' V'
        commands['C3:TRIG_LEVEL'] = 'C3:TRLV '+str(triglevel)+' V'
        commands['C4:TRIG_LEVEL'] = 'C4:TRLV '+str(triglevel)+' V'

    if (voltdiv != 999 ):
        commands['C2:VOLT_DIV'] = 'C2:VDIV '+str(voltdiv)+' V'
        commands['C3:VOLT_DIV'] = 'C3:VDIV '+str(voltdiv)+' V'
        commands['C4:VOLT_DIV'] = 'C4:VDIV '+str(voltdiv)+' V'

    scope.set_settings(commands)
    
    # print(commands)

    newsettings = scope.get_settings()
    #print(newsettings)


    if 'ON' in settings['SEQUENCE']:
        sequence_count = int(settings['SEQUENCE'].split(',')[1])
        # sequence_count=100
        # print("ON")
    else:
        sequence_count = 1
        # print("other")
        
    if nsequence != sequence_count:
        print('Could not configure sequence mode properly')
    if sequence_count != 1:
        print('Using sequence mode with %i traces per aquisition' % sequence_count)
    
    f = {}
    timef = {} # output file with trigger times
    Values = []
    for channel in channels:
        f[channel] = open('%s.ch%s.traces'%(filename,channel),'wb')
        timef[channel] = open('%s.ch%s.traces.times'%(filename,channel),'wb')
    params_pattern = '=IBdddd' # (num_samples, sample_bytes, v_off, v_scale, h_off, h_scale, [samples]) ...
    try:
        i = 0
        #print '\rnumber of events: %i' %nevents
        while i < nevents:
            #print '\rfetching event: %i' % i, 
            sys.stdout.flush()
            try:
                scope.trigger()
                # print channels
                for channel in channels:
                    # print('\nCurrently working through channel: %d' %channel)
                    wave_desc,wave_array,trig_time_array,trigger_time,acq_duration = scope.get_waveform(channel)
                    num_samples = wave_desc['wave_array_count']//sequence_count
                    # print(num_samples)
                    
                    
                    traces = wave_array.reshape(sequence_count, wave_array.size//sequence_count)
                    
                    
                    out = f[channel]
                    outtime = timef[channel]
                    # print num_samples,sequence_count
                    # print trigger_time
                    # print acq_duration
                    
                    
                    outtime.write(str(trigger_time)+' ')
                    outtime.write(str(acq_duration)+'\n')
                    
                    
                    #New way of writing files
                    # waveform=LeCroyWaveformChannel(wave_desc,wave_array,trig_time_array)
                    # waveform.to_file(out)
                    # waveform.from_file(out)
                                        
                    for n in xrange(0,sequence_count):
                        # print "Here",n                    
                        tempsturct=struct.pack(params_pattern,num_samples,wave_desc['dtype'].itemsize,wave_desc['vertical_offset'], wave_desc['vertical_gain'], -wave_desc['horiz_offset'], wave_desc['horiz_interval'])
                        # print traces[n]
                        out.write(tempsturct)
                        traces[n].tofile(out)

                    
            except (socket.error) as e:
                #print '\n' + str(e)
                print(("Socket Error"))
                scope.clear()
                continue
            i += sequence_count
    except KeyboardInterrupt:
        print('\rUser interrupted fetch early') 
    except Exception as e:
        print ("\rUnexpected error:", e)
    finally:
        print ('\r',) 
        for channel in channels:
            print("Closing",channel)
            f[channel].close()
            timef[channel].close()
        scope.clear()
        return i

if __name__ == '__main__':
    #frequencyarr = np.linspace(200,1200,21, dtype=int)
    #[200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1050, 1100, 1150, 1200] 
    # #np.linspace(250,1200, num=20, dtype=int) 
    # levelarr = [10,20,30,40,50,60,70,80,90,100,250,500]
    #levelarr = np.concatenate((np.linspace(5,50,10, dtype=int), np.linspace(100,500,9, dtype=int)))
    #[25, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500] 
    #np.linspace(25,500, num=20, dtype=int)
    captureNumber = 100
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", type=int, dest="nevents",
                        help="number of events to capture in total", default=100)
    parser.add_argument("-s", type=int, dest="nsequence",
                        help="number of sequential events to capture at a time", default=1)
    parser.add_argument("-f", type=int, dest="frequency", 
                        help="The generated radio frequency for file naming convention")
    parser.add_argument("-l", type=int, dest="level", 
                        help="The generated radio signals original energy level for file naming convention")
    parser.add_argument("--temp", action="store_true", dest="temp",
                        help="this is the input for a temporary file that will be saved as toremove in base directory", default=False)

    parser.add_argument("--time", action="store_true", dest="time",
                        help="append time string to filename", default=False)
    parser.add_argument("-c", action="store", type=int, dest="trigchannel",
                        help="Channel to trigger on", default=999)
    parser.add_argument("-t", action="store", type=float, dest="triglevel",
                        help="Trigger level in volts", default=999)
    parser.add_argument("-d", action="store", type=float, dest="voltdiv",
                        help="Divisions in volts", default=999)

    args = parser.parse_args()

    if args.nevents < 1 or args.nsequence < 1:
        sys.exit("Arguments to -s or -n must be positive")
    
    if args.temp == False:
        #try:
         #   frequencyarr.index(args.frequency)
          #  levelarr.index(args.level)
        #except(ValueError):
         #   sys.exit("This is not a valid input frequency or level")
            
        filename2 = '/unix/anita4/hugo/LecroyData/FPGAComp/' + str(args.level) + '_' + str(args.frequency)
        filename = filename2 + '_' + string.replace(time.asctime(time.localtime()), ' ', '-') if args.time else filename2
        
    elif args.temp == True:
        filename = '/unix/anita4/hugo/toremove' + '_' + string.replace(time.asctime(time.localtime()), ' ', '-') if args.time else '/unix/anita4/hugo/toremove'

    print('Saving to file %s' % filename)

    start = time.time()
    count = fetch(filename, args.nevents, args.nsequence, args.trigchannel, args.triglevel, args.voltdiv)
    elapsed = time.time() - start
    if count > 0:
        print('Completed %i events in %.3f seconds.' % (count, elapsed))
        print('Averaged %.5f seconds per acquisition.' % (elapsed/count))
