import re
import sys

from datetime import datetime, timezone, timedelta

import json

class AlfredScriptResultItems:
    def __init__(self):
        self.items = []

    def add_item(self, uid='', title='', subtitle='', arg='', icon_path=''):
        """添加一个新的条目到项目列表中"""
        item = {
            # "uid": uid,
            "title": title,
            "subtitle": subtitle,
            "arg": arg,
            "skipknowledge": True,
            "icon": {
                "path": icon_path
            }
        }
        self.items.append(item)

    def to_json(self):
        """生成包含所有条目的 JSON 字符串"""
        return json.dumps({"items": self.items}, indent=4)


def main():
    script_name, query = get_arg_from_cmd()
    result = process_timestamp(query)
    # 输出结果
    print(result)


def is_valid_timestamp(value):
    s = str(value)

    if s == "" or s == "now":
        return True

    pattern = re.compile(r'^[+-]\d+d$')
    if bool(pattern.fullmatch(s)):
        return True


    # 正则表达式匹配格式：整数部分（可选小数点后3位或6位）
    pattern = r'^(\d+)(?:\.(\d{3}|\d{6}))?$'

    if not re.fullmatch(pattern, s):
        return False

    # 拆分整数和小数部分
    parts = s.split('.')
    integer_part = int(parts[0])

    # 检查整数范围（0 <= timestamp <= 2^63 - 1）
    if integer_part < 0 or integer_part > (2 ** 63 - 1):
        return False

    # 检查小数部分（若有）
    if len(parts) > 1:
        decimal_part = parts[1]
        if not decimal_part.isdigit():
            return False

    return True


def process_timestamp(query):
    print(f"[DEBUG] {query}", file=sys.stderr)

    if not is_valid_timestamp(query):
        exit(0)

    dt = get_time_from_timestamp(query)

    result_items = AlfredScriptResultItems()
    result_items.add_item(title=dt.strftime("%Y-%m-%d"), subtitle="YYYY-MM-DD", arg=dt.strftime("%Y-%m-%d"))
    result_items.add_item(title=dt.strftime("%Y-%m-%d %H:%M:%S"), subtitle="YYYY-MM-DD HH:MM:SS", arg=dt.strftime("%Y-%m-%d %H:%M:%S"))

    rfc3339_base = dt.strftime('%Y-%m-%dT%H:%M:%S')
    tz = dt.strftime('%z')
    formatted_timezone = tz[:3] + ':' + tz[3:]
    rfc3339_format = rfc3339_base + formatted_timezone
    result_items.add_item(title=rfc3339_format, subtitle="RFC3339", arg=rfc3339_format)

    milli_format = dt.strftime('.%f')[:4]
    rfc3339milli_format = rfc3339_base + milli_format + formatted_timezone
    result_items.add_item(title=rfc3339milli_format, subtitle="RFC3339Milli", arg=rfc3339milli_format)

    rfc3339milli_format = dt.strftime('%Y-%m-%dT%H:%M:%S.%f') + formatted_timezone
    result_items.add_item(title=rfc3339milli_format, subtitle="RFC3339Nano", arg=rfc3339milli_format)

    local_tz = datetime.now().astimezone().tzinfo
    date_difference = dt.date() - datetime.now(local_tz).date()
    day_diff = str(date_difference.days)
    result_items.add_item(title=day_diff, subtitle="target - today", arg=day_diff)

    return result_items.to_json()


def get_time_from_timestamp(query):
    if query == "" or query == "now":
        local_tz = datetime.now().astimezone().tzinfo
        return datetime.now(local_tz)

    pattern = re.compile(r'^[+-]\d+d$')
    if bool(pattern.fullmatch(query)):
        local_tz = datetime.now().astimezone().tzinfo
        return datetime.now(local_tz) + timedelta(days=int(query[:-1]))

    try:
        t = float(query)
    except ValueError:
        raise ValueError(f"Invalid input format: {query}")

    if t > 253402271999000:
        t = t / (1000 * 1000)
    elif t > 253402271999:
        t = t / 1000

    local_tz = datetime.now().astimezone().tzinfo
    dt = datetime.fromtimestamp(t, local_tz)
    return dt


def get_arg_from_cmd():
    # 获取命令行参数
    args = sys.argv

    if len(sys.argv) == 1:
        return args[0], ""

    if len(sys.argv) != 2:
        exit(0)

    # 获取第一个参数（脚本名称）
    script_name = args[0]
    query = args[1]
    
    return script_name, query


if __name__ == "__main__":
    main()