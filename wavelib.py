""" Wave tools """
import wave
import struct
import numpy as np

SAMPLE_RATE = 44100.0       # hertz
MAX_AMP = 32767.0           # max wave amplitude

FREQ_A1 = 55.0
FREQ_A2 = FREQ_A1*2.0
FREQ_A3 = FREQ_A2*2.0
FREQ_A4 = FREQ_A3*2.0
FREQ_A5 = FREQ_A4*2.0
FREQ_A6 = FREQ_A5*2.0
FREQ_A7 = FREQ_A6*2.0
FREQ_A8 = FREQ_A7*2.0

UNISON = 1.0/1.0
MAJOR_SECOND = 9.0/8.0
DIMINISHED_THIRD = 256.0/225.0
MINOR_THIRD = 6.0/5.0
MAJOR_THIRD = 5.0/4.0
AUGMENTED_THIRD = 125.0/96.0
PERFECT_FOURTH = 4.0/3.0
PERFECT_FIFTH = 3.0/2.0
DIMINISHED_FIFTH = 64.0/45.0
AUGMENTED_FIFTH = 25.0/16.0
MINOR_SIXTH = 8.0/5.0
MAJOR_SIXTH = 5.0/3.0
DIMINISHED_SEVENTH = 128.0/75.0
HARMONIC_SEVENTH = 7.0/4.0
MINOR_SEVENTH = 9.0/5.0
MAJOR_SEVENTH = 15.0/8.0
AUGMENTED_SEVENTH = 125.0/64.0
OCTAVE = 2.0/1.0

def createtimes(duration_seconds, sample_rate=SAMPLE_RATE):
    """create a numpy array holding the timestamp of each wave data point"""
    return np.arange(0, duration_seconds, 1.0/sample_rate)

def zero(times):
    """create a numpy array holding 0's"""
    return times * 0

def glissando_lin(times, start_freq, end_freq):
    """returns frequency array to represent glissando from start to end pitches, 
    using linear scaling"""
    freq = linear_scale_x(times, start_freq, end_freq)
    return freq

def glissando(times, start_freq, end_freq):
    """returns frequency array to represent glissando from start to end pitches, 
    using exponential scaling for more natural sound"""
    a = times[0]
    b = times[len(times)-1]
    n = b-a
    print('a', a, 'b', b, 'n', n, 'times', times)
    g = (end_freq/start_freq) ** (1.0/n)
    freq = start_freq * (g**(times-a))
    return freq

def glissando_rate(times, start_freq, freq_rate):
    """returns frequency array to represent glissando from start at a given rate"""
    return (start_freq + (times*freq_rate))

def discrete(times, start_freq, end_freq, steps):
    """returns frequency array to represent steps from start to end pitches"""
    falling = end_freq < start_freq
    if falling:
        freq = start_freq * (2.0 ** (-1* ((times//1.0)/steps))) # floor to even steps
    else:
        freq = start_freq * (2.0 ** ((times//1.0)/steps)) # floor to even steps
    return freq

def get_phase_correction_periodic(times, freq_hz):
    """ Calculate phase correction for the frequencies in the case of moving frequencies,
    or otherwise the resulting tone will rise or fall much faster due to the various frequencies
    being out of phase with each other.
    https://stackoverflow.com/questions/3089832/sine-wave-glissando-from-one-pitch-to-another-in-numpy
    """
    do_phase_correct = type(freq_hz).__module__ == np.__name__
    phase_correction = 1.0
    if do_phase_correct:
        phase_correction = np.add.accumulate(times*np.concatenate((np.zeros(1), 2.0*np.pi*(freq_hz[:-1]-freq_hz[1:]))))
    return phase_correction

def get_phase_correction_linear(times, freq_hz):
    """ Calculate phase correction for the frequencies in the case of moving frequencies,
    or otherwise the resulting tone will rise or fall much faster due to the various frequencies
    being out of phase with each other.
    https://stackoverflow.com/questions/3089832/sine-wave-glissando-from-one-pitch-to-another-in-numpy
    """
    do_phase_correct = type(freq_hz).__module__ == np.__name__
    phase_correction = 1.0
    if do_phase_correct:
        phase_correction = np.add.accumulate(times*np.concatenate((np.zeros(1), (freq_hz[:-1]-freq_hz[1:]))))
    return phase_correction

def sinewave(times, freq_hz):
    """sine wave"""
    phase_correction = get_phase_correction_periodic(times, freq_hz)
    vals = np.sin(freq_hz*times*2.0*np.pi+phase_correction)
    return vals

def sawtooth(times, freq_hz):
    """sawtooth wave"""
    phase_correction = get_phase_correction_linear(times, freq_hz)
    vals = 2 * ((times * freq_hz + phase_correction) % 1.0) - 1
    return vals

def triangle(times, freq_hz):
    """triangle wave"""
    period = 1.0/freq_hz
    phase_correction = get_phase_correction_periodic(times, freq_hz)
    vals = (2.0 / np.pi )* np.arcsin(np.sin(2.0*np.pi*times/period + phase_correction))
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

def play_n(vals, n):
    return np.tile(vals, n)

def write_wave_file(filename, vals, nchannels=2, sample_width=2, sample_rate=SAMPLE_RATE):
    """Write wave values to file. Assumes vals have been normalized to 1.0 scale"""
    f_str = []
    for i in vals:
        amp = int(i * MAX_AMP)
        data = struct.pack('<hh', amp, amp) # < means little endian, hh because 2 integers
        #f.writeframes(data) # cade says append to string instead of writing frames here
        f_str.append(data)
    wavef = wave.open(filename, 'wb')
    wavef.setnchannels(nchannels)
    wavef.setsampwidth(sample_width)
    wavef.setframerate(sample_rate)
    wavef.writeframes(b''.join(f_str))
    #wavef.writeframes('')
    wavef.close()

def shepardtone(times, freq, waveform_generator = sinewave, peak_freq=FREQ_A4, num_octaves_down=3, num_octaves_up=3):
    """generates a shepard tone using octaves of the given frequency"""
    print('freq ', freq)

    # if peak_freq == None:
    #     peak_freq = np.average(peak_freq) * 1.5

    # TODO need a more octave-friendly kind of modulo.  e.g. 220 -> 440.  880 -> 440, 
    #freq = freq % peak_freq + peak_freq
    #freq = freq % peak_freq + peak_freq
    #print ('freq modulo', freq)

    vals = waveform_generator(times, freq)

    for i in range(0, num_octaves_down):
        freqi = freq * 2.0**(-(i+1))
        #print 'i', i, freqi
        valsi = waveform_generator(times, freqi)
        if i == (num_octaves_down-1):
            #intsi = (freq - peak_freq)/peak_freq
            intsi = np.abs(freq - peak_freq)/peak_freq
            #print("intsi last lower octave ", i, intsi)
            valsi = valsi * intsi
        vals += valsi

    for i in range(0, num_octaves_up):
        freqi = freq * 2.0**(i+1)
        #print 'i', i, freqi
        valsi = waveform_generator(times, freqi)
        if i == (num_octaves_up-1):
            # intsi = 1.0 - (freq - peak_freq)/peak_freq
            #intsi = 1.0 - (freq - peak_freq)/(np.maximum(peak_freq, freq))
            intsi = 1.0 - np.abs(peak_freq - freq)/peak_freq
            #print("intsi last upper octave ", i, intsi)
            valsi = valsi * intsi
        vals += valsi

    return vals

def fx_delay(vals, delay_ms = 500.0, decay = 0.5, sample_rate=SAMPLE_RATE):
    delay_samples = int(delay_ms * sample_rate/1000.0)
    # note we are effecting the array in-place.  could return just the effects portion as separate array???
    #valsd = np.zeros(vals.shape)
    return fx_delay_num_samples(vals, delay_samples, decay)

def fx_delay_num_samples(vals, delay_samples = 500, decay = 0.5):
    # note we are effecting the array in-place.  could return just the effects portion as separate array???
    #valsd = np.zeros(vals.shape)
    valsd = vals
    for i in range(0, len(vals)-delay_samples):
        valsd[i+delay_samples] += vals[i] * decay
    return valsd

def fx_delay_np(vals, delay_ms, decay, sample_rate=SAMPLE_RATE):
    """delay. same as fx_delay but this will allow the decay to be a numpy array"""
    #####NOTE I'm not sure this is quite right. i think it may not decay properly
    delay_samples = int(delay_ms * sample_rate/1000.0)
    valsd = vals
    valsd[delay_samples:] += valsd[:-delay_samples] * decay
    return valsd

# def fx_reverb(vals, room_size_x = 20.0, decay = 0.5, sample_rate=SAMPLE_RATE):
#     # speed of sound 340 m/s, approximate the echo delay
#     echo_ms = room_size_x/2.0/340.0
#     #TODO use echo delay
#     #TODO use decay_multiplier
#     #delay_samples_list = [919, 997, 1061, 1093, 1129, 1151, 1171, 1187, 1213, 1237, 1259, 1283, 1303, 1319, 1327, 1361]
#     delay_samples_list = [97, 191, 277, 367, 457, 541, 639, 737, 821, 919, 997, 1061, 1093, 1129, 1151, 1171, 1187, 1213, 1237, 1259, 1283, 1303, 1319, 1327, 1361]
#     #delay_samples_list = [919,  1061,  1129,  1171,  1213,  1259,  1303,  1327]
    
#     for i in range(len(delay_samples_list)):
#         #vals = fx_delay_num_samples(vals, delay_samples_list[i], decay /(i+1))
#         vals = fx_delay_num_samples(vals, delay_samples_list[i], decay /(2.0**i))

#     return vals

# def comb_filter(vals, delay_time=29.7, reverb_time=1.0):
#     out = 0
#     output = np.zeros(vals.shape)
#     delay_buffer = np.zeros(vals.shape)
#     pos = 0
#     g = 0.001 ** (delay_time/reverb_time)
#     for i in range(1,len(vals)-1):
#         out = delay_buffer[pos]
#         delay_buffer[pos] = vals[i] + out*g
#         output[i] = out
#         pos = pos + 1

#     return output

# def all_pass_filter(vals, delay_time=29.7, reverb_time=1.0):
#     out = 0
#     output = np.zeros(vals.shape)
#     delay_buffer = np.zeros(vals.shape)
#     pos = 0
#     g = 0.001 ** (delay_time/reverb_time)
#     for i in range(len(vals)):
#         out = delay_buffer[pos]
#         delay_buffer[pos] = vals[i] + out*g
#         vals[i] = out - g*input[i]
#         pos = pos + 1

#     return output
