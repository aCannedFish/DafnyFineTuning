#!/usr/bin/env python3
"""将一个完整且带有正确前/后置条件的 Dafny 文件 (*.dfy) 解析为训练条目并追加到 data/dataset.jsonl。

用法:
  python3 scripts/extract_and_append.py path/to/file.dfy

默认会把新条目追加到 `data/dataset.jsonl`（如果不存在则创建）。

行为说明:
- 从输入文件中提取所有顶层以 `requires` 开头的行（忽略以 // 注释起始的行与块注释内的内容），作为答案（assistant 内容）。
- 把去掉这些 `requires` 行后的代码作为提示（user 内容），并在前面加上固定问句：
  "给下面的Dafny代码生成前置条件pre-condition，不可以修改函数体和后置条件:\n"。
- 如果没有找到任何 `requires`，assistant 内容将为 `requires true`。
"""

from __future__ import annotations
import argparse
import json
import os
import re
import sys


def extract_requires_and_strip(text: str):
    """返回 (requires_list, code_without_requires).

    简单规则：逐行扫描，忽略以 `//` 开头的行和处于 `/* ... */` 块注释内的行；
    对于非注释行，如果在行首（允许前导空格）匹配 `requires`，则把该行的后半部分视为一个前置条件并从代码中去除。
    """
    lines = text.splitlines()
    out_lines = []
    requires = []
    in_block = False
    for line in lines:
        stripped = line.lstrip()
        # 块注释开始/结束的简单处理
        if not in_block and stripped.startswith('/*'):
            in_block = True
            out_lines.append(line)
            if '*/' in line:
                in_block = False
            continue
        if in_block:
            out_lines.append(line)
            if '*/' in line:
                in_block = False
            continue

        # 单行注释，保留
        if stripped.startswith('//'):
            out_lines.append(line)
            continue

        m = re.match(r"\s*requires\b(.*)$", line)
        if m:
            cond = m.group(1).strip()
            # 去掉结尾分号（如果存在）和多余空格
            cond = cond.rstrip(';').strip()
            if cond:
                requires.append(cond)
            else:
                # 空的 requires 行，忽略
                pass
            # 不把该行写入 out_lines，从而实现去除
        else:
            out_lines.append(line)

    code = '\n'.join(out_lines)
    return requires, code


def build_jsonl_entry(code_without_requires: str, requires_list: list[str]):
    prompt = (
        "给下面的Dafny代码生成前置条件pre-condition，不可以修改函数体和后置条件:\n"
        + code_without_requires
    )
    if requires_list:
        # 将多个 requires 条件合并为一个 requires 表达式，格式与已有数据集保持一致
        cleaned = [r for r in (s.strip() for s in requires_list) if r]
        assistant = 'requires ' + ' && '.join(cleaned)
    else:
        assistant = 'requires true'

    obj = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant},
        ]
    }
    return json.dumps(obj, ensure_ascii=False)


def append_to_dataset(dataset_path: str, line: str):
    os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
    # 以追加模式写入新条目，保持文件末尾有换行
    with open(dataset_path, 'a', encoding='utf-8') as f:
        f.write(line)
        f.write('\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Extract requires from Dafny .dfy and append JSONL entry to dataset')
    parser.add_argument('dfy', help='input Dafny .dfy file')
    parser.add_argument('--out', default='data/dataset.jsonl', help='dataset jsonl file to append to (default: data/dataset.jsonl)')
    parser.add_argument('--dry-run', action='store_true', help='print entry to stdout instead of appending')
    args = parser.parse_args(argv)

    if not os.path.isfile(args.dfy):
        print('Input file not found:', args.dfy, file=sys.stderr)
        return 2

    with open(args.dfy, 'r', encoding='utf-8') as f:
        text = f.read()

    requires_list, code_without_requires = extract_requires_and_strip(text)
    entry = build_jsonl_entry(code_without_requires, requires_list)

    if args.dry_run:
        print(entry)
    else:
        append_to_dataset(args.out, entry)
        print(f'Appended 1 entry to {args.out}')


if __name__ == '__main__':
    raise SystemExit(main())
