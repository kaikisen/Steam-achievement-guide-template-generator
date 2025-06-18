import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service


file_path = r'你的achievements.csv路径'  # 此处修改为你的achievements.csv路径
df = pd.read_csv(file_path)

second_column = df.iloc[:, 1]
third_column = df.iloc[:, 2]

ac_title = second_column.tolist()
ac_info = third_column.tolist()

print(ac_title)

#################################
user_data_dir = r"C:\Users\你的用户名\AppData\Local\Microsoft\Edge\User Data"  # 此处修改为你的Edge用户数据路径
# 启动选项
edge_options = Options()
edge_options.add_argument(f"--user-data-dir={user_data_dir}")
edge_options.add_argument("--profile-directory=Default")

service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

driver.get("https://steamcommunity.com/sharedfiles/manageguide/?id=你的指南地址")  # 此处修改为你的steam指南地址

for item in ac_title:
    
    add_button = driver.find_element(By.XPATH, "//a/span[text()='添加一个章节']")
    add_button.click()
    
    time.sleep(1.5)
    # 定位到章节标题的 <a> 标签
    section_title_link = driver.find_element(By.XPATH, "//div[@class='editGuideTOCSectionTitle']/a[text()='（新章节，尚未起标题）']")
    
    section_title_link.click()
    
    # 找到包含"章节标题"的 div 元素
    label_element = driver.find_element(By.XPATH, "//div[text()='章节标题']")
    
    # 定位到标签后的输入框
    input_element = label_element.find_element(By.XPATH, "following-sibling::input")
    input_element.send_keys(item)
    
    # 定位并点击指定的图片
    print(ac_title.index(item)+1)
    image = driver.find_element(By.XPATH, f'''//img[@title="{ac_title.index(item)+1}.jpg"]''')
    image.click()
    
    p_button = driver.find_element(By.XPATH, "//a/span[text()='插入']")
    p_button.click()
    
    # 找到并定位包含"章节内容"的 div 元素
    content_element = driver.find_element(By.XPATH, "//div[text()='章节内容']")
    info_element = driver.find_element(By.XPATH, '//*[@id="description"]')
    info_element.click()
    info_element.send_keys(Keys.END)
    info_element.send_keys(ac_info[ac_title.index(item)])
    
    s_button = driver.find_element(By.XPATH, "//a/span[text()='保存']")
    s_button.click()
    
    section_title_link2 = driver.find_element(By.XPATH, "//div[@class='editGuideHeaderTab ']/a[text()='指南内容']")
    section_title_link2.click()