#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
github action调用此脚本完成一些工作
"""

import json
import os
import subprocess
import time

import requests
from algoliasearch.search_client import SearchClient


# 将最新的url提交到bing
# 需在 gh-pages 上操作，因为涉及到检测html文件
def commit_urls():
    print("将最新的url提交到bing")
    urls = []

    ret = subprocess.run(
        ['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if ret.returncode == 0:
        commit_id = str(ret.stdout, "utf_8").strip()
        print("最近一次的commitId:", commit_id)
        ret = subprocess.run(
            ['git', 'show', '--pretty=', '--name-only', commit_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if ret.returncode == 0:
            changes = str(ret.stdout, "utf-8").split("\n")
            for change in changes:
                # 以20开始，表示年份是20xx，所有posts下面的博客命名都是年月日开始的
                if change.endswith(".md") and change.startswith("20"):
                    urls.append("https://whuwangyong.github.io/{}".format(change[:-8])) # 去掉末尾的index.md
        else:
            print("========================")
            print("subprocess run error:{}".format(ret.stderr))
    else:
        print("========================")
        print("subprocess run error:{}".format(ret.stderr))

    # 按时间排序
    urls.sort()
    # 取最新的5个文件
    urls = urls[-5:]

    print("本次提交的urls:", urls)

    if len(urls) > 0:
        # 提交到bing
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Host": "ssl.bing.com",
        }
        data = {"siteUrl": "https://whuwangyong.github.io/", "urlList": urls}
        response = requests.post(
            url="https://www.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey=c8e29ae3ee2c4465a596a0ac7973b8f3",
            headers=headers,
            data=json.dumps(data),
        )
        print("bing的响应: ", response.content)



# 需要在gh-pages分支操作，因为要读index.json文件
def upload_index_2_algolia():
    print("上传索引文件到algolia...")
    # Connect and authenticate with your Algolia app
    client = SearchClient.create("YMLBEBNFHL", "4962bf8c8b0c034ee6ef247a9c162304")

    # Create a new index and add a record
    index = client.init_index("new-index-1649076215")
    with open('./public/index.json', 'r', encoding='utf8') as fp:
        json_data = json.load(fp)
    index.save_objects(json_data).wait()

    print("上传索引文件到algolia完成")


def main():
    print("+++++++++++++++++++")
    print("++ publish start...")
    print("++ current dir is:", os.getcwd())

    commit_urls()
    # upload_index_2_algolia()

    print("+++++++++++++++++++")
    print("done!")
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


if __name__ == "__main__":
    main()
