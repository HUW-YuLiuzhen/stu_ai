import httpx

# 测试能否连通百炼域名
try:
    # 这里的 URL 是百炼的标准域名
    response = httpx.get("https://dashscope.aliyuncs.com", timeout=5)
    print(f"✅ 网络通畅！状态码: {response.status_code}")
except Exception as e:
    print(f"❌ 连接失败: {e}")
    print("提示：请检查是否开启了代理软件但未运行，或者防火墙拦截。")