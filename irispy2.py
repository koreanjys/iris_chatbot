import sys
import os
import logging

from dotenv import load_dotenv
from iris import Bot, ChatContext, IrisLink
from google import genai
from google.genai import types

load_dotenv()
log_dir = "./log"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s\n%(message)s",
    filename=f"{log_dir}/irispy2.log",
    filemode='a',
    encoding="utf-8"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)
conversation_history = []


if len(sys.argv) < 2:
    print("Usage: python irispy.py {아이리스HOST}:3000")  # 127.0.0.1:3000
    sys.exit(1)
iris_url = sys.argv[1]
bot = Bot(iris_url)
#bot.iris_url은 정제된 주소(IP:PORT 형식)
#kl = IrisLink(bot.iris_url)

#메시지 감지
@bot.on_event("message")
def on_message(chat: ChatContext):
    if chat.room.id == 18247793138980592:  #특정 방에서만 반응

        if len(conversation_history) > 100:
            conversation_history[:] = conversation_history[10:]

        # 메세지 기록 (100개)
        conversation_history.append({"role": "user", "content": f"Name='{chat.sender.name}': Chat='{chat.message.msg}'"})

        if chat.message.msg.startswith("!요약") and chat.sender.id == 143365411:
            try:
                interaction = client.interactions.create(
                    model="gemini-2.5-flash-lite",
                    system_instruction=f"대화 한 사람별로 이름과 대화 내용을 구분해서 각 사람별로 간략하게 요약해 주세요.",
                    input=conversation_history
                )
                bot_response = interaction.outputs[-1].text
                chat.reply(bot_response)
            except Exception as e:
                chat.reply(f"{chat.sender.name}, 빻봇은 토큰을 모으고 있어요... 잠시 후에 다시 시도해줘!")
                logging.error(f"Error during summarization: {e}")
        
#입장감지
@bot.on_event("new_member")
def on_newmem(chat: ChatContext):
    #chat.reply(f"Hello {chat.sender.name}")
    pass

#퇴장감지
@bot.on_event("del_member")
def on_delmem(chat: ChatContext):
    #chat.reply(f"Bye {chat.sender.name}")
    pass

@bot.on_event("error")
def on_error(err):
    print(f"{err.event} 이벤트에서 오류가 발생했습니다: {err.exception}")

if __name__ == "__main__":
    bot.run()
