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


def is_valid_date(value):
    return True


def process_timestamp(query):
    print(f"[DEBUG] {query}", file=sys.stderr)

    if not is_valid_date(query):
        exit(0)

    dt = get_time_from_date_str(query)

    epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)
    delta = dt - epoch
    total_seconds = delta.total_seconds()
    microseconds = dt.microsecond
    # 转换为毫秒级整数时间戳
    timestamp_ms = str(int(total_seconds * 1000) + (microseconds // 1000))

    result_items = AlfredScriptResultItems()
    seconds = str(int(total_seconds))
    result_items.add_item(title=seconds, subtitle="second", arg=seconds)
    result_items.add_item(title=timestamp_ms, subtitle="millisecond", arg=timestamp_ms)

    local_tz = datetime.now().astimezone().tzinfo
    date_difference = dt.date() - datetime.now(local_tz).date()
    day_diff = str(date_difference.days)
    result_items.add_item(title=day_diff, subtitle="target - today", arg=day_diff)

    return result_items.to_json()


def get_time_from_date_str(query):
    if query == "" or query == "now":
        local_tz = datetime.now().astimezone().tzinfo
        return datetime.now(local_tz)

    pattern = re.compile(r'^[+-]\d+d$')
    if bool(pattern.fullmatch(query)):
        local_tz = datetime.now().astimezone().tzinfo
        return datetime.now(local_tz) + timedelta(days=int(query[:-1]))

    # 定义所有可能的格式（包含时区、毫秒等）
    formats = [
        # 无时区
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S.%f",
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",

        # 带时区（%z支持±HH:MM格式）
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%a, %d %b %Y %H:%M:%S %Z",  # RFC 1123格式（如GMT）
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(query, fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"Invalid time format: {query}")


    # 处理时区：若datetime是naive（无时区），则使用本地时区
    if dt.tzinfo is None:
        local_tz = datetime.now().astimezone().tzinfo
        dt = dt.replace(tzinfo=local_tz)

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