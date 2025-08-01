# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 13:47:27 2025

@author: kaikisen
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from PIL import Image
from io import BytesIO

# 创建存储成就图片的文件夹
if not os.path.exists('achievement_images'):
    os.makedirs('achievement_images')

appid = input('请输入steam游戏的appid：')

url = r'https://steamcommunity.com/stats/'+appid+r'/achievements?l=schinese'# 你的目标网页

response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 找到所有成就项
    achieve_rows = soup.find_all('div', class_='achieveRow')
    
    # 存储抓取的成就数据
    achievements = []
    ac_id = 0
    
    for row in achieve_rows:
        ac_id += 1
        
        # 获取成就图像URL
        img_url = row.find('img')['src']
        
        # 获取成就名称
        name = row.find('h3').text.strip()
        
        # 获取成就描述
        description = row.find('h5').text.strip()
        
        # 获取成就达成百分比
        percent = row.find('div', class_='achievePercent').text.strip()
        
        # 下载图片
        img_data = requests.get(img_url).content
        # 使用Pillow库将图片压缩为64x64
        img = Image.open(BytesIO(img_data))
        img = img.resize((64, 64))  # 压缩图片大小到64x64
        img_filename = os.path.join('achievement_images', f"{ac_id}.jpg")
        img.save(img_filename)
        print(img_filename)
        
        # 将数据存入列表
        achievements.append({
            'Achievement ID': ac_id,
            'Achievement Name': name,
            'Description': description,
            'Percentage': percent,
            'Image URL': img_url,
            'Image File': img_filename
        })
    
    # 保存成CSV
    df = pd.DataFrame(achievements)
    df.to_csv('achievements.csv', index=False, encoding='utf-8-sig')
    print("CSV 文件已保存，并下载了所有图片！")
else:
    print(f"请求失败，状态码：{response.status_code}")