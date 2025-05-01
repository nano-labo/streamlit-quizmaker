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
        {"question": "四大大会に含まれないのは？", "options": ["全豪オープン", "全仏オープン", "ウィンブルドン", "マスターズカップ"], "answer": 3, "explanation": "マスターズカップは四大大会（グランドスラム）には含まれません。"},
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
        {"question": "WBC2023で日本が決勝で戦った国は？", "options": ["アメリカ", "韓国", "ドミニカ共和国", "プエルトリコ"], "answer": 0, "explanation": "2023年のWBC決勝はアメリカ対日本。日本が勝利しました。"},
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
   ],
   "世界遺産": [
        { "question": "マチュ・ピチュがある国はどこ？", "options": ["ペルー", "メキシコ", "ボリビア", "ブラジル"], "answer": 0, "explanation": "マチュ・ピチュはペルーのアンデス山中にあるインカ帝国の遺跡です。" },
        { "question": "万里の長城がある国は？", "options": ["日本", "モンゴル", "中国", "韓国"], "answer": 2, "explanation": "万里の長城は中国に築かれた防御壁で、世界最長の建造物の一つです。" },
        { "question": "ピラミッド群があるギザはどこの国？", "options": ["トルコ", "エジプト", "イラク", "モロッコ"], "answer": 1, "explanation": "ギザの三大ピラミッドはエジプト文明を代表する建造物です。" },
        { "question": "「自由の女神像」があるのはどこ？", "options": ["イギリス", "フランス", "アメリカ", "カナダ"], "answer": 2, "explanation": "自由の女神はアメリカ・ニューヨークにあり、フランスから寄贈されました。" },
        { "question": "世界最古の石造建築とされるストーンヘンジがある国は？", "options": ["アイルランド", "ドイツ", "イギリス", "スウェーデン"], "answer": 2, "explanation": "ストーンヘンジはイギリス南部にある先史時代の巨石遺跡です。" },
        { "question": "タージ・マハルがある国は？", "options": ["ネパール", "パキスタン", "イラン", "インド"], "answer": 3, "explanation": "タージ・マハルはインドのムガル帝国が建設した壮麗な霊廟です。" },
        { "question": "モン・サン＝ミッシェルがある国は？", "options": ["フランス", "イタリア", "スペイン", "ベルギー"], "answer": 0, "explanation": "モン・サン＝ミッシェルはフランスの海に浮かぶ修道院で、観光地としても有名です。" },
        { "question": "イースター島のモアイ像がある国は？", "options": ["アルゼンチン", "チリ", "ペルー", "ブラジル"], "answer": 1, "explanation": "イースター島はチリ領で、巨大なモアイ像が多数残されています。" },
        { "question": "世界遺産「白川郷・五箇山の合掌造り集落」があるのは？", "options": ["長野・山梨", "岐阜・富山", "福島・新潟", "静岡・石川"], "answer": 1, "explanation": "白川郷（岐阜県）と五箇山（富山県）の合掌造り集落は、伝統的な建築様式が残る地域です。" },
        { "question": "マラケシュの旧市街がある国は？", "options": ["チュニジア", "エジプト", "モロッコ", "トルコ"], "answer": 2, "explanation": "マラケシュはモロッコの都市で、イスラム文化と建築が色濃く残る歴史地区です。" },

        { "question": "マチュ・ピチュは何と呼ばれることがある？", "options": ["失われた都市", "砂漠の奇跡", "空飛ぶ城", "太陽の塔"], "answer": 0, "explanation": "マチュ・ピチュは「失われた都市」と呼ばれるインカ帝国の遺跡です。" },
        { "question": "次のうち文化遺産に分類されるのは？", "options": ["グランドキャニオン", "ヴェルサイユ宮殿", "キリマンジャロ", "イグアスの滝"], "answer": 1, "explanation": "ヴェルサイユ宮殿は人類の歴史的文化を示す文化遺産です。" },
        { "question": "ピラミッドは主に何の目的で建てられた？", "options": ["兵器庫", "王の墓", "天文観測所", "儀式用神殿"], "answer": 1, "explanation": "ピラミッドは古代エジプト王の墓として建てられました。" },
        { "question": "「ガラパゴス諸島」の特筆すべき特徴は？", "options": ["巨大な滝", "砂漠の動物群", "独自の進化を遂げた生態系", "仏教建築群"], "answer": 2, "explanation": "ガラパゴス諸島はダーウィンの進化論でも知られる独自生態系が有名です。" },
        { "question": "アンコール・ワットは元々どの宗教に基づいて建てられた？", "options": ["仏教", "キリスト教", "ヒンドゥー教", "イスラム教"], "answer": 2, "explanation": "アンコール・ワットは元々ヒンドゥー教寺院として建てられました。" },
        { "question": "危機遺産に登録されたことがあるのは？", "options": ["ポンペイ", "アユタヤ遺跡", "ドレスデンのエルベ渓谷", "マヤ文明遺跡"], "answer": 2, "explanation": "ドレスデンは橋建設により景観が損なわれ、危機遺産に登録されました。" },
        { "question": "世界で初めて登録された世界遺産の一つは？", "options": ["万里の長城", "イエローストーン国立公園", "ピラミッド群", "モン・サン＝ミッシェル"], "answer": 1, "explanation": "1978年、イエローストーン国立公園は世界で最初に登録された遺産のひとつです。" },
        { "question": "パルテノン神殿は何の神を祀るために建てられた？", "options": ["ゼウス", "アテナ", "アポロン", "ポセイドン"], "answer": 1, "explanation": "パルテノン神殿はアテネの守護神・アテナを祀るために建てられました。" },
        { "question": "自由の女神像はどの国から贈られた？", "options": ["イギリス", "カナダ", "フランス", "イタリア"], "answer": 2, "explanation": "アメリカの独立100周年を記念して、フランスから贈られました。" },
        { "question": "「メサ・ヴェルデ国立公園」に残るのはどんな建築物？", "options": ["木造高床式倉庫", "洞窟住宅", "砂漠の天文台", "地下都市"], "answer": 1, "explanation": "アナサジ族が作った岩壁の洞窟住宅群が残されています。" },

        {"question": "アクロポリスの遺跡群がある都市はどこ？", "options": ["ローマ", "アテネ", "イスタンブール", "リスボン"], "answer": 1, "explanation": "アクロポリスはギリシャの首都アテネにある古代遺跡です。"},
        {"question": "グレート・バリア・リーフはどのような世界遺産に分類される？", "options": ["文化遺産", "自然遺産", "複合遺産", "無形遺産"], "answer": 1, "explanation": "グレート・バリア・リーフは世界最大のサンゴ礁で自然遺産に登録されています。"},
        {"question": "アンコール・ワットのある国はどこ？", "options": ["タイ", "ベトナム", "カンボジア", "ラオス"], "answer": 2, "explanation": "アンコール・ワットはカンボジアのシェムリアップにある寺院遺跡です。"},
        {"question": "サグラダ・ファミリアの建築家は誰？", "options": ["ミケランジェロ", "ガウディ", "ル・コルビュジエ", "モネ"], "answer": 1, "explanation": "スペインの建築家アントニ・ガウディが設計した未完の聖堂です。"},
        {"question": "世界遺産「アウシュビッツ強制収容所」はどの国にある？", "options": ["ドイツ", "ポーランド", "チェコ", "フランス"], "answer": 1, "explanation": "アウシュビッツはポーランドにあり、第二次世界大戦中の歴史を今に伝えます。"},
        {"question": "モアイ像で有名なイースター島は何によって知られる？", "options": ["火山活動", "石像群", "地下都市", "氷河地形"], "answer": 1, "explanation": "イースター島は巨大な石像モアイで世界的に有名です。"},
        {"question": "ペトラ遺跡の有名な建築様式は？", "options": ["石窟建築", "木造建築", "ガラス建築", "ピラミッド構造"], "answer": 0, "explanation": "ペトラは断崖に彫られた石窟建築で知られるヨルダンの世界遺産です。"},
        {"question": "世界遺産「アヤソフィア」は元々何として建てられた？", "options": ["宮殿", "寺院", "競技場", "墓所"], "answer": 1, "explanation": "アヤソフィアはビザンティン建築の傑作で、かつてはキリスト教の大聖堂でした。"},
        {"question": "「イエローストーン国立公園」の地質的な特徴は？", "options": ["氷河", "火山活動", "砂丘", "石灰岩の洞窟"], "answer": 1, "explanation": "イエローストーンには間欠泉や温泉などの活発な火山活動が見られます。"},
        {"question": "「フィレンツェ歴史地区」はどの分野の文化が中心？", "options": ["バロック", "ルネサンス", "ゴシック", "ロマン主義"], "answer": 1, "explanation": "フィレンツェはルネサンス文化の中心地として名高い都市です。"},
        {"question": "「古都京都の文化財」に含まれないものはどれ？", "options": ["金閣寺", "清水寺", "二条城", "厳島神社"], "answer": 3, "explanation": "厳島神社は広島県の宮島にあり、京都の遺産ではありません。"},
        {"question": "ピレネー山脈にまたがる「ガヴァルニー圏谷」は何遺産？", "options": ["文化遺産", "自然遺産", "複合遺産", "無形遺産"], "answer": 2, "explanation": "フランスとスペインにまたがる複合遺産です。"},
        {"question": "イランの「ペルセポリス」はどの文明の遺跡？", "options": ["アッシリア", "エジプト", "ペルシャ", "インダス"], "answer": 2, "explanation": "ペルセポリスは古代ペルシャ帝国の首都跡です。"},
        {"question": "「アフリカの大地溝帯」が世界遺産に含まれる理由は？", "options": ["鉱物資源", "火山群", "初期人類の痕跡", "氷河湖群"], "answer": 2, "explanation": "初期人類の化石が発見された人類史における重要な地域です。"},
        {"question": "「ロス・グラシアレス国立公園」で見られる自然現象は？", "options": ["サンゴ礁", "氷河崩壊", "砂漠化", "大潮"], "answer": 1, "explanation": "アルゼンチンのこの国立公園では氷河の大規模な崩壊が見られます。"},
        {"question": "「ヴェルサイユ宮殿」が世界遺産に登録された理由は？", "options": ["軍事施設", "宗教遺跡", "王政文化の象徴", "交通の要衝"], "answer": 2, "explanation": "ヴェルサイユ宮殿はフランス王政の栄華を象徴する文化遺産です。"},
        {"question": "モロッコの「フェズ旧市街」が有名な理由は？", "options": ["イスラム建築の保存状態", "ローマ遺跡", "港町の景観", "砂漠の都市計画"], "answer": 0, "explanation": "フェズ旧市街は迷路のような路地とイスラム建築で知られています。"},
        {"question": "「グレート・スモーキー山脈国立公園」はどの国？", "options": ["アメリカ", "カナダ", "メキシコ", "イギリス"], "answer": 0, "explanation": "アメリカにあり、生物多様性が豊かな自然遺産です。"},
        {"question": "「トンブクトゥ」が栄えた主な理由は？", "options": ["宗教的巡礼地", "金と塩の交易", "軍事拠点", "植民地行政都市"], "answer": 1, "explanation": "トンブクトゥはサハラ交易の中継地として繁栄しました。"},
        {"question": "「サン・ピエトロ大聖堂」がある都市は？", "options": ["ナポリ", "ローマ", "フィレンツェ", "ヴェネツィア"], "answer": 1, "explanation": "バチカン市国内にあるが、所在地はローマです。"},
        {"question": "「グランド・キャニオン」の主な形成要因は？", "options": ["氷河作用", "風化", "川の浸食", "火山活動"], "answer": 2, "explanation": "コロラド川の浸食によって形成された壮大な地形です。"},
        {"question": "「パレンケ遺跡」はどの文明に属する？", "options": ["インカ", "アステカ", "マヤ", "トルテカ"], "answer": 2, "explanation": "パレンケはマヤ文明の古代都市遺跡です。"},
        {"question": "「ナスカの地上絵」は何のために描かれたと考えられている？", "options": ["宗教儀式", "農業記録", "戦争計画", "文字の代用"], "answer": 0, "explanation": "宗教的な意味を持つ儀式用と考えられています。"},
        {"question": "「ドロミーティ」が世界遺産として評価された理由は？", "options": ["熱帯雨林", "石灰岩の景観美", "氷河と湖", "火山島群"], "answer": 1, "explanation": "イタリアの山岳地帯で、石灰岩の断崖や峰が美しい自然遺産です。"},
        {"question": "「ストーン・タウン」はどの文化の影響を受けている？", "options": ["中国", "アラブ", "モンゴル", "ロシア"], "answer": 1, "explanation": "タンザニアのストーン・タウンはアラブ・イスラム文化の影響が色濃い歴史都市です。"},
        {"question": "アユタヤ遺跡が栄えたのは何王朝時代？", "options": ["スコータイ朝", "アユタヤ朝", "チャクリー朝", "ランナー朝"], "answer": 1, "explanation": "アユタヤ遺跡はタイのアユタヤ王朝（14〜18世紀）の都だった場所です。"},
        {"question": "「マラケシュ旧市街」が評価される理由は？", "options": ["要塞建築", "イスラム学術遺産", "宗教的多様性", "赤土の建築群と市場文化"], "answer": 3, "explanation": "赤い日干しレンガで作られた旧市街とスーク（市場）の文化で知られます。"},
        {"question": "「ライン渓谷中流上部」で見られる文化要素は？", "options": ["ワイン生産と古城", "都市計画", "地下礼拝堂", "灯台群"], "answer": 0, "explanation": "ドイツのライン渓谷は中世の古城群とワイン文化が評価されています。"},
        {"question": "「テオティワカン遺跡」で有名な建造物は？", "options": ["太陽のピラミッド", "神殿の塔", "戦士の像", "十字の回廊"], "answer": 0, "explanation": "テオティワカンには巨大な「太陽のピラミッド」があります。"},
        {"question": "「ヴェネツィアとその潟」はなぜ世界遺産？", "options": ["鉄道文化", "干拓の技術", "水上都市の独自文化", "アルプスの眺望"], "answer": 2, "explanation": "水上都市として発展したヴェネツィアの独自文化と建築が評価されています。"},
        {"question": "「アルハンブラ宮殿」はどの文化の建築？", "options": ["ローマ", "アラブ", "フランス", "ビザンティン"], "answer": 1, "explanation": "アルハンブラ宮殿はイスラム王朝ナスル朝によって建てられました。"},
        {"question": "「バーミヤン渓谷の仏教遺跡」はなぜ注目された？", "options": ["大仏の爆破", "火山遺跡", "空中庭園", "巨大洞窟"], "answer": 0, "explanation": "タリバンによって仏像が破壊されたことで世界的に注目されました。"},
        {"question": "「スタリ・モスト」はどの国の遺産？", "options": ["クロアチア", "ボスニア・ヘルツェゴビナ", "セルビア", "モンテネグロ"], "answer": 1, "explanation": "スタリ・モスト（古い橋）はモスタルにある再建された歴史的石橋です。"},
        {"question": "「カナイマ国立公園」にある世界最大の滝は？", "options": ["ナイアガラの滝", "イグアスの滝", "エンジェルフォール", "ヴィクトリア滝"], "answer": 2, "explanation": "エンジェルフォールは979mの落差を誇る世界一高い滝です。"},
        {"question": "「コパン遺跡」はどの古代文明に属する？", "options": ["アステカ", "マヤ", "インカ", "ノルマン"], "answer": 1, "explanation": "コパンはマヤ文明の中心都市のひとつです。"},
        {"question": "「ロロペニ遺跡」はどの地域の文化に属する？", "options": ["北アフリカ", "西アフリカ", "南アフリカ", "東アフリカ"], "answer": 1, "explanation": "ロロペニ遺跡はブルキナファソにある西アフリカの石造遺跡です。"},
        {"question": "「キリマンジャロ国立公園」で知られるのは？", "options": ["大渓谷", "熱帯雨林", "火山山脈", "氷河山頂"], "answer": 3, "explanation": "赤道直下にもかかわらず、山頂に氷河が存在する山として有名です。"},
        {"question": "「イスタンブール歴史地域」は何の交差点とされる？", "options": ["宗教と政治", "東洋と西洋", "奴隷と交易", "山岳と砂漠"], "answer": 1, "explanation": "イスタンブールは東洋と西洋の文化の交差点とされています。"},
        {"question": "「ドゥルミトル国立公園」はどこの国？", "options": ["モンテネグロ", "ルーマニア", "アルバニア", "ブルガリア"], "answer": 0, "explanation": "ドゥルミトルはモンテネグロのカルスト山岳地帯にある自然遺産です。"},
        {"question": "「ハロン湾」は何によって形成された？", "options": ["火山活動", "風化浸食", "石灰岩の沈降と海水侵入", "サンゴ礁堆積"], "answer": 2, "explanation": "ハロン湾は石灰岩の沈降と海の浸食により幻想的な景観が生まれました。"},
        {"question": "「ポン・デュ・ガール」は何時代の遺構？", "options": ["古代ギリシャ", "ローマ帝国", "ビザンティン帝国", "中世フランス"], "answer": 1, "explanation": "ポン・デュ・ガールはローマ時代の水道橋として残る貴重な建築です。"},
        {"question": "「アヴィニョン歴史地区」は何で有名？", "options": ["フレスコ画", "教皇庁の宮殿", "劇場都市", "騎士団の拠点"], "answer": 1, "explanation": "アヴィニョンはかつてローマ教皇庁が置かれた場所として知られています。"},
        {"question": "「トロイア遺跡」が語られるのは何の叙事詩？", "options": ["イーリアス", "オデュッセイア", "アエネーイス", "神曲"], "answer": 0, "explanation": "ホメロスの叙事詩『イーリアス』に登場する伝説の都市です。"},
        {"question": "「バチカン市国」は世界で最も何な国？", "options": ["面積が小さい", "人口が多い", "宗教が混在する", "標高が高い"], "answer": 0, "explanation": "バチカンは面積約0.44平方kmの世界最小の独立国家です。"},
        {"question": "「チチェン・イッツァ」にある階段ピラミッドの名前は？", "options": ["ウル", "カフラー", "エル・カスティーヨ", "クフ"], "answer": 2, "explanation": "エル・カスティーヨはマヤ文明による天文と宗教を反映した建築です。"},
        {"question": "「古都奈良の文化財」に含まれないのは？", "options": ["東大寺", "薬師寺", "金閣寺", "唐招提寺"], "answer": 2, "explanation": "金閣寺は京都にあり、奈良の文化財には含まれません。"},
        {"question": "「日光の社寺」で有名な装飾は？", "options": ["見ざる聞かざる言わざる", "五重塔", "金箔貼りの仏像", "血天井"], "answer": 0, "explanation": "東照宮にある三猿は「見ざる聞かざる言わざる」として有名です。"},
        {"question": "「紀伊山地の霊場と参詣道」で登録された信仰の道は？", "options": ["お遍路道", "奥の細道", "熊野古道", "中山道"], "answer": 2, "explanation": "熊野古道は紀伊山地の霊場と結ぶ信仰の参詣道として登録されています。"},
        {"question": "「富士山」は何として世界遺産に登録されている？", "options": ["自然遺産", "文化遺産", "複合遺産", "無形遺産"], "answer": 1, "explanation": "富士山は信仰の対象と芸術の源泉として文化遺産に登録されています。"},
        {"question": "「石見銀山遺跡」が評価された主な理由は？", "options": ["銀の埋蔵量", "戦国時代の城跡", "環境との共生", "交通網の整備"], "answer": 2, "explanation": "採掘と自然環境の調和が評価されました。"},
        {"question": "「白川郷・五箇山の合掌造り集落」で有名な屋根の形状は？", "options": ["寄棟造", "入母屋造", "茅葺き切妻", "方形造"], "answer": 2, "explanation": "茅葺き切妻屋根の急勾配が特徴です。"},
        {"question": "「原爆ドーム」がある都市は？", "options": ["長崎", "東京", "広島", "大阪"], "answer": 2, "explanation": "広島の原爆ドームは世界平和の象徴として登録されています。"},
        {"question": "「明治日本の産業革命遺産」に含まれるのは？", "options": ["姫路城", "軍艦島", "平泉中尊寺", "厳島神社"], "answer": 1, "explanation": "長崎の軍艦島（端島炭鉱）が含まれています。"},
        {"question": "「ル・コルビュジエの建築作品」で日本にあるのは？", "options": ["東京国立近代美術館", "国立西洋美術館", "京都国立博物館", "金沢21世紀美術館"], "answer": 1, "explanation": "国立西洋美術館（東京・上野）はル・コルビュジエの設計による建築です。"},
        {"question": "「長崎と天草地方の潜伏キリシタン関連遺産」に含まれる文化は？", "options": ["仏教", "神道", "キリスト教", "儒教"], "answer": 2, "explanation": "江戸時代の禁教期にも信仰を守った潜伏キリシタンの文化が評価されました。"},
        {"question": "「奄美・沖縄」が世界遺産に登録された理由は？", "options": ["先史遺跡", "民俗文化", "高い生物多様性", "軍事史跡群"], "answer": 2, "explanation": "固有種や絶滅危惧種などが多く見られる生物多様性が評価されました。"},
        {"question": "「小笠原諸島」が自然遺産として評価された理由は？", "options": ["海中洞窟", "固有動植物", "火山景観", "滝群"], "answer": 1, "explanation": "他の地域と隔絶された環境により進化した固有種が多く見られます。"},
        {"question": "「知床」が評価されたポイントは？", "options": ["交通インフラ", "寒冷地農業", "海と陸をつなぐ生態系", "伝統文化の継承"], "answer": 2, "explanation": "海から陸への栄養循環を含む独自の生態系が評価されました。"},
        {"question": "「屋久島」で見られる樹齢1000年超の杉の名前は？", "options": ["縄文杉", "弥生杉", "白谷杉", "神代杉"], "answer": 0, "explanation": "縄文杉は屋久島の象徴的存在です。"},
        {"question": "「姫路城」の別名は？", "options": ["金鶴城", "白鷺城", "銀鳳城", "赤松城"], "answer": 1, "explanation": "白漆喰の美しい外観から「白鷺城」と呼ばれます。"},
        {"question": "「平泉」の遺産群で有名な金色堂がある寺は？", "options": ["中尊寺", "毛越寺", "無量光院", "観自在王院跡"], "answer": 0, "explanation": "中尊寺金色堂は奥州藤原氏の栄華を今に伝える仏堂です。"},
        {"question": "「富岡製糸場」が示す日本の歴史は？", "options": ["鎌倉仏教の興隆", "幕末の外交", "近代工業化の始まり", "平安貴族文化の隆盛"], "answer": 2, "explanation": "富岡製糸場は日本の産業近代化の先駆けとして世界遺産に登録されました。"},
        {"question": "「北海道・北東北の縄文遺跡群」が示すのは？", "options": ["弥生時代の稲作", "縄文人の定住と精神文化", "古墳時代の豪族政治", "江戸時代の武家社会"], "answer": 1, "explanation": "縄文時代の定住生活と宗教観を示す貴重な遺構です。"},
        {"question": "「百舌鳥・古市古墳群」で最大の古墳は？", "options": ["応神天皇陵", "仁徳天皇陵", "継体天皇陵", "仲哀天皇陵"], "answer": 1, "explanation": "仁徳天皇陵は日本最大規模の前方後円墳です。"},
        {"question": "「上賀茂神社」と「下鴨神社」がある都市は？", "options": ["奈良", "東京", "京都", "伊勢"], "answer": 2, "explanation": "上賀茂・下鴨神社はいずれも京都の世界遺産「古都京都の文化財」に含まれます。"},
        {"question": "「琉球王国のグスク及び関連遺産群」に含まれる城は？", "options": ["首里城", "大阪城", "松本城", "松山城"], "answer": 0, "explanation": "首里城は琉球王国の中心的な政治・文化の拠点でした。"},
        {"question": "「厳島神社」が建つのはどの地形？", "options": ["砂丘", "湿地", "海上", "山頂"], "answer": 2, "explanation": "厳島神社は満潮時に海に浮かんで見えるように建てられています。"},
        {"question": "「古都京都の文化財」に含まれる寺は？", "options": ["金閣寺", "中尊寺", "善光寺", "瑞巌寺"], "answer": 0, "explanation": "金閣寺（鹿苑寺）は京都の文化遺産群のひとつです。"},
        {"question": "「石見銀山」がある都道府県は？", "options": ["島根県", "山口県", "広島県", "鳥取県"], "answer": 0, "explanation": "石見銀山は島根県大田市に位置します。"},
        {"question": "「姫路城」が世界遺産に登録されたのはいつ？", "options": ["1993年", "2000年", "2006年", "2012年"], "answer": 0, "explanation": "姫路城は1993年に日本で初めての世界文化遺産のひとつとして登録されました。"},
   ],
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
    col1, col2, col3, col4 = st.columns(4)
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
    with col4:
        if st.button("世界遺産"):
            st.session_state.genre = "世界遺産"
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