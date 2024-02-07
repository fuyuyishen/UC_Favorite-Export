import json,requests,time

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
    'cookie': r"cna=GHYaHvxTcWACAdoFAQioETNV; xlly_s=1; _UP_A4A_11_=wb9621d0a65f4f52acab64cf4d034bd0; _UP_D_=pc; csrfToken=PiB4rOtD9HjM7xjQh48up2DQ; _UP_28A_52_=54; token=d385a2f6aa61d208586f218f5582fc8d; token.sig=XCv6p-dsxDrkIq-UEnXuWYDCncZ-wyKYjvI15Q7qv-M; nick_name=%E9%AA%8B%E6%80%80%E5%BE%A1%E9%A2%A8; uid=undefined; isg=BFpa8Z1465amZmc7s4G1fe78qwB8i95lqweD4WTTwu241_oRTBlgdSAko6PLB1b9; _UP_F7E_8D_=mgOWEX820Xcx1k2hMHC%2FLpixwrh8ip%2BNtFTrsCwdB2VI4obTezP6cprugJ6xbq77EUez5D%2BmyE%2BSQoLatAnnV6vsiszAxUOP7utJcWblGNtbX%2Ba8Eu8zApM6TbAS9uiQUJ%2FAB3W8hlTSwgCN9PBwaKwT6UgJftfdudJ758ozdm%2FZRmixTYI877Uirzok72efXoNyaJZaba6psG1GsEQp5xuVol99HOwp8UY6dhXkemivxbnxD7x0X%2Fk1icMK4JEqBkav9Q6Tewt7WQKCuT7LzDzS93E4JAw3o%2FoZt5lWEwVKOvoTY9ga8bNWMS8ybOdpiArojyNj1ZXOKAk4L4wc37NWMS8ybOdp1poAnS%2FQyF%2FCAxJ6fs0%2FZekBWv7p6n%2FqTZLRf7JESgiTxjcavbjWVg%3D%3D; st=st96262028dj4344db2itkdtytrjxo7y; st.sig=o2ZwMSY7C3iOCTLG2N_CR00qiQatNlTM3cbEoVWCdRI; tfstk=eIIwx4jODlEa0XD57ex28-g3pT-9c3F5siOXntXDCCAgWnZV86Xc5E6DCI7Fi6OGfPd1TIW5HmO1Ch2Vg_fwlsWYBKAcisRf5yZ5BOKvm7s4Vu69x6emT7w7CjrBDnV7OXEnHqKAaMeDbMcD4ui4IENleBjEvY03QS9JTmmreBYGNudImcIeQ9RlI4mmmMJw7gzmMp2WKiBRgqYMppR7LJun6cu-s8fMuq3v-3peNR9skqLMppR7LJuxkeApLQw6C"
}
session = requests.session()

count=0

def get_text(guid):
    global text
    global count
    for i in range(1,500):
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
            if book['is_directory']==1:	
                print('it is a directory')
                bk=f"\t<DT><H3>{book['name']}</H3>\n\t<DL><p>\n"
                text+=bk
                get_text(book['guid'])
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
