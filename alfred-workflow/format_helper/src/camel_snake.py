import re
import sys


def main():
    script_name, query = get_arg_from_cmd()
    result = camel_snake_convert(query)
    # 输出结果
    print(f"[DEBUG] {result}", file=sys.stderr)
    print(result, end='')


def camel_snake_convert(query):
    print(f"[DEBUG] {query}", file=sys.stderr)

    if is_snake_case(query):
        return snake_to_camel_regex(query)
    elif is_camel_or_lower_camel(query):
        return camel_to_snake(query)
    else:
        return query

def is_camel_or_lower_camel(s):
    # 正则表达式模式：
    # ^[A-Za-z]          : 首字母必须是大写或小写字母
    # [a-zA-Z0-9]*       : 后跟零个或多个字母/数字
    # ([A-Z][a-zA-Z0-9]*)*: 后续每个单词必须以大写字母开头（可重复多次）
    # $                  : 字符串结尾
    pattern = r'^[A-Za-z][a-zA-Z0-9]*([A-Z][a-zA-Z0-9]*)*$'
    return bool(re.fullmatch(pattern, s))

def is_snake_case(s):
    pattern = r'^[a-z]+(_[a-z]+)*$'
    return bool(re.fullmatch(pattern, s))

def snake_to_camel_regex(s):
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), s)

def camel_to_snake(s):
    # 匹配非首字母的大写字母，并在其前插入下划线
    s1 = re.sub(r'(?<!^)(?=[A-Z])', '_', s)
    return s1.lower()

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