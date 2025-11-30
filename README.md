# DafnyFineTuning

## Part1 项目说明

本项目旨在通过微调语言模型，使其能够根据给定的 Dafny 方法体代码，生成正确的前置条件（requires 子句）/循环不变式（invariant 子句）[目前未实现]。项目包含以下主要部分：

### data/

存放用于训练大模型的数据集，格式为 JSONL，每行包含一个训练样本，结构形如：

```json

{"messages": [{"role": "system", "content": "You are a helpful assistant"}, {"role": "user", "content": "给下面的Dafny代码生成前置条件pre-condition，不可以修改函数体和后置条件:\nmethod func(x: int) returns (y: int)\n  ensures x < 0 ==> y == -x\n{\n  y:= x + 1;\n}"}, {"role": "assistant", "content": "requires x >= 0"}]}
```

### scripts/

存放用于生成和转换数据集的脚本，以及验证 Dafny 源文件的脚本。详见下文“Part2 DafnyFineTuning 脚本说明”部分。

### src/

存放从数据集中还原出来的 Dafny 源文件，每个样本对应一个 `.dfy` 文件，命名格式为 `entry_{index}.dfy`。

## Part2 DafnyFineTuning 脚本说明

scripts下的脚本用于生成 / 转换数据集，并验证 Dafny 源文件。

### 环境准备

建议使用 Python 3.8+ 和 Dafny CLI：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

确保 `dafny` 命令可用：

```bash
dafny --version
```

---

### scripts/extract_and_append.py

**用途：**

- 从单个 `.dfy` 文件里抽取前置条件，生成一条 JSONL 训练样本并追加到数据集。

**行为：**

- 把顶层 `requires` 行收集为答案（assistant）。
- 去掉这些 `requires` 后的 Dafny 代码，加上中文提示，作为 prompt（user）。

**使用示例：**

```bash
# 仅打印，不写入文件
python3 scripts/extract_and_append.py path/to/example.dfy --dry-run

# 追加到默认数据文件 data/dataset.jsonl
python3 scripts/extract_and_append.py path/to/example.dfy

# 指定数据集输出文件
python3 scripts/extract_and_append.py path/to/example.dfy --out data/my_dataset.jsonl
```

---

### scripts/jsonl_to_dafny_files.py

**用途：**

- 把 JSONL 数据集中的每条样本还原成一个 `.dfy` 文件（例如 `src/entry_1.dfy`）。

**行为：**

- 从 user 内容里提取 Dafny 代码。
- 在第一条 `ensures` 之前插入 assistant 的 `requires ...`。

**使用示例：**

```bash
python3 scripts/jsonl_to_dafny_files.py \
  --jsonl data/precondition_dataset.jsonl \
  --out-dir src \
  --prefix entry_
```

---

### scripts/run_all_dafny.py

**用途：**

- 批量跑 `dafny run src/*.dfy`，检查所有样本是否能通过验证。
- 结束时调用 `scripts/clean_build.sh` 清理 Dafny 生成的 C# 文件和编译输出。

**使用示例：**

```bash
python3 scripts/run_all_dafny.py
```

---

### scripts/clean_build.sh

**用途：**

- 清理 Dafny 生成的中间产物，保持 `src/` 目录干净。

**当前会删除：**

```bash
rm ./src/*.cs
rm ./src/*.csproj
rm ./src/*.json
rm ./src/*.dll
rm ./src/*.pdb
rm -rf ./src/bin
rm -rf ./src/obj
```

**使用示例：**

- 通常由 `scripts/run_all_dafny.py` 自动调用。
- 如需单独清理，可执行：

```bash
bash scripts/clean_build.sh
```
