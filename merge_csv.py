import sys

import pandas as pd
import glob

DEFAULT_FILE_NAME = "merged.csv"


def main():
    csv_dir_path, merged_csv_name = get_arg_from_cmd()
    merge_csv_files(csv_dir_path, merged_csv_name)


def merge_csv_files(input_dir, output_file):
    # 获取输入目录下的所有CSV文件
    csv_files = glob.glob(input_dir + "/*.csv")

    # 读取第一个CSV文件作为基础数据框
    df = pd.read_csv(csv_files[0])

    # 遍历剩余的CSV文件，并将它们的内容合并到基础数据框中
    for csv_file in csv_files[1:]:
        df_temp = pd.read_csv(csv_file)
        df = pd.concat([df, df_temp], ignore_index=True)

    # 将合并后的数据框写入输出文件
    df.to_csv(output_file, index=False)
    print("已成功合并csv文件并保存到" + output_file + "文件中。")


def get_arg_from_cmd():
    # 获取命令行参数
    args = sys.argv
    # 打印命令行参数
    print("Command line arguments:", args)
    # 获取第一个参数（脚本名称）
    script_name = args[0]
    print("Script name:", script_name)
    # 获取其他参数
    if len(args) == 3:
        csv_dir_path = args[1]
        print("csv_dir_path:", csv_dir_path)
        merged_csv_name = args[2]
        print("merged_csv_name:", merged_csv_name)
        return csv_dir_path, merged_csv_name
    elif len(args) == 2:
        csv_dir_path = args[1]
        print("csv_dir_path:", csv_dir_path)
        return csv_dir_path, DEFAULT_FILE_NAME
    else:
        print(f"Arguments Invalid. \n")
        print("用法：python <merge_csv.py> <csv_dir_path> [<merged_csv_name>] \n")
        print("  csv_dir_path     所需合并的csv文件夹路径")
        print("  merged_csv_name  合并的csv文件名称")
        sys.exit()


if __name__ == "__main__":
    main()
