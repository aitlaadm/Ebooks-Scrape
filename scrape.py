import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree
import sys 
class ebookScrape():
    def __init__(self,page,**kwargs):
        super(ebookScrape,self).__init__(**kwargs)
        self.page=int(page)
        
    def start_request(self):
        for p in range (0,self.page):
            url=f"https://books.toscrape.com/catalogue/page-{p+1}.html"
            webpage=requests.get(url)
            self.parse(webpage)
            
    def parse(self,webpage):
        soup = BeautifulSoup(webpage.content, "html.parser") 
        dom = etree.HTML(str(soup))
        
        titre=dom.xpath("//article/h3/a/@title")
        list_prix=dom.xpath('//article/div[@class="product_price"]/p[1]/text()')
        list_instock=dom.xpath('//article/div[@class="product_price"]/p[2]/text()')
        list_rating=dom.xpath('//article/p/@class')
        
        instock=[]
        for i in list_instock:
            item=i.replace('\n','').replace(' ','')
            if item != '':
                instock.append(item)

        prix=[]
        for p in list_prix:
            prix.append(float(p[1:]))
            
        rating=[]
        for i in list_rating:
            
            item=i.split(' ')[1]
            match item:
                case "One":
                    item=1
                case "Two":
                    item=2
                case "Three":
                    item=3
                case "Four":
                    item=4
                case "Five":
                    item=5
                case _:
                    item=0
                
            rating.append(item)
            
        data={
            'titre':titre,
            'prix':prix,
            'instock': instock,
            'rating':rating
        }
        old_df=pd.read_csv("output.csv")
        df=pd.DataFrame(data)
        
        pd.concat([old_df,df]).to_csv("output.csv",index=False)

        return data

        
if __name__=="__main__":
    page=sys.argv[1]
    p = ebookScrape(page)
    p.start_request()