#!/usr/bin/env python3
"""
项目功能测试
"""

import os
import pandas as pd
import yaml

def test_directories():
    """测试目录是否存在"""
    print("📁 测试目录结构...")
    required_dirs = [
        'data/genomes/passer_domesticus',
        'data/genomes/bombyx_mori',
        'src',
        'notebooks',
        'config',
        'results/tables',
        'results/figures'
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✅ {directory}")
        else:
            print(f"  ❌ {directory} - 缺失")
            all_exist = False
    
    return all_exist

def test_config():
    """测试配置文件"""
    print("\n⚙️ 测试配置文件...")
    try:
        with open('config/species.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        if 'species' in config:
            print(f"  ✅ 配置文件正常")
            print(f"     麻雀: {config['species']['sparrow']['name']}")
            print(f"     蝴蝶: {config['species']['butterfly']['name']}")
            return True
        else:
            print("  ❌ 配置文件格式错误")
            return False
    except Exception as e:
        print(f"  ❌ 读取配置文件失败: {e}")
        return False

def test_analysis_script():
    """测试分析脚本"""
    print("\n🐍 测试分析脚本...")
    try:
        # 导入分析脚本
        import sys
        sys.path.append('src')
        
        # 直接运行脚本
        import subprocess
        result = subprocess.run(['python', 'src/find_orthologs.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ 分析脚本运行成功")
            print("     输出内容:")
            for line in result.stdout.split('\n')[:5]:
                if line: print(f"       {line}")
            return True
        else:
            print(f"  ❌ 分析脚本运行失败")
            print(f"     错误: {result.stderr}")
            return False
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_results():
    """测试结果文件"""
    print("\n📊 测试结果文件...")
    results_file = 'results/tables/orthologs.csv'
    
    if os.path.exists(results_file):
        try:
            df = pd.read_csv(results_file)
            print(f"  ✅ 结果文件存在，包含 {len(df)} 行数据")
            print("     前3行数据:")
            print(df.head(3).to_string())
            return True
        except Exception as e:
            print(f"  ❌ 读取结果文件失败: {e}")
            return False
    else:
        print(f"  ❌ 结果文件不存在: {results_file}")
        return False

def main():
    print("=" * 60)
    print("麻雀与蝴蝶飞行基因分析项目测试")
    print("=" * 60)
    
    tests = [
        ("目录结构", test_directories),
        ("配置文件", test_config),
        ("分析脚本", test_analysis_script),
        ("结果文件", test_results)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🧪 测试: {test_name}")
        success = test_func()
        results.append((test_name, success))
    
    # 总结
    print("\n" + "=" * 60)
    print("测试结果总结:")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n📈 通过率: {passed}/{total} ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！项目可以正常使用。")
        print("下一步:")
        print("  1. 添加真实数据到 data/genomes/ 目录")
        print("  2. 修改 src/find_orthologs.py 进行实际分析")
        print("  3. 运行 python src/find_orthologs.py 开始分析")
    else:
        print("\n⚠️  部分测试失败，请检查项目设置。")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
