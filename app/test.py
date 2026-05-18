import httpx

try:
    r = httpx.get("https://api-inference.huggingface.co/models/THUDM/chatglm2-6b")
    print(r.status_code)
except Exception as e:
    print(e)