from pathlib import Path
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import subprocess
from multiprocessing import Pool
import os
import pandas as pd

from import_motive_csv import import_motive_csv


def make_image(df_series, index, output_dir, three_dimension_mode=True, target=None, is_mujoco=False, **kwargs):
    fig = plt.figure()
    if target is not None:
        pass
    elif set(['target_pos_X', 'target_pos_Y', 'target_pos_Z',]) <= set(df_series.index.tolist()):
        target = df_series[['target_pos_X', 'target_pos_Y', 'target_pos_Z',]].tolist()
    else:
        # target = [0.1882159569945576, -0.961594395840076, 0.2300116906020579]
        target = [0.1, -1.1, 0.1]
        target = [-.2, -1.05, -.2]
        target = [0.2037190656672287, -0.9606900359757182, -0.0034706211930656816]
    if three_dimension_mode:
        ax = fig.add_subplot(111, projection='3d')
        if not is_mujoco:
            im = ax.scatter(
                df_series["joint4_Position_X"] - df_series["joint1_Position_X"],
                -(df_series["joint4_Position_Z"] - df_series["joint1_Position_Z"]),
                df_series["joint4_Position_Y"] - df_series["joint1_Position_Y"],
                s=5, c='b', label='point4')
            # 線をプロットするなら
            ax.plot(
                [df_series[f"joint{i}_Position_X"] - df_series["joint1_Position_X"] for i in range(1, 5)],
                [-(df_series[f"joint{i}_Position_Z"] - df_series["joint1_Position_Z"]) for i in range(1, 5)],
                [df_series[f"joint{i}_Position_Y"] - df_series["joint1_Position_Y"] for i in range(1, 5)],
                c='g',
            )
            ax.scatter(
                target[0],
                -(target[2]),
                target[1],
                s=5, c='r', label='target')

            ax.text(x=0, y=-1, z=1.1, s=f"step: {index}")

            # ax.set_title('before learning')
            # ax.set_title('after sampling 100k steps')
            ax.set_xlabel("y [m]")
            ax.set_ylabel("x [m]")
            ax.set_zlabel("z [m]")
            ax.set_xlim([-0.5, 0.5])
            ax.set_ylim([-0.5, 0.5])
            ax.set_zlim([-1.4, 0.1])
            ax.legend()
        else:
            raise ValueError(is_mujoco)
    else:
        ax = fig.add_subplot(111)
        if not is_mujoco:
            im = ax.scatter(
                # df_series["joint4_Position_X"] - df_series["joint1_Position_X"],
                -(df_series["joint4_Position_Z"] - df_series["joint1_Position_Z"]),
                df_series["joint4_Position_Y"] - df_series["joint1_Position_Y"],
                s=5, c='b', label='point4')
            # 線をプロットするなら
            ax.plot(
                # [df_series[f"joint{i}_Position_X"] - df_series["joint1_Position_X"] for i in range(1, 5)],
                [-(df_series[f"joint{i}_Position_Z"] - df_series["joint1_Position_Z"]) for i in range(1, 5)],
                [df_series[f"joint{i}_Position_Y"] - df_series["joint1_Position_Y"] for i in range(1, 5)],
                c='g',
            )
            ax.scatter(
                # target[0],
                -(target[2]),
                target[1],
                s=5, c='r', label='target')

            ax.text(
                # x=0,
                x=-0.4,
                y=-0.1,
                s=f"step: {index}"
            )

            # ax.set_title('before learning')
            # ax.set_title('after sampling 100k steps')
            # ax.set_xlabel("y [m]")
            ax.set_xlabel("x [m]")
            ax.set_ylabel("z [m]")
            ax.set_xlim([-0.5, 0.5])
            # ax.set_ylim([-0.5, 0.5])
            ax.set_ylim([-1.4, 0.1])
            ax.legend()
        else:
            raise ValueError(is_mujoco)

    plt.savefig(output_dir/'png'/f"image_{int(index):05d}.png", dpi=300)
    plt.close()


def mocap2movie(
    csvpath,
    not_make_image,
    not_save_video,
    make_gif=True,
    three_dimension_mode=True,
    movie_range=None,
    is_mujoco=False,
    target=None,
):
    output_dir = Path(__file__).parent / "output_mocap2movie"
    basename = os.path.splitext(os.path.basename(csvpath))[0]

    if not not_make_image:
        df = import_motive_csv(csvpath, datatype=["Position"])
        df_interpolate = df.interpolate()
        # df_interpolate = pd.read_csv(csvpath, usecols=[
        #     'joint2_Position_X',
        #     'joint2_Position_Y',
        #     'joint2_Position_Z',
        #     'joint3_Position_X',
        #     'joint3_Position_Y',
        #     'joint3_Position_Z',
        #     'joint4_Position_X',
        #     'joint4_Position_Y',
        #     'joint4_Position_Z',
        #     'target_pos_X', 'target_pos_Y', 'target_pos_Z',
        # ])
        # df_interpolate['joint1_Position_X'] = 0
        # df_interpolate['joint1_Position_Y'] = 0
        # df_interpolate['joint1_Position_Z'] = 0

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
            if int(ind) % 2 == 0:
                arglist.append(
                    [df_series, int(ind)//2, output_dir, three_dimension_mode, target])

        tot_num = len(df_interpolate)
        with Pool(processes=4) as pool:
            pool.starmap(make_image, arglist[:300])

    if not not_save_video:
        # subprocess.run(["ffmpeg", "-framerate", "200", "-i", str(output_dir)+r"/image_%05d.png", "-pix_fmt", "rgb8", "-r", "30", f"{str(output_dir/'out.gif')}"])

        subprocess.run(["ffmpeg", "-framerate", "25", "-i", str(output_dir)+r"/png/image_%05d.png", "-vcodec",
                        "libx264", "-r", "30", "-pix_fmt", "yuv420p", str(output_dir/f'{basename}.mp4')])
    if make_gif:
        subprocess.run(
            ["ffmpeg", "-i", str(output_dir/f'{basename}.mp4'), str(output_dir/f'{basename}.gif')])
        # os.remove(output_dir/'output.mp4')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csvpath')
    parser.add_argument('-i', '--not_make_image', action='store_true')
    parser.add_argument('-s', '--not_save_video', action='store_true')
    parser.add_argument('-g', '--make_gif', action='store_true')
    parser.add_argument('-two', '--two_dimension', action='store_true')
    parser.add_argument('-r', '--movie_range', type=int, nargs=2)
    parser.add_argument('-t', '--target', type=float, nargs=3, default=None)
    args = parser.parse_args()
    mocap2movie(
        args.csvpath,
        args.not_make_image,
        args.not_save_video,
        make_gif=args.make_gif,
        three_dimension_mode=not args.two_dimension,
        movie_range=args.movie_range,
        target=args.target
    )
