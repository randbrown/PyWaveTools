""" Generate shepard tone """
import wavelib

FREQ_A4 = 440.0
STEPS = 12.0
DURATION_PER_STEP = 1.0            # seconds
TOTAL_DURATION = DURATION_PER_STEP * STEPS

def shepard_glissando(times, freq_start, freq_end, octaves=5):
    freq = wavelib.glissando(times, freq_start, freq_end)
    print ('gliss: ', freq)
    vals = wavelib.shepardtone(times, freq)
    return vals

def shepard_discrete(times, freq_start, freq_end, octaves=5):
    freq = wavelib.discrete(times, freq_start, freq_end, STEPS)
    print ('discrete: ', freq)
    vals = wavelib.shepardtone(times, freq)
    return vals

def main():
    """main function"""

    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(TOTAL_DURATION)

    vals = wavelib.normalize(shepard_glissando(times, FREQ_A4*2, FREQ_A4, 5))
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_glissando_down_2x.wav', vals)

    vals = wavelib.normalize(shepard_discrete(times, FREQ_A4*2, FREQ_A4, 5))
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_discrete_down_2x.wav', vals)

    vals = wavelib.normalize(shepard_glissando(times, FREQ_A4, FREQ_A4*2, 5))
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_glissando_up_2x.wav', vals)

    vals = wavelib.normalize(shepard_discrete(times, FREQ_A4, FREQ_A4*2, 5))
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_discrete_up_2x.wav', vals)

main()
