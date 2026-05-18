import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

class Settings:
    # API Keys
    qwen_api_key: str = os.getenv("QWEN_API_KEY")
    deepseek_api_key: str = os.getenv("DEEPSEEK_API_KEY")

    
    # 调用参数
    api_timeout: int = int(os.getenv("API_TIMEOUT", 20))   # 默认 20s
    max_retry: int = int(os.getenv("MAX_RETRY", 1))
    cache_ttl: int = int(os.getenv("CACHE_TTL", 300))     # 默认 5分钟

# 实例化全局配置
settings = Settings()