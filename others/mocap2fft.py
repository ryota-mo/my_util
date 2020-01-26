import os
import numpy as np
import matplotlib.pyplot as plt

from import_motive_csv import import_motive_csv


def mocap2fft(csvpath, save, tex=False, plot_range=None):
    if tex:
        plt.style.use("texstyle")
        plt.rcParams['font.size'] = 8
        width = 2.9
        plt.rcParams['figure.figsize'] = (width, width*0.75)

    df = import_motive_csv(csvpath, datatype=["Position"])
    df_interpolate = df.interpolate()

    # Sample spacing (inverse of the sampling rate).
    sample_spaceing = df['Time (Seconds)'].diff().mean()
    freq = np.fft.fftfreq(len(df_interpolate), d=sample_spaceing)

    fig = plt.figure()

    len_df = len(df_interpolate)
    if plot_range is None:
        plot_range = (0, min(len_df, int(1/sample_spaceing))//2)

        # plt.xlim(0, min(len(df_interpolate), int(1/sample_spaceing))//2)
    # plotrange
    plt.plot(freq[:len_df//2], np.fft.fft(df_interpolate["joint2_Position_X"]).real[:len_df//2], label="joint2_Position_X")
    plt.plot(freq[:len_df//2], np.fft.fft(df_interpolate["joint3_Position_X"]).real[:len_df//2], label="joint3_Position_X")
    plt.plot(freq[:len_df//2], np.fft.fft(df_interpolate["joint4_Position_X"]).real[:len_df//2], label="joint4_Position_X")

    plt.title("Fourier transform (period: 1 s)")
    plt.xlabel("frequency [Hz]")
    plt.ylabel("amplitude")
    plt.xlim(plot_range)
    plt.grid()
    plt.legend()
    if save:
        if tex:
            suffix = ".pdf"
        else:
            suffix = ".png"
        filename = os.path.splitext(csvpath)[0] + "fft" + suffix
        plt.savefig(filename, transparent=True, bbox_inches='tight')
    else:
        plt.show()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csvpath')
    parser.add_argument('-s', '--save', action='store_true')
    parser.add_argument('-a', '--add_desc', action='store_true')
    parser.add_argument('-f', '--filepath', default=False)
    parser.add_argument('-t', '--tex', action='store_true', help='for LaTeX, save pdf and so on.')
    parser.add_argument('-r', '--plot_range', type=int, nargs=2)
    args = parser.parse_args()
    mocap2fft(csvpath=args.csvpath, save=args.save, tex=args.tex, plot_range=args.plot_range)
