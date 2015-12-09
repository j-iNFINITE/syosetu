#_*_coding:utf-8_*_
from ebooklib import epub
import os
from lxml import etree
book = epub.EpubBook()
path='temp/'
files=os.listdir('temp/')
if 'main.html' in files:
    f=open(path+'main.html','r',encoding='utf-8').read()
    content=bytes(bytearray(f, encoding='utf-8'))
    selector = etree.HTML(content)
    title=selector.xpath(u'//*[@id="novel_color"]/p/text()')[0].strip()  #标题 去除全角空格
    ID=selector.xpath('//*[@id="novel_color"]/div[3]/dl[1]/dd/a/@href')[0].split('/')[1]  # 书籍ID
    author=selector.xpath('//*[@id="novel_color"]/div[1]/a/text()')[0].replace('\u3000','')  #作者
    book.set_identifier(ID)
    book.set_title(title)
    book.set_language('jp')
    book.add_author(author)
    main = epub.EpubHtml(title='简介',file_name='main.xhtml',lang='jp')
    main.content= '''<h1 align="center">%s</h1><h3 align="right">%s</h3><h3 align="right">Eli生成</h3>
    ''' %(title,author)+''.join(selector.xpath('//*[@id="novel_ex"]/text()')).replace('\n','</p><p>')
    book.add_item(main)
    book.toc = [epub.Link('main.xhtml', '简介', 'main')]
    book.spine = ['nav']
    book.spine.append(main)
    files.remove('main.html')
# create chapter
for i in range(len(files)):
    c_num=str(i+1)
    c_title=files[i].split('.')[1]
    f=open(path+files[i],'r',encoding='utf-8').read()
    content=bytes(bytearray(f, encoding='utf-8'))
    selector = etree.HTML(content)
    c_content=''.join(selector.xpath('//*[@id="novel_honbun"]/text()')).replace('\u3000',' ').replace('\n','<br>')
    locals()['c'+str(i+1)]=epub.EpubHtml(title=c_title,file_name='c'+c_num+'.xhtml',lang='jp')
    locals()['c'+str(i+1)].content= '''<h1 align="center">%s</h1>
    ''' %(c_title)+''.join(selector.xpath('//*[@id="novel_honbun"]/text()')).replace('\u3000',' ').replace('\n','<br>')
    book.add_item(locals()['c'+str(i+1)])
    book.toc.append(epub.Link('c'+c_num+'.xhtml',c_title,'c'+str(i+1)))
    book.spine.append(locals()['c'+str(i+1)])
    print(i)

# c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml', lang='hr')
# c1.content=u'<h1>Intro heading</h1><p>Žaba je skočila u baru.</p>'
#
# # add chapter
# book.add_item(c1)
#
# define Table Of Contents

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
book.add_item(nav_css)

# basic spine

# write to the file
epub.write_epub(title+'.epub', book, {})