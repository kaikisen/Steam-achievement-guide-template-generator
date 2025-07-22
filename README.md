# Steam-achievement-guide-template-generator

## 这个玩意儿到底是干嘛的

这个屎山可以追溯到大半年前Death of the Reprobate的时候心血来潮想写成就指南，但是又想着一条条创建条目、导入图片、编辑成就名和说明实在是好——麻烦！于是就想着一劳永逸整一个自动化工具解决这个问题。

这个脚本运行情况如下：



![3363914853_preview_无标题视频——使用Clipchamp制作 (3)](https://github.com/user-attachments/assets/87926249-920c-4e16-ae13-f426a93387ac)



（这个gif没有加速

如果你好奇这个工具生成的模板效果，可以参考以下几篇指南，其框架都是我用这个小脚本自动生成的。

https://steamcommunity.com/sharedfiles/filedetails/?id=3363914853

https://steamcommunity.com/sharedfiles/filedetails/?id=3439520291

https://steamcommunity.com/sharedfiles/filedetails/?id=3460894332

https://steamcommunity.com/sharedfiles/filedetails/?id=3502332697

本项目完全允许二传二改，如果你对python、steam格式和html样式有一定了解，也可以尝试一下制作成更贴你心意、更适合你自己风格的脚本。



## 使用

0.安装requirement.txt中的库；

1.运行InfoWithPic.py，输入游戏的appid，同文件夹下应该就会出现存放成就图片的achievement_images和achievements.csv了；

2.创建一份指南，编辑好基本信息，在“指南内容”界面并上传achievement_images里的所有成就图片（似乎只有在浏览器编辑才能够批量上传？辣鸡steam又一力证）；复制“指南内容”界面的链接，其末端应该以“manageguide/?id=xxxxxxxxxx”结尾；

3.打开edge浏览器，登录steam并打开你刚刚新建的指南链接，确保你能够在edge上访问这个界面；

4.编辑GuideGenerate.py：

* 将【file_path = r'此处替换achievements.csv的文件路径' 】一行中的路径改为刚刚生成的achievements.csv的文件路径

- 将【user_data_dir = r"C:\Users\{你的用户名}\AppData\Local\Microsoft\Edge\User Data"】一行中的值改为你的edge用户数据文件夹（用于带有缓存状态打开浏览器），这个值只需要在首次使用时编辑一次

* 将【driver.get("你的指南链接")】中的值替换为你刚刚创建的指南链接，其末端应该以“manageguide/?id=xxxxxxxxxx”结尾。

5.**关闭并退出所有的edge界面**、**关闭并退出所有的edge界面**、**关闭并退出所有的edge界面**，并运行GuideGenerate.py——如果一切顺利，你应该可以看到成就条目在以惊人的速度自动生成了。

25.07.23更新，新增了steam无法识别的游戏单独添加功能脚本
