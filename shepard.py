""" Generate shepard tone """
import math
import wavelib
import numpy as np

DURATION = 1.0            # seconds

def normalpdf_base(x):
    return (1.0/((2.0*math.pi)**.5)) * math.e**(-0.5 * x **2.0)

def normalpdf(x, u, o):
    return (1.0/o)*normalpdf_base((x-u)/o)

def cos_dist(x, u, o=12.0):
    return (1.0 + np.cos((2.0*math.pi * (x - u))/o))/2.0

def shepard_util(times, freq):
    print freq
    val = np.sin(freq*(2.0*math.pi) * times)
    return val

def shepardtone(times, freq, index):
    """generates a shepard tone using frequency multiples of the given frequency"""
    print freq
    osc_list = []
    num_octaves = 10

    # lower octaves
    for osc in range(num_octaves, 0, -1):
        print 'octave = ', 2.0**(-osc)
        osc_list += [shepard_util(times, freq * 2.0**(-osc))]

    # actual primary freq
    print 'primary freq'
    osc_list += [shepard_util(times, freq)]

    # higher octaves
    for osc in range(1, num_octaves):
        print 'octave = ', 2.0**(osc)
        osc_list += [shepard_util(times, freq * 2.0**(osc))]

    vals = np.zeros(osc_list[0].shape)
    for i in range(0, len(osc_list)):
        #pdf = normalpdf(i, len(osc_list)*((index)/12.0), len(osc_list)/3.0)
        pdf = cos_dist(i, len(osc_list)*(1.0 - (.4 + ((index)/12.0) * .2)), len(osc_list))
        print 'pdf = ', pdf
        vals += osc_list[i] * pdf

    return vals

def main():
    """main function"""
    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(12 * DURATION)

    #start_freq = 263.0
    start_freq = 440.0 * (2.0 ** ((times//1.0)/12.0))
    #start_freq = 440.0 * (2.0 ** ((times)/12.0))

    vals_list = np.arange(0, 0)
    vals_list = wavelib.normalize(shepardtone(times, start_freq, times))

    # and lets run through it twice, so cat the list together with itself
    vals_list = np.concatenate((vals_list, vals_list), axis=0) 
    wavelib.write_wave_file('output/shepard_steps2x.wav', vals_list)

main()
