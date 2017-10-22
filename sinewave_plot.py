""" Generate sine wave tone and plot the wav and frequency (using FFT) """
import wavelib
import plotlib

DURATION = 1.0            # seconds

def main():
    """main function"""
    # times is array of values at each time slot of the whole wav file
    times = wavelib.createtimes(DURATION)
    vals = wavelib.sinewave(times, wavelib.FREQ_A4)
    vals = wavelib.normalize(vals)
    wavelib.write_wave_file('output/sinewave1.wav', vals)
    # wavelib.plot_show(times, vals)
    # wavelib.fft_plot(times, vals)
    plotlib.plot_wave_and_fft(times, vals)

main()
