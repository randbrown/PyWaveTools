import matplotlib.pyplot as plt
import numpy as np

SAMPLE_RATE = 44100.0       # hertz

def plot_show(t, data, title='Data'):
    fig, ax = plt.subplots()
    ax.plot(t, data)
    ax.set(xlabel='time (s)', ylabel='data (wave)', title=title)
    ax.grid()
    #fig.savefig("test.png")
    plt.show()

def fft_plot(t, vals, sample_rate=SAMPLE_RATE):
    fourier = np.fft.fft(vals)
    T = 1.0/sample_rate
    N = len(vals)
    freqs = np.linspace(0.0, 1.0/(2.0*T), N//2)
    plt.plot(freqs, 2.0/N * np.abs(fourier[0:N//2]))
    plt.grid()
    plt.show()

def plot_wave_and_fft(t, vals):
    plt.subplot(2, 1, 1)
    plt.plot(t, vals, 'ko-')
    plt.title('Wave data')
    plt.ylabel('Intensity')
    plt.xlabel('time (s)')

    fourier = np.fft.fft(vals)
    T = 1.0/SAMPLE_RATE
    N = len(vals)
    freqs = np.linspace(0.0, 1.0/(2.0*T), N//2)

    ax = plt.subplot(2, 1, 2)
    plt.plot(freqs, 2.0/N * np.abs(fourier[0:N//2]))
    plt.xlabel('frequency (Hz)')
    plt.ylabel('Intensity')
    # ax.set_xscale('log')
    # from matplotlib.ticker import ScalarFormatter
    # ax.xaxis.set_major_formatter(ScalarFormatter())
    plt.tight_layout()
    plt.show()