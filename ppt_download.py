import requests
import os
from PIL import Image

def create_file(path):
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        os.makedirs(path)
        print(">>成功创建文件夹: " + path.split(r"/")[-1])
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(">>已存在文件夹: "+path.split(r"/")[-1])
        return False


def png_convert_pdf(path, pdf_name):
    file_list = os.listdir(path)
    pic_name = []
    im_list = []
    for x in file_list:
        if "jpg" in x or 'png' in x or 'jpeg' in x:
            pic_name.append(x)

    pic_name.sort()
    new_pic = pic_name

    im1 = Image.open(os.path.join(path, new_pic[0])).convert('RGB')
    new_pic.pop(0)
    for i in new_pic:
        img = Image.open(os.path.join(path, i))
        # im_list.append(Image.open(i))
        if img.mode == "RGBA":
            img = img.convert('RGB')
            im_list.append(img)
        else:
            im_list.append(img)
    im1.save(pdf_name, "PDF",save_all=True, append_images=im_list)
    print("输出文件名称：", pdf_name)

def parse_ppt(data):
    data = data["data"]["presentationList"]
    for ppt in data:
        name = ppt["Title"]
        create_file(os.path.join(filedir,name))
        slides = ppt["Slides"]
        slides_url = []
        i = 1
        for s in slides:
            slides_url.append(s["Cover"])
            download_img(s["Cover"], name, i)
            i += 1
        png_convert_pdf(os.path.join(filedir,name),name+".pdf")

def download_img(url,pptname,i):
    img_dir = filedir + "/" + str(pptname) + "/" + str(i) + ".png"
    r = requests.get(url,stream=True)
    open(img_dir, 'wb').write(r.content)

def main():
    url = "https://www.yuketang.cn/v/lesson/get_lesson_replay_content/?lesson_id=" + courseid
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        "cookie":"sessionid=" + sessionid
    }

    r = requests.get(url,headers=headers)
    parse_ppt(r.json())

if __name__ == '__main__':
    courseurl = input("请输入课堂网址： ")
    sessionid = input("请输入sessionid： ")
    courseid = courseurl.split("/")[-2]
    filedir = "./"
    main()