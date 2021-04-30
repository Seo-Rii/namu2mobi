from core.namu2html import namu2html
import os
import base64

try:
    os.remove('proc/raw')
except:
    pass

try:
    os.makedirs(os.path.join('proc/raw'))
except OSError as e:
    pass

mode = 1
chunkSize = 10000
dbFile = open("namu.json")
pageDB = dict()
buff = ""
isEscape = False
cnt = 0
while 1:
    chunk = dbFile.read(chunkSize)
    if chunk == '':
        break
    for word in chunk:
        if mode == 1 and (word == '[' or word == ']'):
            pass
        elif mode == 1 and (word == '{'):
            pageDB = dict()
        elif mode == 1 and (word == '}'):
            if not 'title' in pageDB:
                continue
            if '나무위키:' in pageDB['title'] or '사용자:' in pageDB['title'] or '분류:' in pageDB['title'] or '파일:' in pageDB[
                'title'] or '휴지통:' in pageDB['title'] or '위키운영:' in pageDB['title'] or '파일휴지통:' in pageDB[
                'title'] or '더미:' in pageDB['title']:
                continue
            try:
                with open(os.path.join('proc', 'raw', base64.b32encode(pageDB['title'].encode("UTF-8")).decode()),
                          'w', encoding='utf-8') as w:
                    w.write(pageDB['text'])
            except:
                print('Error while processing! Document "%s" will be not processed.' % pageDB['title'])
        elif mode == 1 and (word == '"') and not isEscape:
            mode = 2
            buff = ""
        elif mode == 2 and (word == '"') and not isEscape:
            mode = 3
            dName = buff.encode("utf-8").decode("unicode_escape")
        elif mode == 3 and (word == '"') and not isEscape:
            mode = 4
            buff = ""
        elif mode == 4 and (word == '"') and not isEscape:
            mode = 1
            pageDB[dName] = buff.encode("utf-8").decode("unicode_escape")
        elif mode == 3 and (word == '['):
            mode = 5
        elif mode == 5 and (word == ']'):
            mode = 1
        else:
            buff += word
            isEscape = False
            if word == '\\':
                isEscape = True
dbFile.close()
