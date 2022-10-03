#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-

import requests
from lxml import etree
import os


def get_doc_url(url):
    '''
    获取分试卷的详细页链接
    '''

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
    }

    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:

        html = response.text
        all_doc_page = etree.HTML(html)

        doc_url = all_doc_page.xpath(
            "//div[@class='list-bd']//div[@class='title fl']/a/@href")

        return doc_url


def jpg2pdf(doc_id):
    '''
    将jpg转换为pdf
    '''

    # 如果没有名为output的文件夹，则新建
    if not os.path.exists("output"):
        os.mkdir("output")

    # 进入doc_id文件夹
    os.chdir(doc_id)

    # 遍历该文件夹下的所有文件
    for i in os.listdir():
        # 如果是jpg文件
        if os.path.splitext(i)[1] == ".jpg":
            # 将jpg转换为pdf
            os.system(f"magick {i} {i[:-4]}.pdf")

    # 将该文件夹下的所有pdf文件合并为一个
    os.system(f"magick convert *.pdf {doc_id}.pdf")
    # 将该文件夹下的所有pdf文件移动到output文件夹下
    os.system(f"mv {doc_id}.pdf ../output")
    # 返回上一级目录
    os.chdir("..")
    # 删除doc_id文件夹
    os.system(f"rm -r {doc_id}")


def get_png(doc_url):
    '''
    遍历每套试卷的详细页，下载图片
    '''

    # 遍历每套试卷的详细页
    for i in doc_url:

        url = "https://" + i[2:]
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.53"
        }

        response = requests.get(url=url, headers=headers).text

        # 解析html
        html = etree.HTML(response)

        # 该试卷代号
        doc_id = url.split("-")[1].split(".")[0]

        # 该试卷图片的链接（示例）
        jpg_url = html.xpath("//div[@class='img-box']/img/@src")
        # 试卷图片链接前缀
        jpg_url_split = jpg_url[0].split("/")
        jpg_url_prefix = f"https://{jpg_url_split[2]}/{jpg_url_split[3]}/{jpg_url_split[4]}/{jpg_url_split[5]}"
        # print(jpg_url_prefix)

        # 显示的页数
        show_page_num = len(jpg_url)
        # 试卷未显示的页数
        no_show_page_num = html.xpath(
            "//div[@class='remain-previews-inner']/span/span/text()")[0]
        # 总页数
        all_page_num = int(show_page_num) + int(no_show_page_num)

        # 如果没有名称为doc_id的文件夹，则创建
        if not os.path.exists(doc_id):
            os.mkdir(doc_id)

        print("\n正在下载试卷: {}...".format(doc_id))

        # 遍历每张图片
        for j in range(0, int(all_page_num)):

            # 构建图片链接
            jpg_url = f"{jpg_url_prefix}/0/{j}.jpg?x-oss-process=image/crop,h_1044,g_center/format,webp"

            # 下载图片
            response = requests.get(url=jpg_url, headers=headers)
            # 将图片保存到doc_id文件夹下
            with open(f"{doc_id}/{j}.jpg", "wb") as f:
                f.write(response.content)

        print("下载完成!")

        print("正在转换为PDF...")
        # 转换为PDF
        jpg2pdf(doc_id)

        print("转换完成!")

    print("\n全部下载完毕！\n")


def main():
    url = input("\n请输入成套试卷链接: ")
    # url = "https://www.51jiaoxi.com/album-24388.html"
    # url = "https://www.51jiaoxi.com/album-18400.html"

    doc_url = get_doc_url(url)
    get_png(doc_url)


if __name__ == "__main__":
    main()
