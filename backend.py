import time
import os.path
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession

#######################TeleClinet##############################

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
print("Starting...")

APP_ID = 26900623
API_HASH = "Afbfca403b0065ddb164478305e2b9c9c"

# Define the initial channels to send messages from
FROM_CHANNEL = {
    -1001735360199: '@text_proxyy',
    -1001203971745: '@ProxyMTProto_tel',
    -1001395363861: '@ProxyMTProto',
    -1001559433070: '@proxydarsi',
    -1001171741566: '@IROproxy',
    -1001236837196: '@ProxyHagh',
    -1001091853463: '@TelMTProto',
    -1001344363795: '@MyPoroxy',
}

TO_CHANNEL = -1001933512018
SESSION = "1BJWap1wBuwR-2Vfgov2Y8mlPcUMryxniHegITaHa7P5NWCvsFiLhChiZ8ja03958MZlKive-TQzVGazD66hHR1OnURCxfWhSXf0wmMK2irBRp-aADUSQ158F9sBI__jOjfj4T_na_IGSL4tboGabKhkv_CQmzQCS3M6QlQ82uUhBbjuvs839h7hRjTl4VU1dTLn17_UxSmmmb2uMiaGnVEOL3f_-HtUBcOTkGwFxlcXL9UXivKYx9TlSF1xEBXLWZnujOeNBsHiyHAN_4JBYOeF73-rZ5tAJykf0vv_C_41xqb0I22cGLyc2jl0oM1hI6bmW-shtw-Sr83-bwo8xSnIHGyDBGeg="
TO = [TO_CHANNEL]

log_file = "message_log.txt"

last_sent_time = None
sent_message_count = 0
# Define the maximum number of messages sent in an hour
MAX_MESSAGES_PER_HOUR = 10
# Set the limit to 30 minutes instead of 1 hour (3600 seconds)
HOUR_LIMIT = 1800

flag = 0

# Create the Telegram client
try:
    BotzHubUser = TelegramClient(StringSession(SESSION), APP_ID, API_HASH)
    BotzHubUser.start()
except Exception as ap:
    print(f"ERROR - {ap}")
    exit(1)

if os.path.exists(log_file):
    os.remove(log_file)
open(log_file, "a", encoding='utf-8').close()

# Define the function to write to the log file
async def write_to_log(log_file, message, message_count):
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"{message_count}. {message}")

# Load messages from log file into a set
existing_messages = set()
with open(log_file, "r", encoding='utf-8') as f:
    for line in f:
        if line.startswith("Time:"):
            try:
                # Parse timestamp and check if it's within the last hour
                timestamp_str = line.split(":")[1].strip()
                timestamp = time.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                age_seconds = time.time() - time.mktime(timestamp)
                if age_seconds <= 60 * 60:
                    # Read the message text and add it to the set of existing messages
                    text_line = next(f)  # Read the "Sent:" line
                    text = ""
                    while not text_line.startswith("####"):
                        text += text_line
                        text_line = next(f)
                    existing_messages.add(text.strip())
            except (ValueError, IndexError) as e:
                print(f"ERROR - {e}. Skipping malformed log entry:", line)


@BotzHubUser.on(events.NewMessage(incoming=True, chats=list(FROM_CHANNEL.keys())))
async def sender_bH(event):
    global last_sent_time, sent_message_count
    # Check if the maximum number of messages have already been sent in the last hour
    if sent_message_count >= MAX_MESSAGES_PER_HOUR:
        current_time = time.time()
        if last_sent_time is not None and current_time - last_sent_time < HOUR_LIMIT:
            global time_left
            time_left = current_time - last_sent_time
            print(f"Maximum number of messages sent in the last hour. Skipping message.time left : {time_left}")
            return
        else:
            # Reset the message count if an hour has passed since the last message sent
            sent_message_count = 0
    message = event.message
    text = message.text
    file = None
    from_channel = event.chat_id
    required_text = "『 @ProxyKeder 』"

    if text in existing_messages:
        print("Skipping duplicate message:")
    else:
        message_count = len(existing_messages) + 1  # Initialize message count to the length of existing_messages plus 1
        for i in TO:
            if message.media:
                file = await message.download_media()
            if "@ProxyMTProto_tel" in text:
                text = text.replace("@ProxyMTProto_tel", "『 @ProxyKeder 』")
            if "@ProxyMTProto" in text:
                text = text.replace("@ProxyMTProto", "『 @ProxyKeder 』")
            if "@proxydarsi☜" in text:
                text = text.replace("🔥@proxydarsi☜", "『 @ProxyKeder 』")
            if "@IROproxy" in text:
                text = text.replace("🔥@IROproxy", "『 @ProxyKeder 』")
            if "@ProxyHagh ☜" in text:
                text = text.replace("🆔 @ProxyHagh ☜", "『 @ProxyKeder 』")
            if "@TelMTProto" in text:
                text = text.replace("@TelMTProto", "『 @ProxyKeder 』")
            if "@MyPoroxy" in text:
                text = text.replace("🆔 @MyPoroxy ☜", "『 @ProxyKeder 』")
            if required_text in text:
                try:
                    if file:
                        await BotzHubUser.send_file(i, file=file, caption=text)
                    else:
                        await BotzHubUser.send_message(i, text)

                    # Write message details to log file
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    await write_to_log(log_file, f"Time: {timestamp}\nSent:\n{text}\n\n", message_count)

                    # Add message to set of existing messages
                    existing_messages.add(text)

                    # Increment message counter and update the last sent time
                    sent_message_count += 1
                    last_sent_time = time.time()
                except Exception as e:
                    print(e)
                finally:
                        if file:
                            if os.path.exists(file):
                                os.remove(file)
                            else:
                                print(f"File {file} does not exist.")
            else:
                print("Skipping message because it doesn't contain the required text:", text)

BotzHubUser.run_until_disconnected()





