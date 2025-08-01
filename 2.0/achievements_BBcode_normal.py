# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 16:09:32 2025

@author: kaikisen
"""

import pandas as pd
import glob
import os

image_csv_files = glob.glob("*_steam_guide_images.csv")
if not image_csv_files:
    raise FileNotFoundError("找不到 *_steam_guide_images.csv 文件")
image_csv_path = image_csv_files[0]

achievements_df = pd.read_csv("achievements.csv")
images_df = pd.read_csv(image_csv_path)

achievements_df["Image File"] = achievements_df["Image File"].apply(lambda x: os.path.basename(x).replace("%20", " "))

merged_df = pd.merge(
    achievements_df,
    images_df,
    left_on="Image File",
    right_on="title",
    how="inner"
)

# 替换nan
merged_df["Description"] = merged_df["Description"].fillna("")

blocks = []
for _, row in merged_df.iterrows():
    block = (
        f"[previewimg={row['id']};sizeThumb,floatLeft;{row['title']}][/previewimg] "
        f"[b]{row['Achievement Name']}[/b]\n{row['Description']}\n[hr][/hr]\n"
    )
    blocks.append(block)

bbcode_output = "\n".join(blocks) 

with open("achievements_BBcode_normal.txt", "w", encoding="utf-8") as f:
    f.write(bbcode_output)

print("BBCode 已保存到 achievements_BBcode_normal.txt")
