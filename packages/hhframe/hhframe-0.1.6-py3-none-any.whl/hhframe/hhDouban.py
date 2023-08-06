
# -*- codeing = utf-8 -*-
# @File：hhDouban.py
# @Ver：1.1.0
# @Author：立树
# @Time：2021/07/01 18:11
# @IDE：PyCharm

"""
更新：
- 新增 star 豆瓣明星信息抓取
"""

import re
import execjs
from .hhAjax import hhGet
from bs4 import BeautifulSoup

class hhDouban(object):

    def __init__(self):
        pass

    # 豆瓣搜索
    def search(self,opt={}):
        # 配置
        hhOpt = {
            "search": "",
            "decrypt": ""
        }
        hhOpt.update(opt)

        # 参数判断
        if hhOpt["search"]=="" or hhOpt["decrypt"]=="":
            print("hhframe.hhDouban.search() Error - 请补全参数（search、decrypt）")
            return {}

        try:
            # 发起请求
            page = hhGet(f"https://search.douban.com/movie/subject_search?search_text={hhOpt['search']}&cat=1002")

            # 获取加密数据
            encrypt = re.search('window.__DATA__ = "([^"]+)"',page).group(1)
            # print(encrypt)

            # 提取解密 js
            with open(hhOpt["decrypt"], "r", encoding="UTF-8", errors="ignore") as f:
                decrypt_js = f.read()
                # print(decrypt_js)

            # 解密数据
            ctx = execjs.compile(decrypt_js)
            ret = ctx.call("decrypt",encrypt)
            return ret["payload"]
        except Exception as err:
            print(f"hhframe.hhDouban.search() Error - {err}")
            return {}

    # 豆瓣明星信息抓取
    def star(self,name=""):
        # 参数判断
        if name == "":
            print("hhframe.hhDouban.star() Error - 请补全参数（name）")
            return []

        try:
            # 发起请求
            page = hhGet(f"https://movie.douban.com/celebrities/search?search_text={name}&cat=1002")
            html = BeautifulSoup(page,"html.parser")
            list = html.select("div.article .result")
            stars = []
            for item in list:
                star = {
                    "name": item.select(".content h3 a")[0].text,
                    "poster": item.select(".pic img")[0].attrs["src"],
                    "url": item.select(".content h3 a")[0].attrs["href"]
                }
                infos = item.select(".content > ul li")
                star["jobs"] = infos[0].text.strip().split(" / ")
                if len(infos) == 3:
                    dates = infos[1].text.strip().split(" 至 ")
                    birth = dates[0]
                    death = dates[1] if len(dates) == 2 else ""
                    works = infos[2].text.replace("作品:", "").strip().split(" / ")
                    star["birth"] = birth
                    star["death"] = death
                    star["works"] = works
                if len(infos) == 2:
                    works = infos[1].text.replace("作品:", "").strip().split(" / ")
                    star["works"] = works
                stars.append(star)

            return stars
        except Exception as err:
            print(f"hhframe.hhDouban.star() Error - {err}")
            return []
