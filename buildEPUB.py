#_*_coding:utf-8_*_
import os
import shutil
from lxml import etree

#书籍信息
title='test book'
creator='scturtle'
description='blablablabla'

# 临时工作目录
if os.path.exists('tmp'):
    shutil.rmtree('tmp')
os.mkdir('tmp')

# tmp/mimetype 文件
tf=open('tmp/mimetype','w')
tf.write('application/epub+zip')
tf.close()

# tmp/META-INF 目录
os.mkdir('tmp/META-INF')
# tmp/META-INF/container.xml 文件, 指定opf文件
tf=open('tmp/META-INF/container.xml','w')
tf.write('''<?xml version="1.0" encoding="UTF-8" ?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles> <rootfile full-path="OPS/content.opf" media-type="application/oebps-package+xml"/> </rootfiles>
</container>
''')
tf.close()

# tmp/OPS 目录 主要存在这里
os.mkdir('tmp/OPS')

# 封面图片
if os.path.isfile('cover.jpg'):
    shutil.copyfile('cover.jpg','tmp/OPS/cover.jpg')
    print('Cover found!')

# 准备opf文件信息,包含目录文件封面文件信息
opfcontent='''<?xml version="1.0" encoding="UTF-8" ?>
<package version="2.0" unique-identifier="PrimaryID" xmlns="http://www.idpf.org/2007/opf">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
%(metadata)s
<meta name="cover" content="cover"/>
</metadata>
<manifest>
%(manifest)s
<item id="ncx" href="content.ncx" media-type="application/x-dtbncx+xml"/>
<item id="cover" href="cover.jpg" media-type="image/jpeg"/>
</manifest>
<spine toc="ncx">
%(ncx)s
</spine>
</package>
'''
dc='<dc:%(name)s>%(value)s</dc:%(name)s>'
item="<item id='%(id)s' href='%(url)s' media-type='application/xhtml+xml'/>"
itemref="<itemref idref='%(id)s'/>"

metadata='\n'.join([
        dc % {'name':'title','value':title},
        dc % {'name':'creator','value':creator},
        dc % {'name':'description','value':description},
        ])

manifest=[]
ncx=[]

# 根据每章节生成内容, txt => html
htmls= os.listdir('王国へ続く道/')
for html in htmls:
    file=open('王国へ続く道/'+html,'r',encoding='utf-8')
    content=file.read()
    content=bytes(bytearray(content, encoding='utf-8'))
    selector = etree.HTML(content)
    subt=selector.xpath('//*[@class="novel_subtitle"]/text()')
    subt=''.join(subt).replace(r'/3000','')
    data=selector.xpath('//*[@id="novel_honbun"]/text()')
    ndata=[]
    for d in data:
        ndata.append(d+r'<br />')
    ndata=''.join(ndata).replace(r'/3000','')
    print(ndata)
    tf=open('tmp/OPS/'+html,'w',encoding='utf-8')
    tf.write('''<html><head>
<title>%(title)s</title>
</head><body><h2>%(title)s</h2><div>
''' %{'title':subt})
    tf.write(''.join(ndata))
    tf.write('</div></body></html>')
    tf.close()
    id=html.split('.')[0]
    html=html.strip('.html')
    manifest.append(item % {'id':id, 'url':html+'.html'})
    ncx.append(itemref % {'id':id})

manifest='\n'.join(manifest)
ncx='\n'.join(ncx)

# 生成opf文件
tf=open('tmp/OPS/content.opf','w',encoding='utf-8')
tf.write(opfcontent %{'metadata':metadata,'manifest':manifest,'ncx':ncx,})
tf.close()

# 准备目录文件ncx内容
ncx='''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">
<head>
  <meta name="dtb:uid" content=" "/>
  <meta name="dtb:depth" content="-1"/>
  <meta name="dtb:totalPageCount" content="0"/>
  <meta name="dtb:maxPageNumber" content="0"/>
</head>
 <docTitle><text>%(title)s</text></docTitle>
 <docAuthor><text>%(creator)s</text></docAuthor>
<navMap>
%(navpoints)s
</navMap>
</ncx>
'''

navpoint='''<navPoint id='%s' class='level1' playOrder='%d'>
<navLabel> <text>%s</text> </navLabel>
<content src='%s'/></navPoint>'''

navpoints=[]
for i,txt in enumerate(htmls):
    navpoints.append(navpoint % (txt,i+1,txt,txt))

# 生成目录文件
tf=open('tmp/OPS/content.ncx','w',encoding='utf-8')
tf.write(ncx % {
    'title':title,'creator':creator,
    'navpoints':'\n'.join(navpoints)})
tf.close()

# 打个压缩包
from zipfile import ZipFile
epubfile=ZipFile('book.epub','w')
os.chdir('tmp')
for d,ds,fs in os.walk('.'):
    for f in fs:
        epubfile.write(os.path.join(d,f))
epubfile.close()

print('Finished!')