""" Generate shepard tone """
import math
import wavelib
import numpy as np

START_FREQ = 440/2.0
STEPS = 12.0
DURATION_PER_STEP = 1.0            # seconds
TOTAL_DURATION = DURATION_PER_STEP * STEPS

def linear_scale(x, minx, maxx, miny, maxy):
    return ((x - minx) / (maxx - minx)) * (maxy - miny) + miny

def linear_scale_x(x, miny, maxy):
    return ((x - x.min()) / (x.max() - x.min())) * (maxy - miny) + miny

def shepardtone(times, freq, reverse=False, num_octaves=5):
    """generates a shepard tone using frequency multiples of the given frequency"""
    # assign whatever waveform type we want here
    #waveform_generator = wavelib.sawtooth
    waveform_generator = wavelib.sinewave

    vals = np.zeros(times.shape)

    for i in range(0, num_octaves):
        freqi = freq * 2.0**i
        #print 'i', i, freqi
        valsi = waveform_generator(times, freqi)
        if i == 0:
            intsi = linear_scale_x(times, 0.0, 1.0)
            if(reverse):
                intsi = 1.0 - intsi
            valsi = valsi * intsi
            #print 'intsi', i, intsi
        if i == num_octaves-1:
            intsi = 1 - linear_scale_x(times, 0.0, 1.0)
            if(reverse):
                intsi = 1.0 - intsi
            valsi = valsi * intsi
            #print 'intsi', i, intsi

        wavelib.write_wave_file('output/shepard_' + str(i) + '.wav', valsi)

        vals += valsi

    return vals

def main():
    """main function"""

    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(TOTAL_DURATION)

    print 'times', times
    print 'times//1.0/STEPS', times//1.0/STEPS
    print 'times/STEPS', times/STEPS
    print 'times/STEPS/2.0', times/STEPS/2.0
    #freq = START_FREQ * (2.0 ** ((times//1.0)/STEPS)) # floor to even steps
    #freq = START_FREQ * (2.0 ** ((times)/STEPS/2.0))     # continuous glissando
    #freq = START_FREQ * (2.0 ** ((times)/STEPS/1.0))     # continuous glissando

    freq = START_FREQ * (2.0 ** (-1* ((times//1.0)/STEPS))) # floor to even steps

    wavelib.write_wave_file('output/sine.wav', wavelib.normalize(wavelib.sinewave(times, freq)))
    wavelib.write_wave_file('output/saw.wav', wavelib.normalize(wavelib.sawtooth(times, freq)))

    vals_list = np.arange(0, 0)
    vals_list = wavelib.normalize(shepardtone(times, freq, True, 5))

    # and lets run through it twice, so cat the list together with itself
    vals_list = np.concatenate((vals_list, vals_list), axis=0) 
    wavelib.write_wave_file('output/shepard_steps2x.wav', vals_list)

main()
