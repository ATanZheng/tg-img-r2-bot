# ================= Telegram =================
TELEGRAM_BOT_TOKEN = "你的TelegramBotToken"

# 允许上传的 Telegram 用户 ID（管理员）
# 可以是一个或多个
ADMIN_USER_IDS = [
    123456789,   # 把这里换成你的 Telegram user_id
]

TELEGRAM_FILE_API = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}"

# ================= Cloudflare R2 ===========
R2_ACCESS_KEY_ID = "你的R2AccessKey"
R2_SECRET_ACCESS_KEY = "你的R2SecretKey"
R2_ACCOUNT_ID = "你的CloudflareAccountID"
R2_BUCKET = "tg-img"

R2_ENDPOINT = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

# ================= 对外 =====================
PUBLIC_BASE_URL = "https://img.yourdomain.com"
