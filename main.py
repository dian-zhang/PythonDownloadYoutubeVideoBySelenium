import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_youtube_data(driver):
    # 打开网页
    url = "https://www.youtube.com/@user-lg2ir8qo5e/videos"
    driver.get(url)

    # 使用 XPath 定位元素
    # 视频数量
    element = driver.find_element(By.XPATH, '//*[@id="page-header"]/yt-page-header-renderer/yt-page-header-view-model/div/div[1]/div/yt-content-metadata-view-model/div[2]/span[3]/span')
    video_nums = int(element.text.split(' ')[0])
    print(video_nums)
    # 最新视频标题
    element = driver.find_element(By.XPATH, '//*[@id="contents"]/ytd-rich-item-renderer[1]')
    title = element.text.split('\n')[1]
    print(title)
    # 最新视频url
    element = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-item-renderer[1]/div/ytd-rich-grid-media/div[1]/div[1]/ytd-thumbnail/a')
    video_url = element.get_attribute('href')
    print(video_url)

    return video_nums, title, video_url


def download_video_cover(title, video_url, driver):
    # 视频封面下载
    url = "https://www.strerr.com/index.html"
    driver.get(url)
    time.sleep(5)
    # 定位到 input 元素，其 id 为 "customControlValidation3"
    input_element = driver.find_element(By.ID, "customControlValidation3")
    # 在 input 元素中输入值
    input_element.send_keys(video_url)
    # 定位按钮元素
    button = driver.find_element(By.XPATH, "/html/body/main/div/div[2]/div[4]/button")
    # 模拟点击按钮
    button.click()
    time.sleep(5)
    # 定位图片元素
    img_element = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div[2]/div[7]/a/img")
    # 获取图片的 src 属性值
    img_url = img_element.get_attribute('src')
    # 发送请求获取图片内容
    response = requests.get(img_url)
    # 保存图片
    with open(title + '.jpg', 'wb') as f:
        f.write(response.content)
        print("封面下载完成")


def download_video(video_url, driver):
    # 视频下载
    url = "https://youtube4kdownloader.com/"
    driver.get(url)
    time.sleep(5)
    # 定位到 input 元素，其 id 为 "video"
    input_element = driver.find_element(By.ID, "video")
    # 在 input 元素中输入值
    input_element.send_keys(video_url)
    # 定位按钮元素
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/section[1]/div/div[2]/form/input[2]')
    # 模拟点击按钮
    button.click()
    time.sleep(10)
    # 定位视频格式
    element = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/section[3]/div/div[2]/div/table[1]/tbody/tr[1]/td[2]')
    video_format = element.text
    # 定位视频下载url
    element = driver.find_element(By.XPATH, '//*[@id="table-tab1"]/tbody/tr[1]/td[5]/a')
    video_download_url = element.get_attribute('href')
    # 开始下载视频
    driver.get(video_download_url)
    # 两个小时
    time.sleep(60 * 60 * 2)
    print("视频下载完成。")


if __name__ == "__main__":
    # 创建浏览器驱动对象（以 Chrome 为例）
    driver = webdriver.Chrome()

    video_nums, title, video_url = get_youtube_data(driver)
    download_video_cover(title, video_url, driver)
    download_video(video_url, driver)

    # 关闭浏览器驱动对象
    driver.quit()