""" Generate shepard tone """
import numpy as np
import wavelib
import math

SAMPLE_RATE = 44100.0       # hertz
DURATION = 1.0            # seconds
FREQUENCY = 440.0           # hertz
# FREQUENCY_RATE = -100.0     # fall at N hz per second
FREQUENCY_DELTA = 440.0     # rise/fall N hz total
MAX_AMP = 32767.0

def normalpdf_base(x):
    return (1.0/((2.0*math.pi)**.5)) * math.e**(-0.5 * x **2.0)

def normalpdf(x, u, o):
    return (1.0/o)*normalpdf_base((x-u)/o)

def cos_dist(x, u, o=12.0):
    return (1.0 + np.cos((2.0*math.pi * (x - u))/o))/2.0

def shepard_util(times, freq, mult):
    val = np.sin(freq*(2.0*math.pi) * mult * times)
    return val

def shepardtone(times, freq, index):
    """generates a shepard tone using frequency multiples of the given frequency"""
    print freq
    vals = []

    num_octaves = 10

    # lower octaves
    for osc in range(num_octaves, 0, -1):
        vals += [shepard_util(times, freq, 2.0**(-osc))]

    # actual primary freq
    vals += [shepard_util(times, freq, 1)]

    # higher octaves
    for osc in range(1, num_octaves):
        vals += [shepard_util(times, freq, 2.0**(osc))]

    #vals = [vals[i] * normalpdf(i, 0, len(vals)/2.0) for i in range(0, len(vals))]
    vals_combined = np.zeros(vals[0].shape)
    for i in range(0, len(vals)):
        #pdf = normalpdf(i, len(vals)*((index)/12.0), len(vals)/3.0)
        pdf = cos_dist(i, len(vals)*(1.0 - (.4 + ((index)/12.0) * .2)), len(vals))
        print 'pdf = ', pdf
        vals_combined += vals[i] * pdf

    return vals_combined

def main():
    """main function"""
    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(12 * DURATION, SAMPLE_RATE)

    vals_list = np.arange(0, 0)

    #start_freq = 263.0

    start_freq = 440.0 * (2 ** ((times//1)/12.0))

    vals_list = wavelib.normalize(shepardtone(times, start_freq, times))

    """
    for m in range(0, 12):
        vals = shepardtone(times, 2.0**(float(m)/12.0)*start_freq, m)
        vals = wavelib.normalize(vals)
        wavelib.write_wave_file('output/shepard' + str(m) + '.wav', vals)
        vals_list = np.concatenate((vals_list, vals), axis=0) 
    """
    # and lets run through it twice, so cat the list together with itself 
    vals_list = np.concatenate((vals_list, vals_list), axis=0) 
    wavelib.write_wave_file('output/shepard_steps2x.wav', vals_list)

main()
