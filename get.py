import os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
from grab import Grab
import urllib.request

def download():
    pool = ThreadPool(4)
    url='http://novel18.syosetu.com/n3746ce/'
    main_page=Grab()
    main_page.go(url)
    title=main_page.doc('//*[@id="novel_color"]/p').text()
    path='%s/' %title
    main_page.doc.save(path+'main.html')
    urls_xpath = main_page.doc('//*[@id="novel_color"]/div/dl/dd/a')
    i=1
    urls=[]
    dict={}
    for url in urls_xpath:
        urls.append('http://novel18.syosetu.com'+ url.attr('href'))
        key= url.attr('href').split('/')[2]
        dict[key]=url.text().replace('/',' ')
    print(dict)
    def pages(page_url):
        num=page_url.split('/')[4]
        f = urllib.request.urlopen(page_url)
        data = f.read()
        with open(path+'%04u.%s.html'%(int(num),dict[num]), "wb") as code:
            code.write(data)
        print(num,dict[num])
    pool.map(pages,urls)




if __name__ == '__main__':
    download()
