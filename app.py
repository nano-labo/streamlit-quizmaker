"""
cd nekobot/streamlit-nekobot
python -m venv env
env\Scripts\activate.bat

pip install --upgrade pip
pip install streamlit==1.41.1 openai==1.47.0 httpx==0.27.2 python-dotenv

streamlit run app.py


** 初回登録
git clone リポジトリのURL
git add .
git config -l
git config --global user.name "ユーザー名"
git config --global user.email "メールアドレス"


git clone https://github.com/nano-labo/streamlit-quizmaker

** コミット方法
git add .
git commit -m "first commit."
git push -u origin main

"""

from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from openai import OpenAI

def display_history(messages):
    for message in messages:
        display_msg_content(message)

def display_msg_content(message):
    #st.write(message)
    #st.write(message.content)
    with st.chat_message(message["role"]):
        st.write(message["content"])
        #st.write(message["content"][0]["text"])

client = OpenAI()

st.title("猫ボット")
#st.write("猫チャットボットは、夏目漱石の「吾輩は猫である」の猫の口調・性格で質問に答えるAIです。")
st.write("吾輩は猫である。何でも好きなように聞くがよい。")

st.divider()

MY_JOB_ID = "ftjob-ewBc6B03Z0YgkanSTyNCog7y"
fine_tuned_job = client.fine_tuning.jobs.retrieve(MY_JOB_ID)
#fine_tuned_job

#input_message = st.text_input(label="さて、何を聞きたいのかな。")
input_message = st.chat_input("さて、何を聞きたいのかな。")
#text_count = len(input_message)

#print(f"Input: {input_message}")

if "messages" not in st.session_state:
    st.session_state.messages = []

display_history(st.session_state.messages)

if "button_menu" not in st.session_state:
    st.session_state["button_menu"] = ""
if st.session_state["button_menu"]:
    st.write(st.session_state["button_menu"])
    input_message = st.session_state["button_menu"]
    st.session_state["button_menu"] = ""

#if st.button("聞く"):
if input_message:
    #以下は、質問に対してLLMからの回答を得るコードです。
    completion = client.chat.completions.create(
        model=fine_tuned_job.fine_tuned_model,
        messages=[
            {"role": "system", "content": "あなたは夏目漱石の「吾輩は猫である」の猫の口調・性格で、質問に対して回答するアシスタントAIです。"},
            {"role": "user", "content": input_message}
        ]
    )
    #st.write(completion)
    #msg = completion.choices[0].message.content
    #st.write(msg)
    msg = completion.choices[0].message
    #st.write(msg.content)
    #display_msg_content(msg)
    #display_msg_content({"role": "assistant", "content": msg.content})
    
    with st.chat_message("user"):
        st.markdown(input_message)
    with st.chat_message("assistant"):
        st.markdown(msg.content)
    
    #st.session_state.messages.append(input_message)
    #st.session_state.messages.append(msg)
    st.session_state.messages.append({"role": "user", "content": input_message})
    st.session_state.messages.append({"role": "assistant", "content": msg.content})



if st.button("今日の天気は"):
    st.session_state["button_menu"] = "今日の天気は"
    st.write(st.session_state["button_menu"])
    st.rerun()
if st.button("おすすめのレシピは"):
    st.session_state["button_menu"] = "おすすめのレシピは"
    st.write(st.session_state["button_menu"])
    st.rerun()


if "count" not in st.session_state:
    st.session_state["count"] = 0
st.session_state.count += 1
st.write(f"現在のカウント: {st.session_state.count}")


# クイズデータ（20問分）
quiz_data = [
    {"question": "日本代表の愛称は？", "options": ["ブルーイーグルス", "ブルーホークス", "サムライブルー", "ニッポンナイツ"], "answer": 2},
    {"question": "日本代表が初めてW杯に出場した年は？", "options": ["1994年", "1998年", "2002年", "1990年"], "answer": 1},
    {"question": "日本代表の最多出場記録を持つ選手は？", "options": ["長谷部誠", "川口能活", "吉田麻也", "遠藤保仁"], "answer": 3},
    {"question": "日本代表が初めてW杯で勝利した相手は？", "options": ["チュニジア", "ロシア", "デンマーク", "カメルーン"], "answer": 1},
    {"question": "日本代表の2022年W杯監督は？", "options": ["岡田武史", "西野朗", "森保一", "トルシエ"], "answer": 2},
    {"question": "日本がW杯で初のベスト16に進出した大会は？", "options": ["1998年", "2002年", "2006年", "2010年"], "answer": 1},
    {"question": "2002年W杯で日本が戦った国は？", "options": ["ベルギー、ロシア、チュニジア", "イタリア、ナイジェリア、アメリカ", "イングランド、デンマーク、韓国", "フランス、ウルグアイ、韓国"], "answer": 0},
    {"question": "本田圭佑がW杯で初ゴールを決めたのは？", "options": ["2010年 デンマーク戦", "2014年 ギリシャ戦", "2010年 カメルーン戦", "2018年 セネガル戦"], "answer": 2},
    {"question": "日本がW杯で初めて3勝した大会は？", "options": ["2010年", "2014年", "2018年", "2022年"], "answer": 3},
    {"question": "久保建英の代表デビューは何歳？", "options": ["17歳", "18歳", "19歳", "20歳"], "answer": 1},
    {"question": "サッカー日本代表のホームスタジアムは？", "options": ["国立競技場", "味の素スタジアム", "埼玉スタジアム2002", "豊田スタジアム"], "answer": 2},
    {"question": "日本がW杯で対戦したことがない国は？", "options": ["ドイツ", "スペイン", "アルゼンチン", "ベルギー"], "answer": 2},
    {"question": "W杯でゴールを決めた選手の中で最多得点は？", "options": ["本田圭佑", "岡崎慎司", "稲本潤一", "香川真司"], "answer": 0},
    {"question": "中田英寿が代表を引退したのはいつ？", "options": ["2004年", "2006年", "2002年", "2008年"], "answer": 1},
    {"question": "2022年W杯で日本が勝利した強豪国は？", "options": ["ドイツ・スペイン", "フランス・ブラジル", "ポルトガル・オランダ", "イングランド・クロアチア"], "answer": 0},
    {"question": "初の海外クラブ所属の代表選手は？", "options": ["三浦知良", "中田英寿", "奥寺康彦", "城彰二"], "answer": 2},
    {"question": "日本代表のユニフォームカラーは？", "options": ["青", "赤", "白", "黒"], "answer": 0},
    {"question": "日本代表が最多得点を記録したW杯試合は？", "options": ["2010年vsデンマーク", "2002年vsチュニジア", "2018年vsセネガル", "2022年vsドイツ"], "answer": 0},
    {"question": "2010年大会でPK戦に敗れた相手は？", "options": ["ウルグアイ", "パラグアイ", "コロンビア", "スペイン"], "answer": 1},
    {"question": "三笘薫が活躍した「ライン上パス」の相手は？", "options": ["クロアチア", "ドイツ", "スペイン", "ベルギー"], "answer": 2},
]

# セッションステートで状態を管理
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False

# 現在のクイズ
current_quiz = quiz_data[st.session_state.quiz_index]

st.title("⚽ サッカー日本代表クイズ")

st.subheader(f"第 {st.session_state.quiz_index + 1} 問 / {len(quiz_data)} 問中")
st.write(current_quiz["question"])

# 回答選択
selected = st.radio("選択肢を選んでください", current_quiz["options"], key=st.session_state.quiz_index)

# 回答ボタン
if st.button("回答する") and not st.session_state.answered:
    correct = current_quiz["answer"]
    if current_quiz["options"].index(selected) == correct:
        st.success("正解！")
        st.session_state.score += 1
    else:
        st.error(f"不正解。正解は「{current_quiz['options'][correct]}」です。")
    st.session_state.answered = True

# 次の問題へ
if st.session_state.answered and st.button("次の問題へ"):
    st.session_state.quiz_index += 1
    st.session_state.answered = False
    if st.session_state.quiz_index >= len(quiz_data):
        st.write("🎉 クイズ終了！")
        st.write(f"あなたのスコア: {st.session_state.score} / {len(quiz_data)}")
        st.stop()