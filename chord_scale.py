""" Generate chord scale. Invert each chord as necessary to fit within the range of an octave.
Generates two versions, one using equal temperament harmonies, and the other using just
 intonation """
import wavelib

SAMPLE_RATE = 44100.0
NOTE = wavelib.FREQ_A3
NOTES = [NOTE, NOTE * (2**(2/12.0)), NOTE * (2**(4/12.0)), NOTE * (2**(5/12.0)), NOTE * (2**(7/12.0)), NOTE * (2**(9/12.0)), NOTE * (2**(11/12.0))]
JI_INTERVALS = [wavelib.UNISON, wavelib.MAJOR_SECOND, wavelib.MAJOR_THIRD, wavelib.PERFECT_FOURTH, wavelib.PERFECT_FIFTH, wavelib.MAJOR_SIXTH, wavelib.MAJOR_SEVENTH]

NOTE_DURATION = 1   # play each n seconds
DURATION = len(NOTES) * NOTE_DURATION

def chord_scale_equal_temperament():
    times = wavelib.createtimes(DURATION, SAMPLE_RATE)
    intervals = [1, 3, 5, 7]
    vals = wavelib.zero(times)
    for interval in intervals:
        freq = wavelib.zero(times)
        for n in range(len(NOTES)):
            idx = (n + interval-1) % len(NOTES) 
            f = NOTES[idx]
            startidx = int(n * NOTE_DURATION * SAMPLE_RATE)
            endidx = int(((n+1) * NOTE_DURATION) * SAMPLE_RATE)
            freq[startidx:endidx] = f
        vals += wavelib.sinewave(times, freq)

    vals = wavelib.normalize(vals)
    vals = wavelib.play_n(vals, 3)
    wavelib.write_wave_file('output/chord_scale_equal_temperament.wav', vals)

def chord_scale_just_intonation():
    times = wavelib.createtimes(DURATION, SAMPLE_RATE)
    intervals = [1, 3, 5, 7]
    vals = wavelib.zero(times)
    for interval in intervals:
        freq = wavelib.zero(times)
        for n in range(len(NOTES)):
            idx = (n + interval-1) % len(NOTES) 
            interval_ratio = JI_INTERVALS[idx]
            # always use intervals from the root note, so the harmonies are just
            f = NOTES[0] * interval_ratio
            startidx = int(n * NOTE_DURATION * SAMPLE_RATE)
            endidx = int(((n+1) * NOTE_DURATION) * SAMPLE_RATE)
            freq[startidx:endidx] = f
        vals += wavelib.sinewave(times, freq)

    vals = wavelib.normalize(vals)
    vals = wavelib.play_n(vals, 3)
    wavelib.write_wave_file('output/chord_scale_just_intonation.wav', vals)


chord_scale_equal_temperament()
chord_scale_just_intonation()
