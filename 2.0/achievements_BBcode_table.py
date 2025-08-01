# -*- coding: utf-8 -*-
"""
Created on Fri Aug  1 15:52:34 2025

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


add_extra_column = input("是否增加额外列？(y/n): ").strip().lower() == "y"

rows = []
for _, row in merged_df.iterrows():
    row_parts = [
        "[td][previewimg={id};sizeThumb,floatLeft;{title}][/previewimg][/td]".format(
            id=row["id"], title=row["title"]
        ),
        "[td][b]{name}[/b]\n{desc}[/td]".format(
            name=row["Achievement Name"], desc=row["Description"]
        )
    ]
    if add_extra_column:
        row_parts.append("[td][/td]")

    bbcode_row = "[tr]\n" + "\n".join(row_parts) + "\n[/tr]"
    rows.append(bbcode_row)

bbcode_table = "[table]\n" + "\n".join(rows) + "\n[/table]"

with open("achievements_BBcode_table.txt", "w", encoding="utf-8") as f:
    f.write(bbcode_table)

print("BBCode 表格已保存到 achievements_BBcode_table.txt")
