import sys
import os

# 添加 libs 目录到 Python 路径
libs_path = os.path.join(os.path.dirname(__file__), "libs")
sys.path.insert(0, libs_path)

import sqlparse


def main():
    script_name, query = get_arg_from_cmd()
    formatted_sql = format_sql(query)
    # 输出结果
    print(formatted_sql)


def format_sql(query):
    print(f"[DEBUG] {query}", file=sys.stderr)
    
    # 解析并格式化
    try:
        formatted_sql = sqlparse.format(query, reindent=True, keyword_case="upper")
    except Exception as e:
        print(f"格式化失败: {e}")
        sys.exit(1)

    return formatted_sql


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