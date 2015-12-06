import os
from grab import Grab

def download():
    url='http://novel18.syosetu.com/n3746ce/'
    g=Grab()
    resp = g.go(url)
    urls = g.doc('//*[@id="novel_color"]/div/dl/dd/a')
    for url in urls:
        temp='http://novel18.syosetu.com/'+ url.attr('href')
        name=url.text()
        print(temp,name)



if __name__ == '__main__':
    download()
