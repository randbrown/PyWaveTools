""" Generate shepard tone """
import math
import wavelib
import numpy as np

#START_FREQ = 440/4.0
START_FREQ = 440/8.0
STEPS = 12.0
DURATION_PER_STEP = 1.0            # seconds
TOTAL_DURATION = DURATION_PER_STEP * STEPS

def shepardtone(times, freq, falling=False, num_octaves=5):
    """generates a shepard tone using frequency multiples of the given frequency"""
    # assign whatever waveform type we want here
    #waveform_generator = wavelib.sawtooth
    waveform_generator = wavelib.sinewave

    vals = np.zeros(times.shape)

    # theoretically, it should probably be exponential scaling of intensity, 
    # to fade one voice out while fading the other in.
    # however, since they're in different octaves and such, i've been playing
    # with alternative scalings
    #ints_scale = exp_scale_x(times, 0.0, 1.0)
    #ints_scale = linear_scale_x(times, 0.0, 1.0)
    ints_scale = wavelib.square_scale_x(times, 0.0, 1.0)
    ints_scale_rev = ints_scale[::-1]

    for i in range(0, num_octaves):
        freqi = freq * 2.0**i
        #print 'i', i, freqi
        valsi = waveform_generator(times, freqi)
        if i == 0:
            intsi = ints_scale
            if(falling):
                intsi = ints_scale_rev
            
            valsi = valsi * intsi
            #print 'intsi', i, intsi
        if i == num_octaves-1:
            intsi = ints_scale_rev
            if(falling):
                intsi = ints_scale
            valsi = valsi * intsi
            #print 'intsi', i, intsi

        #wavelib.write_wave_file('output/shepard_' + str(i) + '.wav', valsi)
        vals += valsi

    return vals

def main():
    """main function"""

    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(TOTAL_DURATION)
    #print 'times', times

    #freq = START_FREQ * (2.0 ** ((times//1.0)/STEPS)) # floor to even steps
    freq = START_FREQ * (2.0 ** ((times)/(STEPS-1)/2.0))     # continuous glissando
    falling = False

    # falling tones
    #freq = START_FREQ * (2.0 ** (-1* ((times//1.0)/STEPS))) # floor to even steps
    # freq = START_FREQ * (2.0 ** (-1*(times)/(STEPS+1)/2.0))     # continuous glissando
    # falling = True

    #print 'freq', freq

    vals_list = np.arange(0, 0)
    vals_list = wavelib.normalize(shepardtone(times, freq, falling, 5))

    # and lets run through it twice, so cat the list together with itself
    vals_list = np.concatenate((vals_list, vals_list), axis=0) 
    wavelib.write_wave_file('output/shepard_steps2x.wav', vals_list)

main()
