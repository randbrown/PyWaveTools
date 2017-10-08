""" Generate shepard tone """
import math
import wavelib
import numpy as np

STEPS = 12.0
DURATION_PER_STEP = 1.0            # seconds
TOTAL_DURATION = DURATION_PER_STEP * STEPS

def shepard_glissando(times, freq_start, freq_end, wave_generator, octaves=5):
    falling = freq_end < freq_start
    freq = wavelib.glissando(times, freq_start, freq_end)
    vals = wavelib.shepardtone(times, freq, falling, octaves, wave_generator)
    return vals

def play_twice(vals):
    #return np.concatenate((vals, vals), axis=0) 
    return wavelib.play_n(vals, 2)

def minor_triad_sine(times, freq):
    vals1 = wavelib.sinewave(times, freq)
    vals2 = wavelib.sinewave(times, freq* wavelib.PERFECT_FIFTH) * 0.7  # perfect fifth
    vals3 = wavelib.sinewave(times, freq* wavelib.MINOR_THIRD) * 0.4  # perfect minor third
    vals = vals1 + vals2 + vals3
    return vals

def diminished_fifth_sine(times, freq):
    vals1 = wavelib.sinewave(times, freq)
    vals2 = wavelib.sinewave(times, freq* wavelib.DIMINISHED_FIFTH)
    vals = vals1 + vals2
    return vals

def diminished_full_sine(times, freq):
    vals1 = wavelib.sinewave(times, freq)
    vals2 = wavelib.sinewave(times, freq* wavelib.DIMINISHED_SEVENTH)
    vals2 = wavelib.sinewave(times, freq* wavelib.DIMINISHED_FIFTH)
    vals3 = wavelib.sinewave(times, freq* wavelib.DIMINISHED_THIRD)
    vals = vals1 + vals2 + vals3
    return vals

def augmented_sine(times, freq):
    vals1 = wavelib.sinewave(times, freq)
    vals2 = wavelib.sinewave(times, freq* wavelib.AUGMENTED_FIFTH)
    vals2 = wavelib.sinewave(times, freq* wavelib.AUGMENTED_THIRD)
    vals3 = wavelib.sinewave(times, freq* wavelib.AUGMENTED_SEVENTH)
    vals = vals1 + vals2 + vals3
    return vals

def all_tones_sine(times, freq):
    vals = wavelib.zero(times)
    for i in range(0, 12):
        vals +=wavelib.sinewave(times, freq * 2.0**(i/12.0))
    return vals

def main():
    """main function"""

    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(TOTAL_DURATION)
    # vals = wavelib.normalize(shepard_glissando(times, wavelib.FREQ_A2, wavelib.FREQ_A1, minor_triad_sine, 6))
    # vals = play_twice(vals)
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=100.0, decay=0.5))
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=300.0, decay=0.2))
    # wavelib.write_wave_file('output/shepard_glissando_down_2x_fx_minor.wav', vals)

    # vals = wavelib.normalize(shepard_glissando(times, wavelib.FREQ_A2, wavelib.FREQ_A1, diminished_fifth_sine, 6))
    # vals = play_twice(vals)
    # # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=100.0, decay=0.5))
    # # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=300.0, decay=0.2))
    # wavelib.write_wave_file('output/shepard_glissando_down_2x_fx_diminished.wav', vals)

    # vals = wavelib.normalize(shepard_glissando(times, wavelib.FREQ_A2, wavelib.FREQ_A1, all_tones_sine, 6))
    # vals = play_twice(vals)
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=100.0, decay=0.5))
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=300.0, decay=0.2))
    # wavelib.write_wave_file('output/shepard_glissando_down_2x_fx_all.wav', vals)

    # vals = wavelib.normalize(shepard_glissando(times, wavelib.FREQ_A1, wavelib.FREQ_A2, minor_triad_sine, 6))
    # vals = play_twice(vals)
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=100.0, decay=0.5))
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=300.0, decay=0.2))
    # wavelib.write_wave_file('output/shepard_glissando_up_2x_fx_minor.wav', vals)

    # vals = wavelib.normalize(shepard_glissando(times, wavelib.FREQ_A1, wavelib.FREQ_A2, diminished_fifth_sine, 6))
    # vals = play_twice(vals)
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=100.0, decay=0.5))
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=300.0, decay=0.2))
    # wavelib.write_wave_file('output/shepard_glissando_up_2x_fx_diminished.wav', vals)

    # vals = wavelib.normalize(shepard_glissando(times, wavelib.FREQ_A1, wavelib.FREQ_A2, augmented_sine, 5))
    # vals = play_twice(vals)
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=100.0, decay=0.5))
    # vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=300.0, decay=0.2))
    # wavelib.write_wave_file('output/shepard_glissando_up_2x_fx_augmented.wav', vals)

    vals = wavelib.normalize(shepard_glissando(times, wavelib.FREQ_A2, wavelib.FREQ_A1, diminished_fifth_sine, 6))
    vals = wavelib.play_n(vals, 5)
    vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=100.0, decay=0.5))
    vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=300.0, decay=0.2))
    wavelib.write_wave_file('output/shepard_glissando_down_5x_fx_diminished.wav', vals)

    vals = wavelib.normalize(shepard_glissando(times, wavelib.FREQ_A1, wavelib.FREQ_A2, diminished_fifth_sine, 6))
    vals = wavelib.play_n(vals, 5)
    vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=100.0, decay=0.5))
    vals = wavelib.normalize(wavelib.fx_delay(vals, delay_ms=300.0, decay=0.2))
    wavelib.write_wave_file('output/shepard_glissando_up_5x_fx_diminished.wav', vals)

main()
