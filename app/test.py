import pandas as pd
import json
import os
from pathlib import Path
import math

# ========= 路径（修正） =========
BASE_DIR = Path(__file__).resolve().parent

xlsx_path = Path(r"C:/PyCharm/code/bore-connect/app/knowledge/faults.xlsx")
output_path = Path(r"C:/PyCharm/code/bore-connect/app/knowledge/faults.json")
tmp_path = output_path.with_suffix(".json.tmp")


# ========= 工具：安全判断 NaN =========
def is_valid(v):
    if v is None:
        return False
    if isinstance(v, float) and math.isnan(v):
        return False
    v = str(v).strip()
    return v.lower() != "nan" and v != ""


# ========= 读取 Excel =========
df = pd.read_excel(xlsx_path)
df.columns = [c.strip() for c in df.columns]


# ========= 构建结构 =========
result = {}

for _, row in df.iterrows():
    fault_type = row.get("故障类型")
    status = row.get("设备目前状态")
    desc = row.get("故障描述")
    cause = row.get("故障原因分析")

    if not all(map(is_valid, [fault_type, status, desc, cause])):
        continue

    fault_type = str(fault_type).strip()
    status = str(status).strip()

    result.setdefault(fault_type, {})
    result[fault_type].setdefault(status, [])

    item = {
        "fault": str(desc).strip(),
        "cause": str(cause).strip()
    }

    if item not in result[fault_type][status]:
        result[fault_type][status].append(item)


# ========= 原子写入（核心升级） =========
def atomic_write_json(data, target_path: Path, tmp_path: Path):
    # 写临时文件
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())  # 强制落盘

    # 原子替换
    os.replace(tmp_path, target_path)


atomic_write_json(result, output_path, tmp_path)

print(f"转换完成（原子写入）: {output_path}")