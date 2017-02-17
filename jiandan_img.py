from bs4 import BeautifulSoup
import requests
import random


# 爬取图片地址
web_path = {
    'ooxx': 'http://jandan.net/ooxx',
    'pic': 'http://jandan.net/pic'
}


class Page(object):
    base_path = ''  # 基础路径
    path = ''   # 路径
    page = ''   # 当前所在页面
    r = None    # 爬取到的页面资源
    soup = None
    page_img_path_list = {}     # 页码与值对应表

    def __init__(self, base_path, page=None):
        self.base_path = base_path
        if not page:
            self.set_page(page)

    def set_page(self, page):
        # 设置页码
        self.page = page
        self.path = self.base_path + '/page-' + page.__str__()
        self.r = requests.get(self.path)
        self.soup = BeautifulSoup(self.r.content, 'html.parser')

    def get_total_page_num(self):
        # 获取总页数
        r = requests.get(self.base_path)
        content = r.content
        soup = BeautifulSoup(content, "html.parser")
        ret = soup.find("span", class_='current-comment-page')
        page_num_str = ret.text
        page_num_str = page_num_str[1:page_num_str.__len__()-1]
        page_num_int = int(page_num_str)
        return page_num_int

    def get_img_path_dict(self):
        # 获取当前页面中的所有图片地址
        if self.page in self.page_img_path_list.keys():
            print('has cache')
            return self.page_img_path_list[self.page]
        else:
            soup = self.soup
            rows = soup.find_all("a", class_="view_img_link")
            pic_urls = []
            for row in rows:
                pic_url = row['href']
                pic_urls.append(pic_url)
            self.page_img_path_list[self.page] = pic_urls
            return pic_urls

if __name__ == '__main__':
    P = Page(web_path['pic'])
    total_page_num = P.get_total_page_num()
    print('page total num: ' + total_page_num.__str__())
    rand_page = random.randint(1, total_page_num)
    P.set_page(rand_page)
    img_page_dict = P.get_img_path_dict()
    rand_img_path = img_page_dict[random.randint(0, img_page_dict.__len__()-1)]
    print('rand im path:' + rand_img_path)
