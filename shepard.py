""" Generate shepard tone """
import wavelib
#import plotlib

FREQ_A4 = 440.0
STEPS = 12.0
DURATION_PER_STEP = 1.0            # seconds
TOTAL_DURATION = DURATION_PER_STEP * STEPS

def shepard_glissando(times, freq_start, freq_end):
    # the exponential glissando sounds good, but when stitching together with play_n,
    # there is an audible click. perhaps due to rounding?
    # so for now I'm leaving this as the linear scaling to avoid the click... TODO fix it
    #freq = wavelib.glissando(times, freq_start, freq_end)
    freq = wavelib.glissando_lin(times, freq_start, freq_end)
    print('gliss: ', freq)
    vals = wavelib.shepardtone(times, freq)
    return vals

def shepard_discrete(times, freq_start, freq_end):
    freq = wavelib.discrete(times, freq_start, freq_end, STEPS)
    print('discrete: ', freq)
    vals = wavelib.shepardtone(times, freq)
    return vals

def main():
    """main function"""

    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(TOTAL_DURATION)

    vals = wavelib.normalize(shepard_glissando(times, FREQ_A4*2, FREQ_A4))
    #plotlib.plot_wave_and_fft(times, vals)
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_glissando_down_2x.wav', vals)

    vals = wavelib.normalize(shepard_discrete(times, FREQ_A4*2, FREQ_A4))
    #plotlib.plot_wave_and_fft(times, vals)
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_discrete_down_2x.wav', vals)

    vals = wavelib.normalize(shepard_glissando(times, FREQ_A4, FREQ_A4*2))
    #plotlib.plot_wave_and_fft(times, vals)
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_glissando_up_2x.wav', vals)

    vals = wavelib.normalize(shepard_discrete(times, FREQ_A4, FREQ_A4*2))
    #plotlib.plot_wave_and_fft(times, vals)
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/shepard_discrete_up_2x.wav', vals)

main()
