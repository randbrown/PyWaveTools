""" Wave tools """
import wave
import math
import struct
import numpy as np

SAMPLE_RATE = 44100.0       # hertz
MAX_AMP = 32767.0           # max wave amplitude

def createtimes(duration_seconds, sample_rate=SAMPLE_RATE):
    """create a numpy array holding the timestamp of each wave data point"""
    return np.arange(0, duration_seconds, 1.0/sample_rate)

def zero(times):
    """create a numpy array holding 0's"""
    return times * 0

def glissando(times, start_freq, end_freq):
    """returns frequency array to represent glissando from start to end pitches"""
    # some weird problem where we only need to scale "half way there" to get the desired pitch
    return linear_scale_x(times, start_freq, (start_freq + end_freq)/2.0) 

def glissando_rate(times, start_freq, freq_rate):
    """returns frequency array to represent glissando from start at a given rate"""
    # some weird problem where we only need to scale "half way there" to get the desired pitch
    return (start_freq + (times*freq_rate/2.0)) 

def discrete(times, start_freq, end_freq, steps):
    """returns frequency array to represent steps from start to end pitches"""
    falling = end_freq < start_freq
    if falling:
        freq = start_freq * (2.0 ** (-1* ((times//1.0)/steps))) # floor to even steps
    else:
        freq = start_freq * (2.0 ** ((times//1.0)/steps)) # floor to even steps
    return freq

def sinewave(times, freq_hz):
    """sine wave"""
    vals = np.sin(freq_hz*times*2.0*np.pi)
    return vals

def sawtooth(times, freq_hz):
    """sawtooth wave"""
    period = 1.0/freq_hz
    vals = 2.0 * (times/period - np.floor(.5 + times/period))
    return vals

def triangle(times, freq_hz):
    """triangle wave"""
    period = 1.0/freq_hz
    vals = (2.0 / np.pi )* np.arcsin(np.sin(2.0*np.pi*times/period))
    return vals

def square(times, freq_hz):
    """square wave"""
    vals = np.sign(sinewave(times, freq_hz))
    return vals

def normalize(vals):
    """normalize values to 1.0 scale"""
    return vals / np.max(np.abs(vals))

def linear_scale(x, minx, maxx, miny, maxy):
    return ((x - minx) / (maxx - minx)) * (maxy - miny) + miny

def linear_scale_x(x, miny, maxy):
    return ((x - x.min()) / (x.max() - x.min())) * (maxy - miny) + miny

def square_scale_x(x, miny, maxy):
    xx = linear_scale_x(x, 0, 1.0)
    return np.power(xx, 2)

def quad_scale_x(x, miny, maxy):
    """good approximation of exp for 0-1"""
    xx = linear_scale_x(x, 0, 1.0)
    return np.power(xx, 4)

def exp_scale_x(x, miny, maxy):
    """exponentially scale x to y values"""
    xx = linear_scale_x(x, 0, 1.0)
    return np.exp(6.908*xx)/1000.0

def write_wave_file(filename, vals, nchannels=2, sample_width=2, sample_rate=SAMPLE_RATE):
    """Write wave values to file. Assumes vals have been normalized to 1.0 scale"""
    f_str = ''
    for i in vals:
        amp = int(i * MAX_AMP)
        data = struct.pack('<hh', amp, amp) # < means little endian, hh because 2 integers
        #f.writeframes(data) # cade says append to string instead of writing frames here
        f_str += data
    wavef = wave.open(filename, 'wb')
    wavef.setnchannels(nchannels)
    wavef.setsampwidth(sample_width)
    wavef.setframerate(sample_rate)
    wavef.writeframes(f_str)
    wavef.writeframes('')
    wavef.close()
