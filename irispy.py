
import sys
import os
import requests

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from iris import Bot, ChatContext, IrisLink
from google import genai
from google.genai import types

load_dotenv()
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
        if chat.message.msg.startswith("!"):
            try:
                if len(conversation_history) > 20:
                    conversation_history[:] = conversation_history[10:]

                conversation_history.append({"role": "user", "content": chat.message.msg[1:]})

                interaction = client.interactions.create(
                    model="gemini-2.5-flash-lite",
                    system_instruction=f"너는 '빻봇'이라는 이름으로 불려. 가능한 정확한 지식을 전달하도록 해. 친절하게 반말로 대답해. 너에게 질문하는 사람은 '{chat.sender.name}'",
                    input=conversation_history
                )

                bot_response = interaction.outputs[-1].text
                conversation_history.append({"role": "model", "content": bot_response})

                chat.reply(bot_response)
            except Exception as e:
                chat.reply(f"{chat.sender.name}, 빻봇은 토큰을 모으고 있어요... 잠시 후에 다시 시도해줘!")
        
        elif chat.message.msg.startswith("https://") or chat.message.msg.startswith("http://"):
            try:
                url = chat.message.msg.strip()
                # 웹페이지 가져오기
                response = requests.get(url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                response.raise_for_status()
                # HTML 파싱
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 불필요한 태그 제거
                for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'ad', 'iframe']):
                    tag.decompose()
                
                # article 태그 우선 찾기 (뉴스 본문)
                article = soup.find('article')
                if article:
                    text = article.get_text(separator='\n', strip=True)
                else:
                    # article이 없으면 전체 본문
                    text = soup.get_text(separator='\n', strip=True)
                
                # 공백 정리
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                text = '\n'.join(lines)
                
                # 너무 길면 자르기 (토큰 제한)
                if len(text) > 15000:
                    text = text[:15000]
                
                # Gemini로 요약
                config = types.GenerateContentConfig(
                    system_instruction="다음은 뉴스 기사 본문이야. 핵심 내용을 3-5문장으로 한국어로 요약해줘."
                )
                summary_response = client.models.generate_content(
                    model="gemini-2.5-flash-lite",
                    contents=text,
                    config=config,
                )
                chat.reply(summary_response.text)
            except Exception as e:
                chat.reply(f"{chat.sender.name}, 빻봇은 토큰을 모으고 있어요... 잠시 후에 다시 시도해줘!")

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
