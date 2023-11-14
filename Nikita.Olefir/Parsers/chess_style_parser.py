import requests
from bs4 import BeautifulSoup

def parser(url:str):
    res = requests.get(url=url)
    soup = BeautifulSoup(res.text,"html.parser")
    my_ul = soup.find('ul', class_=None, role=None)
    li_openings =my_ul.find_all('li')
    game_styles = []
    for opening in li_openings:    
        game_styles.append(li_openings.string)
    print(game_styles)

if __name__ == "__main__":
    parser(url="https://chessfox.com/13-different-types-of-chess-openings/#Hypermodern-Openings")


