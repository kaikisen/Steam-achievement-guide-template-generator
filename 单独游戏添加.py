# -*- coding: utf-8 -*-
"""
Created on Wed Jul 23 01:44:42 2025

@author: kaikisen
"""

#无记录的游戏单独补充


import urllib.request
import urllib.error
import json
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib import request, parse
from http import cookiejar
import datetime

'''
重要！在下面替换为你的信息
'''
notion_api = "ntn_K676224617531WhtGAN8YsbrwXpu452qiXRageqr0a6b74"
database_id = "1e71930fb01f80ad9cfbe02109548700"

add_appid = 2905170

import requests

def change_tag_to_text(database_id, notion_api):
    url = f"https://api.notion.com/v1/databases/{database_id}"
    headers = {
        "Authorization": f"Bearer {notion_api}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {
        "properties": {
            "tag": {
                "rich_text": {}
            }
        }
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print("成功将 tag 属性改为文字。")
    else:
        print(f"修改失败，状态码: {response.status_code}")
        print("响应内容:", response.text)
        
change_tag_to_text(database_id, notion_api)

def get_json(url):
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"请求失败: {e}")
        return None



def get_steam_game_info(appid):
    url = f"https://store.steampowered.com/app/{appid}/?l=schinese"
    headers = {"User-Agent": "Mozilla/5.0"}
    cj = cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    request.install_opener(opener)
    cookies = {
        'birthtime': '568022401',
        'lastagecheckage': '1-January-1990',
        'wants_mature_content': '1'
    }
    cookie_str = "; ".join([f"{key}={value}" for key, value in cookies.items()])
    headers['Cookie'] = cookie_str
    req = request.Request(url, headers=headers)
    try:
        with request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f"请求失败: AppID {appid}, 错误: {e}")
        return None
    soup = BeautifulSoup(html, 'html.parser')
    try:
        title_tag = soup.find('div', {'class': 'apphub_AppName'})
        game_name = title_tag.get_text(strip=True) if title_tag else None
    except:
        game_name = None
    try:
        tags = [tag.get_text(strip=True) for tag in soup.find_all('a', {'class': 'app_tag'})[:8]]
        tags_str = ', '.join(tags)
    except:
        tags_str = None
    return {
        '游戏名称': game_name,
        'tag': tags_str,
        '封面': f'https://steamcdn-a.akamaihd.net/steam/apps/{appid}/header.jpg',
        'appid': appid
    }


def create_notion_page(game):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_api}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    data = {
        "parent": {"database_id": database_id},
        "cover": {"external": {"url": game['封面']}},
        "properties": {
            "游戏名称": {"title": [{"text": {"content": game['游戏名称']}}]},
            "appid": {"rich_text": [{"text": {"content": str(game['appid'])}}]},
            "tag": {"rich_text": [{"text": {"content": game.get('tag', '')}}]},
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if not response.ok:
        print(f"导入失败：{game['游戏名称']}，错误：{response.status_code} {response.text}")



def main():
    appid = add_appid
    #print(appid)
    meta = get_steam_game_info(appid) or {}
    print(f"新增游戏: {meta['游戏名称']}")
    game_info = meta
    create_notion_page(game_info)
    print("操作完成！")

if __name__ == "__main__":
    main()