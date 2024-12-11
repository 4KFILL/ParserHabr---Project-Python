import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import os

keywords = input("Введите ключевые слова через запятую: ").split(", ") # список ключевых слов
if os.path.exists('habr.txt'): os.remove('habr.txt')

class ArticleParser(mp.Process):
    def __init__(self, links_queue, keywords,**kwargs):
        mp.Process.__init__(self, **kwargs)
        self.link = links_queue.get()  # взяли ссылку из очереди
        self.keywords = keywords


    def parse_articles_in_array(self):

        response = requests.get(self.link).text
        soup = BeautifulSoup(response, 'lxml')
        block_h2 = soup.find_all('h2')

        for h2 in block_h2:
            text = h2.text.strip().lower()
            for keyword in self.keywords:
                if keyword.lower() in text:
                    self.parse_article_in_array(h2)


    def parse_article_in_array(self, h2):
        article_link = h2.find('a')['href']
        link_support = 'https://habr.com'
        full_link = link_support + article_link
        article_response = requests.get(full_link).text
        article_soup = BeautifulSoup(article_response, 'lxml')
        try:
            article_title = article_soup.find('h1', class_='tm-title tm-title_h1').text.strip()
            article_text = article_soup.find('div', class_='tm-article-body').text.strip()
            print(f"Ссылка на статью: {full_link}")
            print(f"Заголовок статьи: {article_title}")
            print("Далее...")
            self.write_to_file(article_title, article_text)
        except:
            pass

    def write_to_file(self, article_title, article_text):
        file = open('habr.txt', 'a', encoding='utf-8')
        file.write(f"- Заголовок статьи: {article_title}\n")
        file.write(f"- Текст статьи: {article_text}\n")
        file.write("\n")
        file.write("#####\n")
        file.write("\n")
        file.close()
        exit(0)

    def run(self):
        self.parse_articles_in_array()

if __name__ =='__main__':
    arr_url = [
    r"https://habr.com/ru/articles/",
    r"https://habr.com/ru/articles/page2/",
    r"https://habr.com/ru/articles/page3/",
    r"https://habr.com/ru/articles/page4/",
    r"https://habr.com/ru/articles/page5/",
    r"https://habr.com/ru/articles/page6/",
    r"https://habr.com/ru/articles/page7/",
    r"https://habr.com/ru/articles/page8/",
    r"https://habr.com/ru/articles/page9/",
    r"https://habr.com/ru/articles/page10/",
    r"https://habr.com/ru/articles/page11/",
    r"https://habr.com/ru/articles/page12/",
    r"https://habr.com/ru/articles/page13/",
    r"https://habr.com/ru/articles/page14/",
    r"https://habr.com/ru/articles/page15/",
    r"https://habr.com/ru/articles/page16/",
    r"https://habr.com/ru/articles/page17/",
    r"https://habr.com/ru/articles/page18/",
    r"https://habr.com/ru/articles/page19/",
    r"https://habr.com/ru/articles/page20/",
    r"https://habr.com/ru/articles/page21/",
    r"https://habr.com/ru/articles/page22/",
    r"https://habr.com/ru/articles/page23/",
    r"https://habr.com/ru/articles/page24/",
    r"https://habr.com/ru/articles/page25/",
    r"https://habr.com/ru/articles/page26/",
    r"https://habr.com/ru/articles/page27/",
    r"https://habr.com/ru/articles/page28/",
    r"https://habr.com/ru/articles/page29/",
    r"https://habr.com/ru/articles/page30/",
    r"https://habr.com/ru/articles/page31/",
    r"https://habr.com/ru/articles/page32/",
    r"https://habr.com/ru/articles/page33/",
    r"https://habr.com/ru/articles/page34/",
    r"https://habr.com/ru/articles/page35/",
    r"https://habr.com/ru/articles/page36/",
    r"https://habr.com/ru/articles/page37/",
    r"https://habr.com/ru/articles/page38/",
    r"https://habr.com/ru/articles/page39/",
    r"https://habr.com/ru/articles/page40/",
    r"https://habr.com/ru/articles/page41/",
    r"https://habr.com/ru/articles/page42/",
    r"https://habr.com/ru/articles/page43/",
    r"https://habr.com/ru/articles/page44/",
    r"https://habr.com/ru/articles/page45/",
    r"https://habr.com/ru/articles/page46/",
    r"https://habr.com/ru/articles/page47/",
    r"https://habr.com/ru/articles/page48/",
    r"https://habr.com/ru/articles/page49/",
    r"https://habr.com/ru/articles/page50/"
    ] #ссылки на страницы с новостями
    links_queue = mp.Queue()  # готовим очередь со ссылками
    for link in arr_url:
        links_queue.put(link)
    processess = []
    for i in range(links_queue.qsize()):
        parser = ArticleParser(links_queue, keywords)
        parser.run()
        processess.append(parser)
    while len(processess) > 0:
        for i in range(len(processess)):
            if processess[i].is_alive():
                pass #активные оставляем
            else: #если процесс завершился - выкидываем
                processess.remove(processess[i])
                break

if os.path.exists('habr.txt'):
    print(f"Данные по ключевым словам {keywords} находятся в файле habr.txt") 
else:
    print(f"Данные по ключевым словам {keywords} не найдены...")