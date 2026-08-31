"""
parse_match.py
fetch_match.py が取得したHTMLから、スコア・チーム名・得点者を抜き出す。

役割：HTMLの中から欲しい情報だけを見つけて取り出すこと。
    サイトにアクセスするのは fetch_match.py の役目。
"""

from bs4 import BeautifulSoup

with open("data/sample_match.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scores = soup.find_all("p", class_="o-page-header__match-score")

home_score = scores[0].get_text(strip=True)
away_score = scores[1].get_text(strip=True)

club_names = soup.find_all("p", class_="o-page-header__club-name", attrs={"data-media": "pc"})
home_club = club_names[0].get_text(strip=True)
away_club = club_names[1].get_text(strip=True)

score_lists = soup.find_all("div", class_="o-page-header__player-score-list")

scorers = []
minutes = []
for score_list in score_lists:
    player_links = score_list.find_all("a", class_="o-page-header__player-score-link")
    for link in player_links:
        scorers.append(link.get_text(strip=True))

    score_p_tags = score_list.find_all("p", class_="a-typography--fw-semibold")
    for tag in score_p_tags:
        minutes.append(tag.get_text(strip=True))

match_data = {
    "home_club": home_club,
    "away_club": away_club,
    "home_score": home_score,
    "away_score": away_score,
    "scorers": scorers,
    "minutes": minutes,
}

if __name__ == "__main__":
    print(match_data)