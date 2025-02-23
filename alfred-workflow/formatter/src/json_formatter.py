import sys

import json


def main():
    script_name, query = get_arg_from_cmd()
    formatted_json = format_json(query)
    # 输出结果
    print(formatted_json)


def format_json(query):
    print(f"[DEBUG] {query}", file=sys.stderr)
    
    # 解析并格式化
    try:
        parsed_data = json.loads(query)
        formatted_json = json.dumps(parsed_data, indent=4, ensure_ascii=False, sort_keys=True)
    except Exception as e:
        print(f"格式化失败: {e}")
        sys.exit(1)

    return formatted_json


def get_arg_from_cmd():
    # 获取命令行参数
    args = sys.argv
    
    if len(sys.argv) != 2:
        exit(0)

    # 获取第一个参数（脚本名称）
    script_name = args[0]
    query = args[1]
    
    return script_name, query


if __name__ == "__main__":
    main()