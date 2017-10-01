""" Generate shepard tone """
import numpy as np
import wavelib

SAMPLE_RATE = 44100.0       # hertz
DURATION = 10.0             # seconds
FREQUENCY = 440.0           # hertz
# FREQUENCY_RATE = -100.0     # fall at N hz per second
FREQUENCY_DELTA = 440.0     # rise/fall N hz total
MAX_AMP = 32767.0
NUM_OSC = 3

def shepardtone(times, freq_a, num_osc):
    """generates a shepard tone using frequency multiples of the given frequency"""
    freq = FREQUENCY + freq_a % FREQUENCY
    #freq = freq_a
    print freq_a
    print freq
    #target_freq = FREQUENCY*2
    target_freq = FREQUENCY
    # gets quieter as we go away from midpoint
    #### TODO: use log scale instead of linear
    amp = (-1/target_freq) * np.abs(target_freq-freq) + 1    # each one gets quieter as we go away from midpoint
    vals = wavelib.sinewave(times, freq) * amp
    #vals = wavelib.zero(times)
    wavelib.write_wave_file('output/sine1.wav', vals)

    # higher voices
    for j in range(2, num_osc):
        #freqj = freq * 2.0**j
        freqj = freq * float(j)
        # gets quieter as we go away from midpoint
        #### TODO: use log scale instead of linear
        amp = (-1/target_freq) * np.abs(target_freq-freqj) + 1
        #print '%s upper amp: %s' % (j, amp)
        valsj = wavelib.sinewave(times, freqj) * amp
        vals = vals + valsj

    #lower voices
    for j in range(2, num_osc):
        #freqj = freq * 2.0**(-j)
        freqj = freq / float(j)
        # gets quieter as we go away from midpoint
        #### TODO: use log scale instead of linear
        amp = (-1/target_freq) * np.abs(target_freq-freqj) + 1
        #print '%s lower amp: %s' % (j, amp)
        valsj = wavelib.sinewave(times, freqj) * amp
        vals = vals + valsj
    return vals

def main():
    """main function"""
    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(DURATION, SAMPLE_RATE)
    # this is how we drop/raise the frequency over time
    freq = FREQUENCY + ((times * (FREQUENCY_DELTA/DURATION)) % FREQUENCY)
    #freq = FREQUENCY
    vals = shepardtone(times, freq, NUM_OSC)
    vals = wavelib.normalize(vals)
    wavelib.write_wave_file('output/shepard.wav', vals)

main()
