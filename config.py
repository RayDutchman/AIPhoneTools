"""
服务器配置常量
修改此文件后重启 server.py 生效。
"""
import os

# ==== 文件路径 ====
DOWNLOAD_DIR            = os.path.expanduser("~")
GLOBAL_MEMORY_PATH      = os.path.join(DOWNLOAD_DIR, "memory.md")
TTS_STATE_PATH          = os.path.join(DOWNLOAD_DIR, "tts_state.json")
MODELS_CONFIG_PATH      = os.path.join(DOWNLOAD_DIR, "models_config.json")

# ==== 工具输出 ====
TOOL_OUTPUT_MAX_CHARS       = 8000   # 工具返回内容超出此字符数时截断
SMART_TRUNCATE_TAIL_RATIO   = 0.3    # _smart_truncate：尾部保留比例

# ==== 文件读写限制 ====
FILE_READ_MAX_BYTES     = 500 * 1024   # read_phone_file：单文件读取上限（字节）
FILE_WRITE_MAX_BYTES    = 1 * 1024 * 1024  # write_phone_file：单次写入上限（字节）

# ==== 命令执行 ====
COMMAND_TIMEOUT_SECS        = 300  # execute_local_command：shell 命令超时（秒）
TERMUX_API_TIMEOUT_SECS     = 30   # termux-* 命令超时（秒），IPC 调用要么快速响应要么失败

# ==== 工具调用轮次 ====
MAX_TOOL_ROUNDS         = 50    # 最大工具调用轮数
BUDGET_SECONDS          = 1200  # 请求总时间预算（秒），超出后停止调用工具
KEEPALIVE_INTERVAL_SECS = 5     # 工具执行期间 SSE 心跳间隔（秒）

# ==== LLM 请求超时 ====
LLM_SYNC_TIMEOUT_SECS       = 120   # call_llm_sync：非流式请求超时（秒）
LLM_STREAM_CONNECT_TIMEOUT  = 30    # call_llm_stream：连接超时（秒）
LLM_STREAM_READ_TIMEOUT     = 300   # call_llm_stream：读取超时（秒）
FETCH_MODELS_TIMEOUT_SECS   = 15    # 启动时拉取模型列表的超时（秒）

# ==== TTS ====
TTS_SPEAK_TIMEOUT_SECS  = 120   # termux-tts-speak 单句最大等待时间（秒）

# ==== 长期记忆（memory.md）====
MEMORY_READ_MAX_CHARS   = 8000  # 每次请求注入的 memory.md 最大字符数
MEMORY_PRINTABLE_RATIO  = 0.8   # 低于此可打印字符比例时跳过加载

# ==== 模型默认值 ====
DEFAULT_MODEL_FALLBACK      = "claude-sonnet-4-6"  # models_config.json 缺失时的兜底模型
SYNTHETIC_MODEL_MAX_TOKENS  = 8192  # 未在配置中找到的模型的 max_tokens 默认值

# ==== Flask 服务器 ====
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5846

# ==== 启动提示 ====
STARTUP_AUTO_CONFIRM_SECS = 10  # 启动配置确认界面自动确认等待时间（秒）
