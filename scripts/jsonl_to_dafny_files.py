import argparse
import json
import os
from pathlib import Path


def extract_code_from_user(message: str) -> str:
    """从 user 提示中抽取 Dafny 代码块（在说明文字之后的部分）。"""
    # 假设说明文字后紧跟着代码，中间只有一个换行
    parts = message.split("\n", 1)
    if len(parts) == 2:
        return parts[1].strip("\n")
    return message


def build_dafny_code(user_msg: str, assistant_msg: str) -> str:
    code = extract_code_from_user(user_msg)
    # assistant_msg 本身就是一整行 requires ...
    requires_line = assistant_msg.strip()
    # 在方法/函数签名和 ensures 之间插入 requires
    lines = code.splitlines()
    out_lines = []
    inserted = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        out_lines.append(line)
        # 在第一条 ensures 之前插入 requires
        if not inserted and stripped.startswith("ensures"):
            indent = line[: len(line) - len(stripped)]
            out_lines.insert(len(out_lines) - 1, f"{indent}{requires_line}")
            inserted = True
    if not inserted:
        # 如果没有 ensures，就简单地在首行之后插入
        if lines:
            first = lines[0]
            indent = first[: len(first) - len(first.lstrip())]
            out_lines = [first, f"{indent}{requires_line}"] + lines[1:]
        else:
            out_lines = [requires_line]
    return "\n".join(out_lines) + "\n"


def convert(jsonl_path: Path, out_dir: Path, prefix: str = "entry_") -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    with jsonl_path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            messages = obj.get("messages", [])
            user_msg = next((m["content"] for m in messages if m.get("role") == "user"), None)
            assistant_msg = next((m["content"] for m in messages if m.get("role") == "assistant"), None)
            if not user_msg or not assistant_msg:
                continue
            dafny_code = build_dafny_code(user_msg, assistant_msg)
            out_path = out_dir / f"{prefix}{idx}.dfy"
            with out_path.open("w", encoding="utf-8") as wf:
                wf.write(dafny_code)
            print(f"Wrote {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Convert JSONL dataset to Dafny .dfy files")
    parser.add_argument("--jsonl", type=str, default="data/precondition_dataset.jsonl", help="Path to JSONL dataset")
    parser.add_argument("--out-dir", type=str, default="src", help="Output directory for .dfy files")
    parser.add_argument("--prefix", type=str, default="entry_", help="Filename prefix")
    args = parser.parse_args()

    jsonl_path = Path(args.jsonl)
    out_dir = Path(args.out_dir)
    convert(jsonl_path, out_dir, args.prefix)


if __name__ == "__main__":
    main()
