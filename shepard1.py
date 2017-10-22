""" Generate shepard tone """
import math
import wavelib
import numpy as np
import plotlib

FREQ_A1 = 55.0
STEPS = 12.0
DURATION_PER_STEP = 1.0            # seconds
TOTAL_DURATION = DURATION_PER_STEP * STEPS

def shepard(times, freq):
    vals = wavelib.shepardtone1(times, freq, wavelib.sinewave, wavelib.FREQ_A4, 0, 0)
    return vals

def main():
    """main function"""

    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(TOTAL_DURATION)

    freq = wavelib.discrete(times, wavelib.FREQ_A5, wavelib.FREQ_A4, 12)
    vals = wavelib.normalize(wavelib.shepardtone1(times, freq))
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard1_discrete.wav', vals)
    
    # #plotlib.plot_wave_and_fft(times, vals)
    # wavelib.write_wave_file('output/shepard1_discrete.wav', vals)
    # wavelib.write_wave_file('output/test_sine_const880.wav', wavelib.normalize(wavelib.sinewave(times, 880)))
    # wavelib.write_wave_file('output/test_sine_const440.wav', wavelib.normalize(wavelib.sinewave(times, 440)))

    freq = wavelib.glissando(times, wavelib.FREQ_A5, wavelib.FREQ_A4)
    vals = wavelib.normalize(wavelib.shepardtone1(times, freq))
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard1_glissando.wav', vals)

main()
