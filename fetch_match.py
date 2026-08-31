"""
fetch_match.py
Jリーグ公式サイトから、指定した

役割：URLにアクセスしてHTMLを取ってくるだけ。
    中身を読み取る（パース）のは parse_match.py の役割
"""

import requests
import time

# robots.txtの "User-Agent: spider" グループを避けるため、
# 自分の名前をはっきり名乗る（Disallow: / の対象にしない）
HEADERS = {
    "User-Agent": "TakemaMiki-LearningBot/1.0 (personal project; contact:[https://github.com/takemamiki])"}

# アクセス間隔（秒）。サーバーに負荷をかけないよう、
# 複数試合を連続取得するときは必ずこの秒数以上あける。
WAIT_SECONDS = 3


def fetch_match_html(url: str) -> str:
    """
    指定したURLにアクセスして、HTML本文を文字列で返す。
    失敗した場合は None を返す。
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # ステータスコードが200番台以外ならエラーにする
        response.encoding = "utf-8"  # 文字化け対策
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"取得失敗: {url}")
        print(f"エラー内容: {e}")
        return None

if __name__=="__main__":
    # 徳島ヴォルティス公式サイトの試合結果ページ（第4節）を試しに取得してみる
    test_url = "https://www.vortis.jp/game/match/result.php?year=2026&category=game&game=2026082919"

    print(f"アクセス中: {test_url}")
    html = fetch_match_html(test_url)

    if html:
        # 取得できたHTMLをファイルに保存して、中身を確認できるようにする
        with open("data/sample_vortis_match.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("取得成功。data/sample_vortis_match.html に保存しました。")
        print(f"HTMLの長さ: {len(html)} 文字")
    else:
        print("取得に失敗しました。") 

    time.sleep(WAIT_SECONDS)
