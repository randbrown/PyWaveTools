""" Generate falling triad sawtooth wave """
import wavelib
import numpy as np

SAMPLE_RATE = 44100.0   # hertz
DURATION = 5.0          # seconds
FREQUENCY = 440.0       # hertz
FREQUENCY_RATE = -10.0   # fall at 10 hz per second

def main():
    """main function"""
    # x is array of values at each time slot of the whole wav file
    times1 = wavelib.createtimes(0.1, SAMPLE_RATE)
    times2 = wavelib.createtimes(0.9, SAMPLE_RATE)
    # constant frequency
    freq = FREQUENCY
    vals1 = wavelib.square(times1, freq)
    vals2 = wavelib.zero(times2)
    vals1 = wavelib.normalize(vals1)
    vals = np.concatenate((vals1, vals2))
    vals = wavelib.play_n(vals, 10)
    #wavelib.write_wave_file('output/alt_dry.wav', vals)
    # vals = wavelib.fx_reverb(vals)
    # vals = wavelib.normalize(vals)
    # wavelib.write_wave_file('output/alt_reverb.wav', vals)
    # print vals
    # vals = wavelib.comb_filter(vals)
    print vals
    vals = wavelib.normalize(vals)
    wavelib.write_wave_file('output/alt_comb.wav', vals)

main()
