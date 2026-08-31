"""
find_vortis_schedule.py
徳島ヴォルティス公式サイトの日程一覧ページから、終了済みJ2リーグ試合のURLを集める。

役割：一覧ページを取得し、終了済みのJ2リーグ試合だけを見分けて、
    各試合結果ページ（result.php)のURLをリストとして作ること。
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SCHEDULE_URL = "https://www.vortis.jp/game/match/"

HEADERS = {
    "User-Agent": "TakemaMiki-LearningBot/1.0 (personal project; contact:https://github.com/takemamiki)"
}

def fetch_schedule_page() -> BeautifulSoup:
    """
    日程一覧ページを取得し、BeautifulSoupオブジェクトとして返す。
    """
    response = requests.get(SCHEDULE_URL, headers=HEADERS, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def find_finished_j2_urls(soup: BeautifulSoup) -> list:
    """
    日程一覧ページのsoupから、終了済みのJ2リーグ試合のresult.php URLだけをリストで返す。
    """
    match_urls = []
    matches = soup.find_all("div", class_="contents")

    for match in matches:
        score_tag = match.find("div", class_="score")

        if score_tag is None:
            continue

        score_text = score_tag.get_text(strip=True)

        if score_text == "":
            continue

        link_tag = match.find(
            "a",
            href=lambda href: href and "result.php" in href and "category=game" in href
        )

        if link_tag is None:
            continue

        relative_url = link_tag.get("href")
        full_url = urljoin(SCHEDULE_URL, relative_url)
        match_urls.append(full_url)

    return match_urls

if __name__ == "__main__":
    soup = fetch_schedule_page()
    urls = find_finished_j2_urls(soup)

    print(f"見つかった試合数: {len(urls)}")
    for url in urls:
        print(url)