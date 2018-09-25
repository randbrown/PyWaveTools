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

    freq = wavelib.glissando_lin(times, wavelib.FREQ_A4, wavelib.FREQ_A3)
    vals = wavelib.shepardtone(times, freq, tritone_sine, wavelib.FREQ_A3, 1, 1)
    vals = wavelib.normalize(vals)
    vals = wavelib.play_n(vals, 5)
    wavelib.write_wave_file('output/shepard_tritone_down_5x.wav', vals)

    freq = wavelib.glissando_lin(times, wavelib.FREQ_A3, wavelib.FREQ_A4)
    vals = wavelib.shepardtone(times, freq, tritone_sine, wavelib.FREQ_A3, 1, 1)
    vals = wavelib.normalize(vals)
    vals = wavelib.play_n(vals, 5)
    wavelib.write_wave_file('output/shepard_tritone_up_5x.wav', vals)

    # create a crescendo, fading in from 0 to full volume at the very end
    vals = wavelib.fade(vals)
    wavelib.write_wave_file('output/shepard_tritone_up_5x_crescendo.wav', vals)


main()
