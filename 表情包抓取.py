import requests
from bs4 import BeautifulSoup
import re

def download_all_htmls():
    """
    下载所有列表页面的HTML，用于后续的分析
    """
    htmls = []
    for idx in range(5):
        url = f"https://fabiaoqing.com/biaoqing/lists/page/{idx+1}.html"
        print("craw html:", url)
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception("error")
        htmls.append(r.text)
    print("success")
    return htmls

# 执行爬取
htmls = download_all_htmls()
htmls[0][:1000]
def parse_single_html(html):
    """
    解析单个HTML，得到数据
    @return list((img_title, img_url))
    """
    soup = BeautifulSoup(html, 'html.parser')
    img_divs = soup.find_all("div", class_="tagbqppdiv")
    datas = []
    for img_div in img_divs:
        img_node = img_div.find("img")
        if not img_node: continue
        datas.append((img_node["title"], img_node["data-original"]))
    return datas
import pprint
pprint.pprint(parse_single_html(htmls[0])[:10])

# 执行所有的HTML页面的解析
all_imgs = []
for html in htmls:
    all_imgs.extend(parse_single_html(html))
all_imgs[:10]

print(len(all_imgs))

for idx, (title, img_url) in enumerate(all_imgs):
    # 移除标点符号，只保留中文、大小写字母和阿拉伯数字
    reg = "[^0-9A-Za-z\u4e00-\u9fa5]"
    title = re.sub(reg, '', title)

    # 发现了超长的图片标题，做截断
    if len(title)>10: title = title[:10]

    # 得到jpg还是gif后缀
    post_fix = img_url[-3:]
    filename = f"./output/{title}.{post_fix}"

    print(idx, filename)
    img_data = requests.get(img_url)
    with open(filename,"wb")as f:
        f.write(img_data.content)

print("success")




