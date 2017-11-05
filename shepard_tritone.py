""" Generate shepard tone """
import math
import wavelib
import numpy as np

STEPS = 12.0
DURATION_PER_STEP = 1.0            # seconds
TOTAL_DURATION = DURATION_PER_STEP * STEPS

def tritone_sine(times, freq):
    vals1 = wavelib.sinewave(times, freq)
    vals2 = wavelib.sinewave(times, freq* wavelib.DIMINISHED_FIFTH)
    vals = vals1 + vals2
    return vals

def main():
    """main function"""

    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(TOTAL_DURATION)
    
    freq = wavelib.glissando_lin(times, wavelib.FREQ_A5, wavelib.FREQ_A4)
    vals = wavelib.shepardtone(times, freq, tritone_sine)
    vals = wavelib.normalize(vals)
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_tritone_down_2x.wav', vals)

    freq = wavelib.glissando_lin(times, wavelib.FREQ_A4, wavelib.FREQ_A5)
    vals = wavelib.shepardtone(times, freq, tritone_sine)
    vals = wavelib.normalize(vals)
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_tritone_up_2x.wav', vals)

main()
