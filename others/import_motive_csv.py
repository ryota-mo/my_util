import csv
from pathlib import Path
import pandas as pd


def import_motive_csv(csvpath, datatype=[], hz=None, save=False, interpolate=False):
    with open(csvpath, 'r') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i == 1:
                if row:
                    _header = 3
                else:
                    _header = 2
                break

    # headerはName joint1 joint1.1 ... ball.5 ball.6 ball.7など
    df_origin = pd.read_csv(csvpath, index_col=0, header=_header)

    # Positionだけ欲しい
    # datatype = ["Position", "Rotation"]
    if "Position" not in datatype and "Rotation" not in datatype:
        raise ValueError("not 'Position' in datatype and not 'Rotation' in datatype")
    boolfilter = [True if str(x) in datatype else False for x in df_origin.iloc[1]]
    # Time (Seconds)のところだけNaNなので強制的にTrueに
    boolfilter[0] = True

    # TimeとPosition/Rotationだけの新しいデータフレームの作成
    df = df_origin.loc[:, boolfilter]

    # カラムのリネーム
    new_column = {}
    for colname in df.columns:
        if(df[colname][2] == "Time (Seconds)"):
            new_column["Name"] = "Time (Seconds)"
        else:
            new_column[colname] = colname.split(".")[0] + "_" + df[colname][1] + "_" + df[colname][2]

    # カラムのリネーム実行
    df = df.rename(columns=new_column)

    # 列名から実際の値が始まるまでの不要な行を削除し，文字列型になっているのを浮動小数点型に変更
    df = df[3:].astype(float)

    if interpolate:
        df.reset_index(inplace=True)
        df.set_index("Time (Seconds)", inplace=True)
        try:
            # df.interpolate(method=interpolate, limit=None, limit_direction='both', inplace=True)
            df.interpolate(method=interpolate, limit=None, limit_area='inside', inplace=True)
        except ValueError as e:
            print(f"{csvpath}: {e} is not defined")

    if hz is not None:
        df = df[(df["Time (Seconds)"]*hz).is_integer()]

    if save:
        p = Path(csvpath)
        filename = p.stem
        new_filename = filename + '_edit.csv'
        if hz is None:
            output_dir = p.parent.joinpath('motion_edit')
        else:
            output_dir = p.parent.joinpath(f'motion_edit_{hz}hz')
        output_dir.mkdir(exist_ok=True)
        df.to_csv(output_dir.joinpath(new_filename))
        print(f'output: {str(output_dir.joinpath(new_filename))}')

    return df


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('csvpath')
    parser.add_argument('-t', '--datatype', nargs=2, default=["Position", "Rotation"], choices=["Position", "Rotation"])
    parser.add_argument('-i', '--interpolate', action='store_true')
    parser.add_argument('-s', '--save', action='store_true')
    parser.add_argument('--hz', type=int, help='Hz')
    args = parser.parse_args()

    csvpath = Path(args.csvpath).expanduser().resolve()
    if csvpath.is_dir():
        csvlist = csvpath.glob('*.csv')
    elif csvpath.is_file():
        csvlist = [csvpath]
    else:
        raise FileNotFoundError(f'{str(csvpath)} does not exist')

    print(f"Extract data: {args.datatype}")

    for csvfile in csvlist:
        print(csvfile)
        import_motive_csv(csvfile, args.datatype, args.hz, args.save, args.interpolate)
