#!/usr/bin/env python3
"""
结果验证脚本
用于自动化验证任务产出是否符合预期
兼容：脚本独立运行、交互式环境（Jupyter/IDLE）、任意工作目录执行
"""

import json
import os
import sys
from pathlib import Path

# ========== 自动定位项目根目录 ==========
def set_project_root():
    """
    将当前工作目录切换到项目根目录（即包含 artifacts/ 和 others/ 的上级目录）。
    兼容 __file__ 未定义的情况（交互式环境）。
    """
    try:
        # 当作为脚本运行时
        script_path = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))
    except NameError:
        # 交互式环境：尝试从当前工作目录向上查找，直到找到 artifacts 文件夹
        current = os.getcwd()
        while True:
            if os.path.isdir(os.path.join(current, 'artifacts')):
                project_root = current
                break
            parent = os.path.dirname(current)
            if parent == current:  # 已到根目录
                project_root = current
                break
            current = parent
    os.chdir(project_root)
    return project_root

project_root = set_project_root()
# ========================================

def validate_number(value, expected, tolerance):
    """验证数值是否在允许误差范围内"""
    return abs(value - expected) <= tolerance

def validate_file_exists(file_path):
    """验证文件是否存在"""
    return os.path.exists(file_path)

def validate_string_contains(text, substring):
    """验证文本是否包含特定子串"""
    return substring.lower() in text.lower()

def main():
    print("正在验证任务产出物...")
    print(f"当前工作目录: {os.getcwd()}")

    # 读取结果文件
    results_path = Path("artifacts/final_results.json")
    if not results_path.exists():
        print("❌ 结果文件不存在")
        return False

    with open(results_path, 'r', encoding='utf-8') as f:
        results = json.load(f)

    # 验证1: 光子能量
    classical_energy = results["calculated_parameters"]["photon_energies"]["classical_signal_J"]
    quantum_energy = results["calculated_parameters"]["photon_energies"]["quantum_signal_J"]

    energy_check1 = validate_number(classical_energy, 1.282e-19, 0.01e-19)
    energy_check2 = validate_number(quantum_energy, 1.537e-19, 0.01e-19)

    # 验证2: 数值孔径
    na = results["calculated_parameters"]["fiber_optics"]["numerical_aperture"]
    na_check = validate_number(na, 0.171, 0.01)

    # 验证3: SpRS噪声率
    noise = results["calculated_parameters"]["noise_analysis"]["sprs_noise_rate_counts_per_s_per_mW"]
    noise_check = validate_number(noise, 79.0, 5.0)

    # 验证4: 文件存在
    file_check1 = validate_file_exists("artifacts/noise_vs_power.png")
    file_check2 = validate_file_exists("artifacts/analysis_report.txt")
    file_check3 = validate_file_exists("artifacts/sprs_results.json")
    file_check4 = validate_file_exists("artifacts/final_results.json")

    # 验证5: 报告内容
    if file_check2:
        with open("artifacts/analysis_report.txt", 'r', encoding='utf-8') as f:
            report = f.read()
        report_check = validate_string_contains(report, "量子-经典共传")
    else:
        report_check = False

    # 汇总结果
    checks = [
        ("经典光子能量", energy_check1),
        ("量子光子能量", energy_check2),
        ("数值孔径", na_check),
        ("SpRS噪声率", noise_check),
        ("噪声图表文件", file_check1),
        ("分析报告文件", file_check2),
        ("SpRS结果文件", file_check3),
        ("最终结果文件", file_check4),
        ("报告内容", report_check)
    ]

    print("\n验证结果:")
    all_passed = True
    for name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"  {name}: {status}")
        if not passed:
            all_passed = False

    # 输出验证文件
    validation_result = {
        "task_id": results.get("task_id", "phys-optics-20250320-abcd"),
        "validation_time": "2025-03-20T11:00:00Z",  # 建议动态生成时间
        "all_passed": all_passed,
        "details": {name: passed for name, passed in checks}  # 修正字典推导
    }

    # 确保 artifacts 目录存在
    os.makedirs("artifacts", exist_ok=True)

    with open("artifacts/validation_result.json", 'w', encoding='utf-8') as f:
        json.dump(validation_result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ 验证结果已保存至 {os.path.abspath('artifacts/validation_result.json')}")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)