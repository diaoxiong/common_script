import csv
import sys
import re


def main():
    source_csv_path, columns = get_arg_from_cmd()

    output_csv = source_csv_path.replace(".csv", "_ac.csv")
    add_column_to_csv(source_csv_path, output_csv, columns)


def get_arg_from_cmd():
    # 获取命令行参数
    args = sys.argv
    # 打印命令行参数
    print("Command line arguments:", args)
    # 获取第一个参数（脚本名称）
    script_name = args[0]
    print("Script name:", script_name)
    if len(args) % 2 != 0 or len(args) < 4:
        print(f"Arguments Invalid. \n")
        print("用法：python <csv2sql.py> <source_csv_path> [<column_name>] [<column_value>]... \n")
        print("将一个csv文件添加列，新生成的文件名后缀为_ac")
        print("  source_csv_path   所需添加列的csv文件路径")
        print("  column_name       列名")
        print("  column_value      列值")
        sys.exit()

    # 获取其他参数
    source_csv_path = args[1]
    print("source_csv_path:", source_csv_path)
    columns = args[2:]

    for i in range(len(columns)):
        if i % 2 == 1:
            continue
        if is_integer(columns[i]):
            columns[i] = int(columns[i])
        elif is_float(columns[i]):
            columns[i] = float(columns[i])

    print("columns:", columns)

    return source_csv_path, columns



def is_integer(s):
    return bool(re.match(r'^-?\d+$', s))


def is_float(s):
    return bool(re.match(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$', s))


def add_column_to_csv(input_csv, output_csv, columns):
    with open(input_csv, 'r') as readCsvfile:
        reader = csv.reader(readCsvfile)
        header = next(reader)  # 读取表头

        for index, value in enumerate(columns):
            if index % 2 == 0:
                header.append(value)  # 添加新列名

        with open(output_csv, 'w', newline='', encoding='utf-8') as writeCsvfile:
            writer = csv.writer(writeCsvfile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(header)  # 写入新的表头

            for row in reader:
                for index, value in enumerate(columns):
                    if index % 2 == 1:
                        row.append(value)  # 为每行添加新列值
                writer.writerow(row)


if __name__ == "__main__":
    main()