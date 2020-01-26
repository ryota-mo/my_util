from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import subprocess
from multiprocessing import Pool
import os
import numpy as np

from import_motive_csv import import_motive_csv


def make_image(df_series, index, output_dir, is_mujoco=False, **kwargs):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    if not is_mujoco:
        target = [-0.006010090186017,-1.13288764369554,0.129542942108335
]
        im = ax.scatter(
            df_series["joint4_Position_X"] - df_series["joint1_Position_X"],
            -(df_series["joint4_Position_Z"] - df_series["joint1_Position_Z"]),
            df_series["joint4_Position_Y"] - df_series["joint1_Position_Y"],
            s=5, c='b', label='joint4')
        # ax.scatter(
        #     target[0] - df_series["joint1_Position_X"],
        #     -(target[2] - df_series["joint1_Position_Z"]),
        #     target[1] - df_series["joint1_Position_Y"],
        #     s=5, c='r', label='target')
        ax.scatter(
            target[0],
            -(target[2]),
            target[1],
            s=5, c='r', label='target')

        ax.text(x=0, y=-1, z=0.4, s=f"step: {index}")

        ax.set_title('epoch 1')
        ax.set_xlabel("y [m]")
        ax.set_ylabel("x [m]")
        ax.set_zlabel("z [m]")
        ax.set_xlim([-0.5, 0.5])
        ax.set_ylim([-0.5, 0.5])
        ax.set_zlim([-2, -0.6])
        ax.legend()
    else:
        raise ValueError(is_mujoco)

    plt.savefig(output_dir/f"image_{int(index):05d}.png")
    plt.close()

def mocap2movie(csvpath, not_make_image, not_save_video, movie_range=None, is_mujoco=False):
    output_dir = Path(__file__).parent / "output_mocap2movie"

    if not not_make_image:
        df = import_motive_csv(csvpath, datatype=["Position"])
        df_interpolate = df.interpolate()

        if movie_range is not None:
            if movie_range[0] == -1:
                df_interpolate = df_interpolate[:len(df_interpolate)//movie_range[1]]
            else:
                df_interpolate = df_interpolate[movie_range[0]:movie_range[1]]

        if output_dir.is_dir():
            for path in output_dir.glob("image_*.png"):
                os.remove(path)

        output_dir.mkdir(exist_ok=True)

        arglist = []
        for ind, df_series in df_interpolate.iterrows():
            arglist.append([df_series, ind, output_dir])

        tot_num = len(df_interpolate)
        with Pool(processes=4) as pool:
            pool.starmap(make_image, arglist)

    if not not_save_video:
        # subprocess.run(["ffmpeg", "-framerate", "200", "-i", str(output_dir)+r"/image_%05d.png", "-pix_fmt", "rgb8", "-r", "30", f"{str(output_dir/'out.gif')}"])

        subprocess.run(["ffmpeg", "-framerate", "50", "-i", str(output_dir)+r"/image_%05d.png", "-vcodec", "libx264", "-r", "30", "-pix_fmt", "yuv420p", f"{str(output_dir/'output.mp4')}"])
        subprocess.run(["ffmpeg", "-i", f"{str(output_dir/'output.mp4')}", f"{str(output_dir/'output.gif')}"])
        # os.remove(output_dir/'output.mp4')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csvpath')
    parser.add_argument('-i', '--not_make_image', action='store_true')
    parser.add_argument('-s', '--not_save_video', action='store_true')
    parser.add_argument('-r', '--movie_range', type=int, nargs=2)
    args = parser.parse_args()
    mocap2movie(args.csvpath, args.not_make_image, args.not_save_video, args.movie_range)
