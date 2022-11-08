from bs4 import BeautifulSoup
import requests 
import pandas as pd
import time 
import random
from fp.fp import FreeProxy

start=time.time()

headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0"}
keywords=["TCR","BCR","T CELL","B CELL","NKC","CD4","CD8","DEEP LEARNING","MACHINE LEARNING","HLA"]
base_url="https://www.nature.com"
header_df=["Article","Summary","Authors","Date","Access","Figure","Link paper",
          "TCR","BCR","T CELL","B CELL","NKC","CD4","CD8","DEEP LEARNING","MACHINE LEARNING","HLA"]
print("Selected keywords are:",*keywords)

proxies={}
for i in range(20):#obtain proxies to access nature.com so we don't get bloked
    proxy = FreeProxy(timeout=1,anonym=True,rand=True).get()
    proxies[i]=proxy

print("Done gathering proxies")

def cook_soup(url): #get soup of the page and the page to get status
    page = requests.get(url,headers=headers,proxies=proxies)
    soup = BeautifulSoup(page.content, "html.parser")
    return page,soup
    
def process_date(date): #process date of the article into accessebility and date itself
    date=str(date.text).split(sep="\n")
    access=date[2]
    if access=="":#if it does not say anything, the article is not free
        access="Payed Access"
    date=date[3]
    return date,access
    
def process_abstract(url_abs,keywords): #process abstract of the paper and get the keywords
    keyword_bin=[]
    sleep=random.randint(1,5) #even though we are using proxies, it is never a bad idea to use double protection
    time.sleep(sleep)
    page = requests.get(url_abs,headers=headers,proxies=proxies)
    soup = BeautifulSoup(page.content, "html.parser")
    abstract = soup.find("div",class_="c-article-section__content")
    abstract=abstract.text.strip().upper()
    for word in keywords:
        if word in abstract:
            keyword_bin.append(1)
        else:
            keyword_bin.append(0)
    return keyword_bin
    
def get_articles(soup,url): #loop through the table to get articles on the webpage
    all_arts=[]
    results = soup.find(id="new-article-list")
    articles = results.find_all("li", class_="app-article-list-row__item")
    for art in articles:
        article = art.find("h3", class_="c-card__title")
        summmary = art.find("div", class_="c-card__summary u-mb-16 u-hide-sm-max")
        authors = art.find("ul", class_="c-author-list c-author-list--compact c-author-list--truncated")
        date_in=art.find("div", class_="c-card__section c-meta")
        date,access=process_date(date_in)
        pic=art.find("img")#,src="c-card__image")
        link_art=art.find("a",class_="c-card__link u-link-inherit")
        link_art=base_url+str(link_art.attrs["href"])
        keywords_art=process_abstract(link_art,keywords)
        row_data=[article.text.strip(),summmary.text.strip(),
                  authors.text.strip(),date,access,
                  "https:"+pic.attrs["src"],link_art]
        row_data.extend(keywords_art)
        all_arts.append(row_data)
    print("url:",url,"finished")
    return all_arts
    
    
n=True
p=1
max_p=100 #define max iter so we don't loop forever in case error is not 404 
rows_df=[header_df]# add header to the future df

while n:
    sleep=random.randint(1,5)
    time.sleep(sleep)
    URL="https://www.nature.com/ni/research-articles?searchType=journalSearch&sort=PubDate&type=article&year=2022&page="+str(p)#loop over pages 
    page,soup=cook_soup(URL)
    print(p,page.status_code)# check if page is not a 404 Not Found
    
    p+=1
    
    if p>max_p or page.status_code==404: # if the webapge is Not Found we stop iterating since we reached the end of possible pages 
        n=False
        break
    article_list=get_articles(soup,URL)
    rows_df.extend(article_list)
    
#maybe implement asynch io (multi threading)
#not javascript page so no selenium 
# quite simple web page and open access area of nature, so no hard blockers were identified


print("Number of retrieved articles:",len(rows_df)-1)

df = pd.DataFrame(rows_df[1:], columns = rows_df[0])# turn the list of lists into a df

df.to_csv("../dataset/2022_immuno_articles.csv",index=False) # save it to dataset folder 
end=time.time()
print("All done in:",end-start,"seconds")
