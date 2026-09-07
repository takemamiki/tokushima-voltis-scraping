"""
main.py
find_vortis_schedule.py → fetch_match.py → parse_match.py → save_data.py を
1本につなげて、J2の終了済み試合を自動でCSVに保存する。
"""

import time
from urllib.parse import urlparse, parse_qs

from find_vortis_schedule import fetch_schedule_page, find_finished_j2_urls
from fetch_match import fetch_match_html, WAIT_SECONDS
from parse_match import parse_match
from save_data import save_match_data

def extract_game_id(url: str) -> str:
    """
    試合結果ページのURLから、game=から始まる試合IDだけを取り出す。
    """
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query)
    return query.get("game", [None])[0]


if __name__ == "__main__":
    soup = fetch_schedule_page()
    urls = find_finished_j2_urls(soup)

    print(f"見つかった試合数: {len(urls)}")

    for url in urls:
        game_id = extract_game_id(url)
        print(f"取得中: {game_id}")

        html = fetch_match_html(url)
        match_data = parse_match(html)
        match_data["game_id"] = game_id

        save_match_data(match_data)

        time.sleep(WAIT_SECONDS)

    print("全試合の保存が完了しました")



    