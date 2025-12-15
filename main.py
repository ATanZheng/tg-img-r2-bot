import uuid
import datetime
import boto3
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
)
from config import *

# ================= 日志 =================
def log(tag, msg):
    ts = datetime.datetime.utcnow().isoformat()
    print(f"[{ts}][{tag}] {msg}", flush=True)

# ================= R2 客户端 =================
s3 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name="auto",
)

# ================= 工具函数 =================
def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_USER_IDS

def gen_object_key(ext: str) -> str:
    date = datetime.datetime.utcnow().strftime("%Y/%m/%d")
    name = uuid.uuid4().hex
    return f"{date}/{name}.{ext}"

def guess_content_type(ext: str) -> str:
    ext = ext.lower()
    if ext in ("jpg", "jpeg"):
        return "image/jpeg"
    if ext == "png":
        return "image/png"
    if ext == "webp":
        return "image/webp"
    return "application/octet-stream"

# ================= Telegram 处理 =================
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # 管理员校验
    if not is_admin(user.id):
        log("DENY", f"user {user.id} blocked")
        return

    photo = update.message.photo[-1]
    log("TG", f"receive photo from admin {user.id}")

    await context.bot.send_message(chat_id, "📤 正在上传到 R2...")

    try:
        # 1. 下载图片（PTB 官方方式）
        file = await context.bot.get_file(photo.file_id)
        data = await file.download_as_bytearray()

        # 2. 推断文件后缀
        ext = "jpg"
        if "." in file.file_path:
            ext = file.file_path.rsplit(".", 1)[-1]

        content_type = guess_content_type(ext)
        object_key = gen_object_key(ext)

        # 3. 上传到 Cloudflare R2
        s3.put_object(
            Bucket=R2_BUCKET,
            Key=object_key,
            Body=data,
            ContentType=content_type,
        )

        final_url = f"{PUBLIC_BASE_URL}/{object_key}"
        log("OK", f"upload success {final_url}")

        msg = (
            f"Direct Link\n{final_url}\n\n"
            f"Markdown\n![Image]({final_url})\n\n"
            f"BBCode\n[img]{final_url}[/img]"
        )

        await context.bot.send_message(
            chat_id,
            msg,
            disable_web_page_preview=True,
        )

    except Exception as e:
        log("ERROR", repr(e))
        await context.bot.send_message(chat_id, "❌ 上传失败")

# ================= 主入口 =================
def main():
    log("BOOT", "starting telegram bot")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    app.run_polling()

if __name__ == "__main__":
    main()

