import subprocess
from pathlib import Path


def run_dafny_on_file(dafny_path: Path, root: Path) -> int:
    print(f"\n=== Running: {dafny_path} ===")
    try:
        result = subprocess.run(
            ["dafny", "run", str(dafny_path)],
            cwd=str(root),
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print("dafny 命令未找到，请先安装 Dafny 并确保其在 PATH 中。")
        return 1

    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())

    if result.returncode == 0:
        print(f"[OK] {dafny_path}")
    else:
        print(f"[FAIL] {dafny_path} (exit code {result.returncode})")
    return result.returncode


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    src_dir = root / "src"
    dfy_files = sorted(src_dir.glob("*.dfy"))

    if not dfy_files:
        print(f"在 {src_dir} 下没有找到任何 .dfy 文件。")
        return

    overall_ok = True
    for f in dfy_files:
        code = run_dafny_on_file(f, root)
        if code != 0:
            overall_ok = False

    # 运行完成后调用清理脚本，删除 Dafny 生成的中间文件
    clean_script = root / "scripts" / "clean_build.sh"
    if clean_script.exists():
        print("\n开始清理 Dafny 生成的中间产物...")
        try:
            subprocess.run(["bash", str(clean_script)], cwd=str(root), check=False)
            print("清理完成。")
        except Exception as e:
            print(f"清理脚本执行失败: {e}")

    if overall_ok:
        print("\n所有 .dfy 文件均通过 Dafny 验证/运行。")
    else:
        print("\n部分 .dfy 文件存在错误，请根据上面的日志逐个修复。")


if __name__ == "__main__":
    main()
