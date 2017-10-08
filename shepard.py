""" Generate shepard tone """
import math
import wavelib
import numpy as np

FREQ_A1 = 55.0
STEPS = 12.0
DURATION_PER_STEP = 1.0            # seconds
TOTAL_DURATION = DURATION_PER_STEP * STEPS

def shepard_glissando(times, freq_start, freq_end, octaves=5):
    falling = freq_end < freq_start
    freq = wavelib.glissando(times, freq_start, freq_end)
    vals = wavelib.shepardtone(times, freq, falling, octaves)
    return vals

def shepard_discrete(times, freq_start, freq_end, octaves=5):
    falling = freq_end < freq_start
    freq = wavelib.discrete(times, freq_start, freq_end, STEPS)
    vals = wavelib.shepardtone(times, freq, falling, octaves)
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
