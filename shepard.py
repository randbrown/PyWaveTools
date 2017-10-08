""" Generate shepard tone """
import math
import wavelib
import numpy as np

FREQ_A1 = 55.0
STEPS = 12.0
DURATION_PER_STEP = 1.0            # seconds
TOTAL_DURATION = DURATION_PER_STEP * STEPS

def shepardtone(times, freq, falling=False, num_octaves=5, waveform_generator = wavelib.sinewave):
    """generates a shepard tone using octaves of the given frequency"""

    vals = np.zeros(times.shape)

    # theoretically, it should probably be exponential scaling of intensity, 
    # to fade one voice out while fading the other in.
    # however, since they're in different octaves and such, i've been playing
    # with alternative scalings
    #ints_scale = wavelib.exp_scale_x(times, 0.0, 1.0)
    ints_scale = wavelib.linear_scale_x(times, 0.0, 1.0)
    #ints_scale = wavelib.square_scale_x(times, 0.0, 1.0)
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

def shepard_glissando(times, freq_start, freq_end, octaves=5):
    falling = freq_end < freq_start
    freq = freq_start
    if falling:
        freq = freq_start * (2.0 ** (-1*(times)/(STEPS+1)/2.0))     # continuous glissando
    else:
        freq = freq_start * (2.0 ** ((times)/(STEPS-1)/2.0))     # continuous glissando
    vals = shepardtone(times, freq, falling, octaves)
    return vals

def shepard_discrete(times, freq_start, freq_end, octaves=5):
    falling = freq_end < freq_start
    freq = freq_start
    if falling:
        freq = freq_start * (2.0 ** (-1* ((times//1.0)/STEPS))) # floor to even steps
    else:
        freq = freq_start * (2.0 ** ((times//1.0)/STEPS)) # floor to even steps
    vals = shepardtone(times, freq, falling, octaves)
    return vals

def play_twice(vals):
    return np.concatenate((vals, vals), axis=0) 

def main():
    """main function"""

    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(TOTAL_DURATION)

    vals = wavelib.normalize(shepard_glissando(times, FREQ_A1*2, FREQ_A1, 5))
    vals = play_twice(vals)
    wavelib.write_wave_file('output/shepard_glissando_down_2x.wav', vals)

    vals = wavelib.normalize(shepard_discrete(times, FREQ_A1*2, FREQ_A1, 5))
    vals = play_twice(vals)
    wavelib.write_wave_file('output/shepard_discrete_down_2x.wav', vals)

    vals = wavelib.normalize(shepard_glissando(times, FREQ_A1, FREQ_A1*2, 5))
    vals = play_twice(vals)
    wavelib.write_wave_file('output/shepard_glissando_up_2x.wav', vals)

    vals = wavelib.normalize(shepard_discrete(times, FREQ_A1, FREQ_A1*2, 5))
    vals = play_twice(vals)
    wavelib.write_wave_file('output/shepard_discrete_up_2x.wav', vals)

main()
