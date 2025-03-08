import sys


def main():
    script_name, query, mode = get_arg_from_cmd()
    result = case_convert(query, mode)
    # 输出结果
    print(f"[DEBUG] {result}", file=sys.stderr)
    print(result, end='')


def case_convert(query, mode):
    print(f"[DEBUG] {query} {mode}", file=sys.stderr)

    if mode == "upper":
        return query.upper()
    elif mode == "lower":
        return query.lower()
    else:
        return query


def get_arg_from_cmd():
    # 获取命令行参数
    args = sys.argv
    
    if len(sys.argv) != 3:
        exit(0)

    # 获取第一个参数（脚本名称）
    script_name = args[0]
    mode = args[1]
    query = args[2]

    return script_name, query, mode


if __name__ == "__main__":
    main()