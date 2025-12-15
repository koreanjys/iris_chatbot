
import sys
import os

from dotenv import load_dotenv
from iris import Bot, ChatContext, IrisLink
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

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
        if chat.message.command.startswith("!"):
            try:
                prompt = "프롬프트에 대해 유머러스하게 한국어로 100 자 이내로 짧게 답변해. 프롬프트 : " + chat.message.command[1:]  #명령어 앞의 '!' 제거
                response = model.generate_content(prompt).text
                # chat.reply(f"안녕, {chat.sender.name}! 좋은 밤 보내!")
                chat.reply(response)
            except Exception as e:
                chat.reply("빻봇은 토큰을 모으고 있어요... 잠시 후에 다시 시도해주세요!")

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
