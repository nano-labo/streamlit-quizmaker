"""
cd nekobot/streamlit-nekobot
python -m venv env
env\Scripts\activate.bat

pip install --upgrade pip
pip install streamlit==1.41.1 openai==1.47.0 httpx==0.27.2 python-dotenv

pip freeze > requirements.txt

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
    with st.chat_message(message["role"]):
        st.write(message["content"])

client = OpenAI()

#st.title("猫ボット")
#st.write("吾輩は猫である。何でも好きなように聞くがよい。")

#st.divider()

MY_JOB_ID = "ftjob-ewBc6B03Z0YgkanSTyNCog7y"
fine_tuned_job = client.fine_tuning.jobs.retrieve(MY_JOB_ID)
#fine_tuned_job

#input_message = st.text_input(label="さて、何を聞きたいのかな。")
input_message = st.chat_input("さて、何を聞きたいのかな。")


if "messages" not in st.session_state:
    st.session_state.messages = []

display_history(st.session_state.messages)

if "button_menu" not in st.session_state:
    st.session_state["button_menu"] = ""

if st.session_state["button_menu"]:
    st.write(st.session_state["button_menu"])
    input_message = st.session_state["button_menu"]
    st.session_state["button_menu"] = ""

if input_message:
    #以下は、質問に対してLLMからの回答を得るコードです。
    completion = client.chat.completions.create(
        model=fine_tuned_job.fine_tuned_model,
        messages=[
            {"role": "system", "content": "あなたは夏目漱石の「吾輩は猫である」の猫の口調・性格で、質問に対して回答するアシスタントAIです。"},
            {"role": "user", "content": input_message}
        ]
    )
    msg = completion.choices[0].message
    
    with st.chat_message("user"):
        st.markdown(input_message)
    with st.chat_message("assistant"):
        st.markdown(msg.content)
    
    st.session_state.messages.append({"role": "user", "content": input_message})
    st.session_state.messages.append({"role": "assistant", "content": msg.content})

# コメント切替 CTRL + /
# if st.button("今日の天気は"):
#     st.session_state["button_menu"] = "今日の天気は"
#     st.write(st.session_state["button_menu"])
#     st.rerun()
# if st.button("おすすめのレシピは"):
#     st.session_state["button_menu"] = "おすすめのレシピは"
#     st.write(st.session_state["button_menu"])
#     st.rerun()


if "count" not in st.session_state:
    st.session_state["count"] = 0
st.session_state.count += 1
st.write(f"現在のカウント: {st.session_state.count}")


# クイズデータ（20問分）
quiz_data_all = {
    "サッカー": [
        {"question": "日本代表の愛称は？", "options": ["ブルーイーグルス", "ブルーホークス", "サムライブルー", "ニッポンナイツ"], "answer": 2, "explanation": "日本代表のユニフォームは青を基調としており、侍のイメージと合わせて「サムライブルー」と呼ばれています。"},
        {"question": "日本代表が初めてW杯に出場した年は？", "options": ["1994年", "1998年", "2002年", "1990年"], "answer": 1, "explanation": "日本は1998年フランス大会でW杯初出場を果たしました。"},
        {"question": "日本代表の最多出場記録を持つ選手は？（2024年時点）", "options": ["長谷部誠", "川口能活", "吉田麻也", "遠藤保仁"], "answer": 3, "explanation": "遠藤保仁選手は国際Aマッチで150試合以上出場しており、歴代最多です。"},
        {"question": "日本代表が初めてW杯で勝利した相手は？", "options": ["チュニジア", "ロシア", "デンマーク", "カメルーン"], "answer": 1, "explanation": "2002年日韓W杯でロシアに1-0で勝利し、日本のW杯初勝利となりました。"},
        {"question": "日本代表の2022年W杯監督は？", "options": ["岡田武史", "西野朗", "森保一", "トルシエ"], "answer": 2, "explanation": "森保一監督は2018年から2022年大会まで代表を率い、強豪撃破の快挙を達成しました。"},
        {"question": "日本がW杯で初のベスト16に進出した大会は？", "options": ["1998年", "2002年", "2006年", "2010年"], "answer": 1, "explanation": "2002年の日韓共催大会で日本はグループ1位通過し、初の決勝トーナメント進出を果たしました。"},
        {"question": "2002年W杯で日本が戦った国は？（グループリーグ）", "options": ["ベルギー、ロシア、チュニジア", "イタリア、ナイジェリア、アメリカ", "イングランド、デンマーク、韓国", "フランス、ウルグアイ、韓国"], "answer": 0, "explanation": "2002年大会で日本はグループHに属し、ベルギー・ロシア・チュニジアと対戦しました。"},
        {"question": "本田圭佑がW杯で初ゴールを決めたのは？", "options": ["2010年 デンマーク戦", "2014年 ギリシャ戦", "2010年 カメルーン戦", "2018年 セネガル戦"], "answer": 2, "explanation": "2010年南アフリカ大会のカメルーン戦で本田が決勝ゴールを決めました。"},
        {"question": "日本がW杯で初めて3勝した大会は？", "options": ["2010年", "2014年", "2018年", "2022年"], "answer": 3, "explanation": "2022年カタール大会ではドイツ、スペイン、コスタリカに勝利し、W杯最多勝を記録しました。"},
        {"question": "久保建英の代表デビューは何歳？", "options": ["17歳", "18歳", "19歳", "20歳"], "answer": 1, "explanation": "久保建英は18歳で日本代表に初選出され、注目を集めました。"},
        {"question": "サッカー日本代表のホームスタジアムは？", "options": ["国立競技場", "味の素スタジアム", "埼玉スタジアム2002", "豊田スタジアム"], "answer": 2, "explanation": "代表戦の多くは「埼スタ」こと埼玉スタジアム2002で開催されます。"},
        {"question": "日本がW杯で対戦したことがない国は？", "options": ["ドイツ", "スペイン", "アルゼンチン", "ベルギー"], "answer": 2, "explanation": "2024年時点で、アルゼンチンとはW杯本大会での対戦がありません。"},
        {"question": "W杯でゴールを決めた選手の中で最多得点は？（日本代表）", "options": ["本田圭佑", "岡崎慎司", "稲本潤一", "香川真司"], "answer": 0, "explanation": "本田圭佑はW杯3大会連続ゴールを含め、通算4得点を挙げました。"},
        {"question": "中田英寿が代表を引退したのはいつ？", "options": ["2004年", "2006年", "2002年", "2008年"], "answer": 1, "explanation": "中田英寿は2006年W杯終了後、29歳で現役引退を表明しました。"},
        {"question": "2022年W杯で日本が勝利した強豪国は？", "options": ["ドイツ・スペイン", "フランス・ブラジル", "ポルトガル・オランダ", "イングランド・クロアチア"], "answer": 0, "explanation": "日本はグループリーグでドイツとスペインという優勝経験国を破りました。"},
        {"question": "初の海外クラブ所属の代表選手は？", "options": ["三浦知良", "中田英寿", "奥寺康彦", "城彰二"], "answer": 2, "explanation": "奥寺康彦は1970年代からドイツでプレーし、“東洋のコンピューター”と呼ばれました。"},
        {"question": "日本代表のユニフォームカラーは？", "options": ["青", "赤", "白", "黒"], "answer": 0, "explanation": "日本代表はホーム用に青いユニフォームを採用しており「サムライブルー」の由来となっています。"},
        {"question": "日本代表が最多得点を記録したW杯試合は？", "options": ["2010年vsデンマーク", "2002年vsチュニジア", "2018年vsセネガル", "2022年vsドイツ"], "answer": 0, "explanation": "2010年のデンマーク戦では3-1で勝利し、日本代表のW杯最多得点試合となりました。"},
        {"question": "2010年大会でPK戦に敗れた相手は？", "options": ["ウルグアイ", "パラグアイ", "コロンビア", "スペイン"], "answer": 1, "explanation": "2010年南アフリカ大会の決勝Tで日本はパラグアイにPK戦で惜敗しました。"},
        {"question": "三笘薫が活躍した「ライン上パス」の相手は？", "options": ["クロアチア", "ドイツ", "スペイン", "ベルギー"], "answer": 2, "explanation": "2022年W杯スペイン戦での「ライン上折り返し→田中碧ゴール」は大きな話題となりました。"},
    ],
    "テニス": [
        {"question": "四大大会に含まれないのは？", "options": ["全豪オープン", "全仏オープン", "ウィンブルドン", "マスターズカップ"], "answer": 3, "explanation": "マスターズカップは四大大会（グランドスラム）には含まれません。"}
        {"question": "「ビッグ3」と呼ばれる男子選手の組み合わせは？", "options": ["ナダル・フェデラー・ジョコビッチ", "マレー・デルポトロ・ジョコビッチ", "チチパス・ズベレフ・ティエム", "ナダル・フェデラー・マレー"], "answer": 0, "explanation": "長年テニス界を支配したのがナダル、フェデラー、ジョコビッチの3人です。"},
        {"question": "グランドスラム通算優勝数最多（2024年時点）の男子選手は？", "options": ["ロジャー・フェデラー", "ノバク・ジョコビッチ", "ラファエル・ナダル", "ピート・サンプラス"], "answer": 1, "explanation": "ジョコビッチが最多の24勝（2024年）を記録しています。"},
        {"question": "全豪オープンが行われる都市は？", "options": ["シドニー", "メルボルン", "パース", "ブリスベン"], "answer": 1, "explanation": "全豪オープンはオーストラリア・メルボルンで開催されます。"},
        {"question": "ウィンブルドン最多優勝記録（男子）保持者は？", "options": ["ナダル", "サンプラス", "ジョコビッチ", "フェデラー"], "answer": 3, "explanation": "フェデラーはウィンブルドンで8回の優勝を誇ります。"},
        {"question": "WTA世界ランキングで史上最年少1位は？", "options": ["大坂なおみ", "マリア・シャラポワ", "マルチナ・ヒンギス", "セリーナ・ウィリアムズ"], "answer": 2, "explanation": "ヒンギスは16歳で世界1位に到達しました。"},
        {"question": "全仏オープン最多優勝記録（男子）保持者は？", "options": ["ジョコビッチ", "ナダル", "フェデラー", "モヤ"], "answer": 1, "explanation": "ナダルは全仏オープンで14回の優勝という圧倒的な記録を持っています。"},
        {"question": "グランドスラム全制覇（キャリアグランドスラム）を達成していないのは？", "options": ["フェデラー", "ナダル", "ジョコビッチ", "マレー"], "answer": 3, "explanation": "マレーは全仏オープンを制覇しておらず、キャリアグランドスラム未達です。"},
        {"question": "2021年全米オープン男子決勝でジョコビッチを破った選手は？", "options": ["ティエム", "メドベージェフ", "チチパス", "ズベレフ"], "answer": 1, "explanation": "メドベージェフがジョコビッチをストレートで破り初優勝しました。"},
        {"question": "セリーナ・ウィリアムズのグランドスラム優勝回数は？", "options": ["18", "21", "23", "24"], "answer": 2, "explanation": "セリーナは23回のグランドスラムタイトルを獲得しています。"},
        {"question": "ディフェンディングチャンピオンとは？", "options": ["引退した王者", "前年優勝者", "世界ランキング1位", "地元選手"], "answer": 1, "explanation": "「ディフェンディングチャンピオン」は前年優勝者を指します。"},
        {"question": "ATPファイナルズの年間出場枠は？", "options": ["4人", "6人", "8人", "16人"], "answer": 2, "explanation": "シーズン成績上位8人だけが出場できるエリート大会です。"},
        {"question": "全米オープンの開催時期は？", "options": ["1月", "5月", "7月", "8月〜9月"], "answer": 3, "explanation": "全米は夏の終わり、8月下旬から9月にかけて開催されます。"},
        {"question": "ATPツアーの頂点を決める大会は？", "options": ["デビスカップ", "マスターズ1000", "ATPファイナルズ", "チャレンジャー大会"], "answer": 2, "explanation": "ATPファイナルズはツアー上位8名による年間王者決定戦です。"},
        {"question": "2023年のウィンブルドン男子優勝者は？", "options": ["ジョコビッチ", "アルカラス", "メドベージェフ", "ルード"], "answer": 1, "explanation": "カルロス・アルカラスが決勝でジョコビッチを破って初優勝しました。"},
        {"question": "マリア・シャラポワが最初に優勝したグランドスラムは？", "options": ["全豪", "全仏", "全米", "ウィンブルドン"], "answer": 3, "explanation": "シャラポワは17歳で2004年ウィンブルドンを制覇しました。"},
        {"question": "大坂なおみがWTAツアーで最初に優勝したのは？", "options": ["インディアンウェルズ", "全米オープン", "東京オープン", "ローマ大会"], "answer": 0, "explanation": "2018年のインディアンウェルズでツアー初優勝を果たしました。"},
        {"question": "ノバク・ジョコビッチの国籍は？", "options": ["スロバキア", "クロアチア", "セルビア", "オーストリア"], "answer": 2, "explanation": "ジョコビッチはセルビア出身です。"},
        {"question": "グランドスラムの中で最も古い大会は？", "options": ["全豪", "全仏", "全米", "ウィンブルドン"], "answer": 3, "explanation": "ウィンブルドンは1877年に始まり、最も歴史ある大会です。"},
        {"question": "2020年東京五輪の女子金メダルは？", "options": ["バーティ", "スビトリナ", "ベンチッチ", "アザレンカ"], "answer": 2, "explanation": "スイスのベンチッチが女子シングルスで金メダルを獲得しました。"},
        {"question": "カルロス・アルカラスがグランドスラム初優勝を飾った大会は？", "options": ["全仏オープン", "全米オープン", "ウィンブルドン", "全豪オープン"], "answer": 1, "explanation": "アルカラスは2022年全米オープンで初のグランドスラム優勝を達成しました。"},
    ],
    "野球": [
        {"question":"野球で1イニングは何アウトでチェンジ？","options":["2アウト","3アウト","4アウト","5アウト"],"answer":1,"explanation":"各チーム3アウトで攻守交代です。"},
        {"question":"WBC2023で日本が決勝で対戦した国は？","options":["アメリカ","韓国","ドミニカ共和国","プエルトリコ"],"answer":0,"explanation":"決勝はアメリカとの対戦で、日本が優勝しました。"},
        {"question":"日本プロ野球のセ・リーグ球団はどれ？","options":["楽天","日本ハム","DeNA","オリックス"],"answer":2,"explanation":"DeNAベイスターズはセ・リーグ所属です。"},
        {"question":"メジャーリーグで最多本塁打記録を持つのは？","options":["ベーブ・ルース","バリー・ボンズ","マーク・マグワイア","アレックス・ロドリゲス"],"answer":1,"explanation":"ボンズが通算762本で最多です。"},
        {"question":"イチローが所属していなかったチームは？","options":["マリナーズ","ヤンキース","ドジャース","マーリンズ"],"answer":2,"explanation":"イチローはドジャースには所属していません。"},
        {"question":"プロ野球の1試合は何回までが通常？","options":["7回","8回","9回","10回"],"answer":2,"explanation":"通常は9回制です（延長あり）。"},
        {"question":"野球で「犠打」とは何の略？","options":["犠牲打","犠牲点","犠牲球","犠牲走"],"answer":0,"explanation":"進塁のためにアウトになる打撃を犠牲打と呼びます。"},
        {"question":"WBC初代優勝国は？","options":["キューバ","アメリカ","日本","韓国"],"answer":2,"explanation":"第1回WBC（2006年）は日本が初代王者です。"},
        {"question":"2023年WBCでMVPを獲得した選手は？","options":["大谷翔平","ダルビッシュ有","吉田正尚","村上宗隆"],"answer":0,"explanation":"大谷翔平が大会MVPに輝きました。"},
        {"question":"甲子園球場の所在地は？","options":["大阪","兵庫","京都","東京"],"answer":1,"explanation":"兵庫県西宮市にあります。"},
        {"question":"ノーヒットノーランとは何か？","options":["本塁打を打たれない","出塁を許さない","ヒットも四球も出さない","ヒットを1本も許さない"],"answer":3,"explanation":"ヒットを1本も打たれずに試合を終えることです。"},
        {"question":"野球のポジション番号でピッチャーは？","options":["1","2","3","4"],"answer":0,"explanation":"ピッチャーは守備番号1です。"},
        {"question":"メジャーリーグの公式球団数は？（2024年時点）","options":["28","30","32","34"],"answer":1,"explanation":"MLBは30球団で構成されています。"},
        {"question":"「トリプルスリー」とは？","options":["3冠王の別名","3つの球団でプレー","3割30本30盗塁","3連続サヨナラ勝ち"],"answer":2,"explanation":"打率3割、本塁打30本、盗塁30の達成記録です。"},
        {"question":"大谷翔平が2021年に達成した偉業は？","options":["打点王","二刀流での活躍","三冠王","ノーヒットノーラン"],"answer":1,"explanation":"大谷は投打の二刀流で大活躍しました。"},
        {"question":"「パ・リーグ」に所属しない球団は？","options":["ロッテ","ソフトバンク","巨人","楽天"],"answer":2,"explanation":"巨人はセ・リーグ所属です。"},
        {"question":"野球で「満塁」とは？","options":["3ストライク","3アウト","全塁にランナーがいる","3失点"],"answer":2,"explanation":"一塁・二塁・三塁すべてに走者がいる状態です。"},
        {"question":"1打席で満塁本塁打を打ったときの得点は？","options":["1点","2点","3点","4点"],"answer":3,"explanation":"満塁本塁打は4点入ります。"},
        {"question":"プロ野球で1年間のペナントレース試合数は？（2024年時点）","options":["120試合","130試合","143試合","150試合"],"answer":2,"explanation":"セ・パ両リーグとも143試合制です。"},
        {"question":"2023年の日本シリーズで優勝したチームは？","options":["オリックス","阪神","ソフトバンク","ヤクルト"],"answer":1,"explanation":"阪神タイガースが38年ぶりに優勝しました。"},
   ]
}

# セッションステートで状態を管理
if "genre" not in st.session_state:
    st.session_state.genre = None
if "quiz_index" not in st.session_state:
    st.session_state.quiz_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False

def display_menu():
    st.write("クイズジャンルを選んでください")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("サッカー"):
            st.session_state.genre = "サッカー"
            st.session_state.quiz_index = 0
            st.rerun()
    with col2:
        if st.button("テニス"):
            st.session_state.genre = "テニス"
            st.session_state.quiz_index = 0
            st.rerun()
    with col3:
        if st.button("野球"):
            st.session_state.genre = "野球"
            st.session_state.quiz_index = 0
            st.rerun()
    st.stop()


# ジャンルが未選択の場合、ジャンル選択ボタンを表示
if st.session_state.genre is None:
    display_menu()

# 現在のクイズ
genre = st.session_state.genre
quiz_data = quiz_data_all[genre]
current_quiz = quiz_data[st.session_state.quiz_index]

st.title("⚽ サッカー日本代表クイズ")

st.subheader(f"第 {st.session_state.quiz_index + 1} 問 / {len(quiz_data)} 問中")
st.write(current_quiz["question"])

# 回答選択
#selected = st.radio("選択肢を選んでください", current_quiz["options"], key=st.session_state.quiz_index)

# 回答選択肢をボタンで表示
selected = None
for i, option in enumerate(current_quiz["options"]):
    if st.button(option):
        selected = i

# 回答ボタン
#if st.button("回答する") and not st.session_state.answered:
if selected is not None and not st.session_state.answered:
    correct = current_quiz["answer"]
    if selected == correct:
        st.success("正解！")
        st.info(f"解説：{current_quiz['explanation']}")
        st.session_state.score += 1
    else:
        st.error(f"不正解。正解は「{current_quiz['options'][correct]}」です。")
        st.info(f"解説：{current_quiz['explanation']}")
    st.session_state.answered = True


# 次の問題へ
if st.session_state.answered and st.button("次の問題へ"):
    st.session_state.quiz_index += 1
    st.session_state.answered = False
    if st.session_state.quiz_index >= len(quiz_data):
        st.write("🎉 クイズ終了！")
        st.write(f"あなたのスコア: {st.session_state.score} / {len(quiz_data)}")
        st.session_state.quiz_index = 0
        st.session_state.genre = None
        display_menu()
        st.stop()
    else:
        st.rerun()