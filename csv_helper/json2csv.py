import csv
import json
import sys


def main():
    json_file_path, field_path = get_arg_from_cmd()
    json_str = read_file(json_file_path)
    data = json.loads(json_str)
    value = get_value_by_path(data, field_path)
    output_csv(value)


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
        json_file_path = args[1]
        print("json_file_path:", json_file_path)
        field_path = args[2]
        print("field_path:", field_path)
        return json_file_path, field_path
    else:
        print(f"Arguments Invalid. \n")
        print("用法：python <json2csv.py> <json_file_path> <field_path> \n")
        print("  json_file_path  所需转换的json文件路径")
        print("  field_path      对象数组所在的属性路径，如layer1.layer2.list")
        print('''
    {
        "layer1": {
            "layer2": {
                "list": [
                    {
                        "column_a": 123,
                        "column_b": "xxx",
                        "column_c": null
                    },
                    {
                        "column_a": 456,
                        "column_b": "yyy",
                        "column_c": ""
                    }
                ]
            }
        }
    }
        ''')
        sys.exit()


# 读取JSON文件的内容
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            print("File content:")
            print(content)
            print()
            return content

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except IOError as e:
        print(f"Error reading file: {e}")


# 根据路径获取JSON对象中的某个对象属性
def get_value_by_path(json_obj, field_path):
    keys = field_path.split('.')
    for key in keys:
        if key in json_obj:
            json_obj = json_obj[key]
        else:
            return None
    return json_obj


def output_csv(json_array):
    if json_array is None:
        print(f"json_array is None")
        return

    if not isinstance(json_array, list):
        print(f"value is not array. can not convert to CSV. please check the argument.")
        return

    if len(json_array) == 0:
        print(f"array is empty. can not convert to CSV.")
        return

    # 获取JSON对象的键作为CSV的列名
    column_names = json_array[0].keys()
    # 创建一个CSV文件
    with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=column_names)

        # 将列名写入CSV文件
        writer.writeheader()

        # 将JSON对象的值写入CSV文件
        for row in json_array:
            writer.writerow(row)
    print("JSON对象已成功转换为CSV格式并保存到output.csv文件中。")


if __name__ == "__main__":
    main()
