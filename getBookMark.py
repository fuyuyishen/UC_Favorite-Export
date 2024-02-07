import json,requests,time
#登录UC云找到cookie和 x-csrf-token
host = f'https://cloud.uc.cn/api/bookmark/listdata'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection': 'Keep-Alive',
    'origin': 'https://cloud.uc.cn',
    'referer': 'https://cloud.uc.cn/home/phone',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'x-csrf-token': 'PiB4rOtD9HjM7xjQh48up2DQ',
    'cookie': r"cna=GHYaHvxTcWACAdoFAQioETNV; xlly_s=1; _UP_A4A_11_=wb9621d0a65f4f52acab64cf4d034bd0; _UP_D_=pc; isg=BG5utZLUh5tYt_P_72WJwVpQv8QwbzJpvzs3pZg0QXEsew_VAPudeU0yN-eXoyqB; csrfToken=PiB4rOtD9HjM7xjQh48up2DQ; _UP_28A_52_=54; st=st9626202ddgtlhyt7l5v56ve1z5rvjq; st.sig=pSKx6pRZB34iCW62F9B0yRSjB2ddc_sLv8H08kTIBsA; token=d385a2f6aa61d208586f218f5582fc8d; token.sig=XCv6p-dsxDrkIq-UEnXuWYDCncZ-wyKYjvI15Q7qv-M; nick_name=%E9%AA%8B%E6%80%80%E5%BE%A1%E9%A2%A8; uid=undefined; tfstk=f7fsskscscm1RuKYbNUFRRSgzzOb8GNP6qTArZhZkCd9GZIwYh-4SZWIMiKF_KRTjItvviDZ_nRNGMshxG7Nus6nGabc_PA4SCbMiIEz47rPSNA0S41sZ1OK9EQpknKTzjmfQIEz4Woh2qVWMOzJqW8NJHYXWxKODpKpxEl9MhpxvvLJvnL2PJV-lv77AXcEMPprWXuQ3-5BJoYf5gTHJ6TMC3ppAjLfOF962NC9gHXBJ65BUpu4WBQlLGLBN5ik59QW6E10yxtXh1ABkGNoPHC1l69GL4GPRKt1p1pIkjQpMhpPhGZsIhBNALYppqNk8g-dS1BQoDQO4hO9JpP8PwpA4HcyVU-Kh72rMetzRyMmnmYovXSt73WwBeY6LyaIXtv9-etzRyMmndLH5UzQRcBc."
}
session = requests.session()

count=0

def get_text(guid):
    global text
    global count
    for i in range(1,200):	#假设最多加载200页,有200多页书签的话改这里
        time.sleep(0.1)
        post_data={'cur_page': i, 'type': "phone", 'dir_guid': str(guid)}
        response = session.post(host, headers=headers,data=post_data).json()
        print(f'dir_guid: {guid}  cur_page:{i} ')
        if response['msg']!='ok':
            print(f"i:{i},quit{response['msg']}")
            break
        try:
            data=response['data']['list']
            print(f'i:{i}')
        except:
            print('error')
            continue
        for book in data:
            if book['is_directory']==1:	#如果是书签目录，则递归调用，相当于DFS
                print('it is a directory')
                bk=f"\t<DT><H3>{book['name']}</H3>\n\t<DL><p>\n"
                text+=bk
                get_text(book['guid'])	#这里是递归遍历目录
                text+="\t</DL><p>\n"
            else:
                bk=f"\t<DT><A HREF=\"{book['origin_url']}\">{book['title']}</A>\n"
                count=count+1
                text+=bk
        
        if not response['data']['meta']['has_last_page']:
            print(f"本页结束")
            break

with open('bookmark.html',mode='w',encoding='utf-8') as f:
    text='''<!DOCTYPE NETSCAPE-Bookmark-file-1>
			<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
			<TITLE>Bookmarks</TITLE>
			<H1>Bookmarks</H1>
			<DL><p>
			'''
    f.write(text)
    text=""
    get_text('0')
    f.write(text+'</DL><p>')
    print(f'生成书签总数 {count}')
