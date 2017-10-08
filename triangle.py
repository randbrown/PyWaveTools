""" Generate falling triad sawtooth wave """
import wavelib

SAMPLE_RATE = 44100.0   # hertz
DURATION = 5.0          # seconds
FREQUENCY = 440.0       # hertz
FREQUENCY_RATE = -10.0   # fall at 10 hz per second

def main():
    """main function"""
    # x is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(DURATION, SAMPLE_RATE)
    # constant frequency
    freq = FREQUENCY
    vals = wavelib.triangle(times, freq)
    vals = wavelib.normalize(vals)
    wavelib.write_wave_file('output/triangle.wav', vals)

    # changing frequency
    freq = (FREQUENCY + (times*FREQUENCY_RATE))
    vals = wavelib.triangle(times, freq)
    vals = wavelib.normalize(vals)
    wavelib.write_wave_file('output/fallingtriangle.wav', vals)

main()
