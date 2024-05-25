import csv
import sys


def main():
    input_file, output_file, columns = get_arg_from_cmd()
    extract_columns(input_file, output_file, columns)


# 从表头中返回所需列名的索引数组
def get_copy_column_index_list(header, column_names):
    indices = []
    for column_name in column_names:
        try:
            index = header.index(column_name)
            indices.append(index)
        except ValueError:
            print(f"列名 '{column_name}' 未找到。")
    return indices


def extract_columns(input_file, output_file, columns):
    with open(input_file, 'r', newline='', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # 读取并写入表头
        header = next(reader)

        # 从表头中返回所需列名的索引数组
        copy_column_index_list = get_copy_column_index_list(header, columns)

        writer.writerow([header[i] for i in copy_column_index_list])

        # 读取并写入指定列的数据
        for row in reader:
            writer.writerow([row[i] for i in copy_column_index_list])
    print("extract success.")


def get_arg_from_cmd():
    # 获取命令行参数
    args = sys.argv
    # 打印命令行参数
    print("Command line arguments:", args)
    # 获取第一个参数（脚本名称）
    script_name = args[0]
    print("Script name:", script_name)
    # 获取其他参数
    if len(args) > 3:
        source_csv_path = args[1]
        print("source_csv_path:", source_csv_path)
        output_csv_name = args[2]
        print("output_csv_name:", output_csv_name)
        columns = args[3:]
        print("columns:", columns)
        return source_csv_path, output_csv_name, columns
    else:
        print(f"Arguments Invalid. \n")
        print("用法：python <csv_extract_column.py> <source_csv_path> <output_csv_name> [<columns>..] \n")
        print("  source_csv_path  所需提取的csv文件路径")
        print("  output_csv_name  输出的文件名称")
        print("  columns          所需截取的列名，空格隔开即可")
        sys.exit()


if __name__ == "__main__":
    main()
