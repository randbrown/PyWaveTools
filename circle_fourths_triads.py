""" Generate circles of fourths of dominant seventh chords.
We invert each chord as necessary to fit within the range of an octave. """
import wavelib

SAMPLE_RATE = 44100.0
NOTE = wavelib.FREQ_A3
NOTES = [NOTE]
note = NOTE
for i in range(1, 12):
    note = note * wavelib.PERFECT_FOURTH
    NOTES.append(note)

NOTE_DURATION = 1   # play each n seconds
DURATION = len(NOTES) * NOTE_DURATION

def circle_fourths_discrete():
    notemin = NOTE
    notemax = NOTE * 2
    times = wavelib.createtimes(DURATION, SAMPLE_RATE)
    # use harmonic 7th for smoother beatless chord
    intervals = [wavelib.UNISON, wavelib.MAJOR_THIRD, wavelib.PERFECT_FIFTH, wavelib.HARMONIC_SEVENTH]
    vals = wavelib.zero(times)
    for i in range(len(intervals)):
        interval = intervals[i]
        freq = wavelib.zero(times)
        for n in range(len(NOTES)):
            note = NOTES[n]
            f = NOTES[n] * interval
            while f >= notemax:
                f = f / 2.0
            while f < notemin:
                f = f * 2.0
            startidx = int(n * NOTE_DURATION * SAMPLE_RATE)
            endidx = int(((n+1) * NOTE_DURATION) * SAMPLE_RATE)
            #print i, interval, note, f, startidx, endidx 
            freq[startidx:endidx] = f
        #print n, note, freq
        vals1 = wavelib.sinewave(times, freq)
        vals1 = wavelib.normalize(vals1)
        vals += wavelib.normalize(vals1)

    vals = wavelib.normalize(vals)
    vals = wavelib.play_n(vals, 2)
    wavelib.write_wave_file('output/circle_fourths_chords.wav', vals)

circle_fourths_discrete()
