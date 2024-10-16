import requests
import streamlit as st
from langchain_core.messages.chat import ChatMessage

st.title("AI봇💬")

def send_chat_message(prompt, gid, question):
    
    import json
    
    # payload = json.dumps({
    #     "body": json.dumps({
    #         "prompt": prompt,
    #         "question": question,
    #         "gid": gid
    #     })
    # })

    payload = {
        "prompt": prompt,
        "question": question,
        "goodsId": gid
    }
    headers = {
        "Accept": "text/plain",
        "Content-Type": "application/json"
        }
    try:
        # HTTP POST 요청 보내기
        response = requests.post(api_server, data=payload, headers=headers)
        
        # 요청이 성공했는지 확인
        response.raise_for_status()  # 상태 코드가 200번대가 아니면 예외 발생
        
        # 응답의 body 부분을 JSON으로 변환
        response_body = response.json()  # response.json()으로 응답을 JSON으로 파싱

        # body 안의 message만 추출
        body = json.loads(response_body['body'])
        message = body.get('message')
        
        return message

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
        
# 이전 대화를 출력
if "messages" not in st.session_state:
    # 대화기록을 저장하기 위한 용도로 생성한다.
    st.session_state["messages"] = []
    
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)
            
# 새로운 메시지를 추가
def add_message(role, message):
        st.session_state["messages"].append(ChatMessage(role=role, content=message))
            
# 사이드바 생성
with st.sidebar:
    st.markdown("## 사용 방법 \n"
                    "1. 🕸️ URL 을 입력해주세요.\n"
                    "2. 🔑 ID를 입력해주세요.\n"
                    "3. ♥️ Prompt 를 입력하세요.\n"
                    "4. 🏃 궁금한 내용을 물어보세요!\n"
                    "---")
    
    api_server = st.text_input("URL(필수)", "")
    
    gid = st.number_input("ID(필수)", min_value=1, step=1)
    
    prompt = st.text_area('Prompt', height=780)


# 이전 대화 기록 출력
print_messages()
    
# 사용자의 입력
question = st.chat_input("궁금한 내용을 물어보세요!")

# 만약에 사용자 입력이 들어오면...
if question:
    # 사용자의 입력
    st.chat_message("user").write(question)

    with st.chat_message("assistant"):
        container = st.empty()
        
        answer = send_chat_message(prompt, gid, question)
        container.markdown(answer)
        
    # 대화기록을 저장한다.
    add_message("user", question)
    add_message("assistant", answer)
