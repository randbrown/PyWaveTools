""" Generate falling triad sine wave """
import wavelib

SAMPLE_RATE = 44100.0   # hertz
DURATION = 5.0          # seconds
FREQUENCY = 440.0       # hertz
FREQUENCY_RATE = -10.0   # fall at 10 hz per second

def main():
    """main function"""
    # x is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(DURATION, SAMPLE_RATE)
    freq = FREQUENCY + (times*FREQUENCY_RATE)
    vals1 = wavelib.sinewave(times, freq)
    vals2 = wavelib.sinewave(times, freq* 3/2)  # perfect fifth
    vals3 = wavelib.sinewave(times, freq* 5/4)  # perfect third
    vals = vals1 + vals2 + vals3
    vals = wavelib.normalize(vals)
    wavelib.write_wave_file('output/fallingtriad.wav', vals)

main()
