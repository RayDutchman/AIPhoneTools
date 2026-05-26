#!/usr/bin/env python3
"""
Termux Agent Server API 测试脚本
用于快速验证 API 基础功能，不依赖 Chatbox
"""
import requests
import json
import time
import sys

BASE_URL = "http://192.168.100.115:5846"
CONV_ID = f"test-{int(time.time())}"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_models_endpoint():
    """测试 /v1/models 端点（连接检测）"""
    print_section("测试 1: 连接检测 (/v1/models)")
    try:
        resp = requests.get(f"{BASE_URL}/v1/models", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ 连接成功")
            print(f"  可用模型: {data['data'][0]['id']}")
            return True
        else:
            print(f"✗ 失败: HTTP {resp.status_code}")
            return False
    except Exception as e:
        print(f"✗ 连接失败: {e}")
        return False

def test_simple_chat():
    """测试普通对话（不调用工具）"""
    print_section("测试 2: 普通对话")
    payload = {
        "model": "claude-sonnet-4-6",
        "messages": [{"role": "user", "content": "你好，用一句话介绍你自己"}],
        "stream": False,
        "conversation_id": CONV_ID
    }
    try:
        resp = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload, timeout=30)
        result = resp.json()
        content = result["choices"][0]["message"].get("content", "")
        print(f"✓ 回复: {content[:100]}...")
        return True
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_tool_call():
    """测试工具调用"""
    print_section("测试 3: 工具调用 (echo 命令)")
    payload = {
        "model": "claude-sonnet-4-6",
        "messages": [{"role": "user", "content": f"执行命令: echo test-{int(time.time())}"}],
        "stream": False,
        "conversation_id": CONV_ID
    }
    try:
        resp = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload, timeout=60)
        result = resp.json()
        content = result["choices"][0]["message"].get("content", "")
        print(f"✓ 回复: {content[:200]}...")
        if "test-" in content:
            print(f"✓ 工具执行成功（输出包含时间戳）")
            return True
        else:
            print(f"⚠ 工具可能未执行")
            return False
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_memory():
    """测试 session 记忆"""
    print_section("测试 4: Session 记忆")
    payload = {
        "model": "claude-sonnet-4-6",
        "messages": [{"role": "user", "content": "你刚才执行了什么命令？"}],
        "stream": False,
        "conversation_id": CONV_ID
    }
    try:
        resp = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload, timeout=30)
        result = resp.json()
        content = result["choices"][0]["message"].get("content", "")
        print(f"✓ 回复: {content[:200]}...")
        if "echo" in content.lower() or "test-" in content:
            print(f"✓ AI 记得之前的对话")
            return True
        else:
            print(f"⚠ AI 可能失忆了")
            return False
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_read_file():
    """测试读文件"""
    print_section("测试 5: 读文件")
    payload = {
        "model": "claude-sonnet-4-6",
        "messages": [{"role": "user", "content": "读取 server_stream.py 的前 3 行"}],
        "stream": False,
        "conversation_id": f"test-read-{int(time.time())}"
    }
    try:
        resp = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload, timeout=60)
        result = resp.json()
        content = result["choices"][0]["message"].get("content", "")
        print(f"✓ 回复: {content[:200]}...")
        if "import" in content:
            print(f"✓ 文件读取成功")
            return True
        else:
            print(f"⚠ 文件内容可能未返回")
            return False
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def test_write_file():
    """测试写文件"""
    print_section("测试 6: 写文件")
    test_content = f"test-{int(time.time())}"
    payload = {
        "model": "claude-sonnet-4-6",
        "messages": [{"role": "user", "content": f"创建文件 test_output.txt，内容是 {test_content}"}],
        "stream": False,
        "conversation_id": f"test-write-{int(time.time())}"
    }
    try:
        resp = requests.post(f"{BASE_URL}/v1/chat/completions", json=payload, timeout=60)
        result = resp.json()
        content = result["choices"][0]["message"].get("content", "")
        print(f"✓ 回复: {content[:200]}...")
        if "成功" in content or "已保存" in content:
            print(f"✓ 文件写入成功")
            return True
        else:
            print(f"⚠ 文件可能未创建")
            return False
    except Exception as e:
        print(f"✗ 失败: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("  Termux Agent Server - 自动化测试")
    print("="*60)
    print(f"  目标服务器: {BASE_URL}")
    print(f"  测试会话 ID: {CONV_ID}")
    print("="*60)
    
    results = []
    results.append(("连接检测", test_models_endpoint()))
    results.append(("普通对话", test_simple_chat()))
    results.append(("工具调用", test_tool_call()))
    results.append(("Session 记忆", test_memory()))
    results.append(("读文件", test_read_file()))
    results.append(("写文件", test_write_file()))
    
    print_section("测试总结")
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status}  {name}")
    
    print(f"\n  总计: {passed}/{total} 通过")
    
    if passed == total:
        print("\n  🎉 所有测试通过！")
        sys.exit(0)
    else:
        print(f"\n  ⚠️  {total - passed} 个测试失败，需要修复")
        sys.exit(1)

if __name__ == "__main__":
    main()
