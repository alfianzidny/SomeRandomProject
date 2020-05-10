from bs4 import BeautifulSoup
import requests
import sys

def main():
    
    url = "https://thehackernews.com"

    page = requests.get(url)
    soup = page.text
    soup_news = BeautifulSoup(soup, 'lxml')

    result_temp = soup_news.find_all("div", {'class': 'blog-posts clear'})

    f = open("hasil_web.txt", 'w')

    for x in result_temp:
        link_main = x.find_all('div', {'class': 'body-post clear'})
        
        for index in link_main:
            link_page = index.find('a')['href']
            title = index.find('h2', {'class':'home-title'})
            posted = index.find('div', {'class':'item-label'})
            tanggal = posted.text[1:15]
            author = posted.text[16:32]
            print("Title = " + title.text)
            print("Link = " + link_page)
            print("Author = " + author)
            print("Date = " + tanggal)
            print("-"*15)
            f.write(title.text + ',' + link_page + '\n')
            

if __name__ == "__main__":
    main()
