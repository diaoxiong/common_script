import csv
import os
import sys
import math


def main():
    input_file, csv_file_split_size, output_dir = get_arg_from_cmd()
    split_csv_by_size(input_file, output_dir, csv_file_split_size)


def get_arg_from_cmd():
    # 获取命令行参数
    args = sys.argv
    # 打印命令行参数
    print("Command line arguments:", args)
    # 获取第一个参数（脚本名称）
    script_name = args[0]
    print("Script name:", script_name)
    # 获取其他参数
    if len(args) >= 3:
        source_csv_path = args[1]
        print("source_csv_path:", source_csv_path)
        csv_file_size_threshold = int(args[2])
        csv_file_split_size = csv_file_size_threshold * 1024 * 1024
        print(f"csv_file_size_threshold: {csv_file_size_threshold} MB")

        if len(args) >= 4:
            output_dir = args[3]
        else:
            source_csv_directory = os.path.dirname(source_csv_path)
            output_dir = "{}/{}".format(source_csv_directory, "csv_split_output")
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

        print("output_dir:", output_dir)

        return source_csv_path, csv_file_split_size, output_dir
    else:
        print(f"Arguments Invalid. \n")
        print("用法：python split_csv.py <source_csv_path> <csv_file_size_threshold> [<output_directory_path>] \n")
        print("将一个csv文件转换为sql insert语句，列名与csv表头一致，文件生成在csv文件所在目录下与表名相同的文件夹内")
        print("  source_csv_path           所需提取的csv文件路径")
        print("  csv_file_size_threshold   csv文件的大小阈值，单位为MB，默认无")
        print("  output_directory_path     输出文件目录的路径，若无则默认在csv文件相同的目录下新建目录")
        sys.exit()


def split_csv_by_size(input_file, output_dir, max_size):
    output_prefix = "{}/{}".format(output_dir, os.path.basename(input_file))
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        # 读取表头
        header = next(reader)
        chunk_number = 1
        current_size = 0
        rows = []

        for row in reader:
            # 估算当前行的大小
            row_size = len(','.join(map(str, row)).encode('utf-8'))
            if current_size + row_size > max_size:
                # 若加上当前行超过最大文件大小，则保存当前块
                output_file = f'{output_prefix}_{chunk_number}.csv'
                with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    # 写入表头
                    writer.writerow(header)
                    # 写入数据行
                    writer.writerows(rows)
                # 重置相关变量
                rows = []
                current_size = 0
                chunk_number += 1
            # 添加当前行到当前块
            rows.append(row)
            current_size += row_size

        # 处理最后一个块
        if rows:
            output_file = f'{output_prefix}_{chunk_number}.csv'
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                writer.writerows(rows)


if __name__ == "__main__":
    main()