import csv
import os
import sys
import math


def main():
    input_file, table_name, rows_per_statement, sql_file_size_threshold = get_arg_from_cmd()
    csv_to_sql_insert(input_file, table_name, rows_per_statement, sql_file_size_threshold)


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
        table_name = args[2]
        print("table_name:", table_name)

        if len(args) >= 4:
            rows_per_statement = int(args[3])
        else:
            rows_per_statement = 10000

        if len(args) == 5:
            sql_file_size_threshold = int(args[4]) * 1024 * 1024
        else:
            sql_file_size_threshold = -1

        return source_csv_path, table_name, rows_per_statement, sql_file_size_threshold
    else:
        print(f"Arguments Invalid. \n")
        print("用法：python <csv2sql.py> <source_csv_path> <table_name> [<rows_per_statement>] [<sql_file_size_threshold>] \n")
        print("将一个csv文件转换为sql insert语句，列名与csv表头一致，文件生成在csv文件所在目录下与表名相同的文件夹内")
        print("  source_csv_path           所需提取的csv文件路径")
        print("  table_name                表名")
        print("  rows_per_statement        每个insert插入多少行，默认10000")
        print("  sql_file_size_threshold   sql文件的大小阈值，单位为MB，默认无")
        sys.exit()


def infer_data_type(value):
    try:
        return int(value)
    except ValueError:
        try:
            if math.isinf(float(value)):
                return f"'{value}'"
            else:
                return float(value)
        except ValueError:
            return f"'{value}'"


def csv_to_sql_insert(csv_file_path, table_name, batch_size, max_file_size):
    current_directory = os.path.dirname(csv_file_path)
    output_dir = "{}/{}".format(current_directory, table_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        batch = []
        batch_count = 0
        file_count = 1
        current_file_size = 0
        sql_file_path = os.path.join(output_dir, f"{table_name}_part{file_count}.sql")

        with open(sql_file_path, 'w', encoding='utf-8') as sql_file:
            for row in reader:
                batch_row = {field: infer_data_type(value) for field, value in row.items()}
                batch.append(batch_row)
                batch_count += 1

                if batch_count >= batch_size:
                    insert_statement = generate_insert_statement(table_name, fieldnames, batch)

                    if max_file_size > 0:
                        current_file_size += len(insert_statement.encode('utf-8'))
                        current_file_size += len('\n'.encode('utf-8'))
                        if current_file_size > max_file_size:
                            sql_file.close()

                            file_count += 1
                            sql_file_path = os.path.join(output_dir, f"{table_name}_part{file_count}.sql")
                            sql_file = open(sql_file_path, 'w', encoding='utf-8')

                            sql_file.write(insert_statement + '\n')
                            current_file_size = len(insert_statement.encode('utf-8')) + len('\n'.encode('utf-8'))
                            batch = []
                            batch_count = 0
                        else:
                            sql_file.write(insert_statement + '\n')
                            batch = []
                            batch_count = 0
                    else:
                        sql_file.write(insert_statement + '\n')
                        batch = []
                        batch_count = 0

            # Write the last batch if it's less than batch_size
            if batch:
                insert_statement = generate_insert_statement(table_name, fieldnames, batch)
                sql_file.write(insert_statement + '\n')


def generate_insert_statement(table_name, fieldnames, batch):
    columns = ', '.join(fieldnames)
    values = ['({})'.format(', '.join(["{}".format(row[field]) for field in fieldnames])) for row in batch]
    values_str = ', '.join(values)
    return "INSERT INTO {} ({}) VALUES {};".format(table_name, columns, values_str)


if __name__ == "__main__":
    main()