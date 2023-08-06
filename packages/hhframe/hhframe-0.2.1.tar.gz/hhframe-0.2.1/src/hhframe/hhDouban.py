
# -*- codeing = utf-8 -*-
# @File：hhDouban.py
# @Ver：1.2.1
# @Author：立树
# @Time：2021/07/02 17:48
# @IDE：PyCharm

"""
更新：
- 优化 getStarDetail 豆瓣明星详情抓取（添加了 descp 详细简介字段）
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

    # 豆瓣明星列表抓取
    def getStarList(self,name=""):
        # 参数判断
        if name == "":
            print("hhframe.hhDouban.getStarList() Error - 请补全参数（name）")
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
                star["id"] = re.findall("\d+",star["url"])[0]
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
            print(f"hhframe.hhDouban.getStarList() Error - {err}")
            return []

    # 豆瓣明星详情抓取
    def getStarDetail(self,id=""):
        # 参数判断
        if id == "":
            print("hhframe.hhDouban.getStarDetail() Error - 请补全参数（id）")
            return []

        try:
            # 发起请求
            page = hhGet(f"https://movie.douban.com/celebrity/{id}/")
            # 调试
            # file = "./demo_douban_star_detail.txt"
            # with open(file,"w",encoding="utf-8") as f:
            #     f.write(page)
            # return
            # with open(file,"rb") as f:
            #     page = f.read()

            html = BeautifulSoup(page,"html.parser")

            star = {
                "id": id,
                "poster": html.select("#headline .pic img")[0].attrs["src"]
            }
            names = html.select("#content > h1")[0].text
            name = html.select("#headline .pic img")[0].attrs["title"]
            alias = names.replace(name,"").strip()
            star["name"] = name
            star["alias"] = alias

            info = html.select("#headline .info li")
            for item in info:
                label = item.select("span")[0].text
                # print(label)
                # print(item)
                if label=="星座":
                    star["constellation"] = item.text.replace("星座:","").strip()
                if label=="出生日期":
                    dates = re.findall("((\d+)年(\d+)月(\d+)日)", item.text)
                    birth, bY, bM, bD = dates[0]
                    star["birth"] = f"{bY}-{bM}-{bD}"
                if label=="生卒日期":
                    dates = re.findall("((\d+)年(\d+)月(\d+)日)", item.text)
                    birth, bY, bM, bD = dates[0]
                    death, dY, dM, dD = dates[1]
                    star["birth"] = f"{bY}-{bM}-{bD}"
                    star["death"] = f"{dY}-{dM}-{dD}"
                if label=="出生地":
                    star["area"] = item.text.replace("出生地:","").strip()
                if label=="职业":
                    star["jobs"] = item.text.replace("职业:","").strip().split(" / ")
                if label=="更多中文名":
                    star["chinese_names"] = item.text.replace("更多中文名:","").strip().split(" / ")
                if label=="更多外文名":
                    star["other_names"] = item.text.replace("更多外文名:","").strip().split(" / ")
                if label=="imdb编号":
                    star["imdb"] = item.select("a")[0].text
                    star["imdb_url"] = item.select("a")[0].attrs["href"]
                if label=="家庭成员":
                    star["family"] = item.text.replace("家庭成员:","").strip().split(" / ")

            # 简介
            star["descp"] = html.select("#intro .all")[0].text.replace("\u3000","").replace("\r","<br>")
            print(star["descp"])
            return star
        except Exception as err:
            print(f"hhframe.hhDouban.getStarDetail() Error - {err}")
            return []
