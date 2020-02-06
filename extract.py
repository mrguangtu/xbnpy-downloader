from bs4 import BeautifulSoup
import os
import requests
import re
import time

## https://online.xbnpy.com/
## 该网站视频批量下载
## 1. 需要登录，获取cookie，cookie文件放在工作目录中，文件名：cookie.txt
## 2. 将需要下载的科目的目录页另存为html，放在工作目录中
## 3. 运行本程序
## 4. 在 https://github.com/nilaoda/N_m3u8DL-CLI/releases 下载m3u8下载器，随便将一个m3u8路径写入临时文件，拖入N_m3u8DL-CLI-SimpleG.exe
## 程序会自动生成一个bat文件。
## 注意：如果下载zip压缩包，由于Newtonsoft.Json.dll可能误报毒，需要手工白名单一下。
## 5. 打开该bat文件，将本程序生成的一大堆代码替换
## 6. 运行bat文件


# 根据下载另存的html文件，找到课程目录，明确每一节课的网页链接，并解析出详情页中的m3u8地址
# 返回[课程名称，课程详情页网址，解析出的m3u8地址]
def find_topics(inputfile):
    inputfile = open(inputfile,'r',encoding='utf8')
    soup = BeautifulSoup(inputfile, 'html.parser')
    videos = soup.find_all(class_='video')

    classarray = []
    for v in videos:
        li = v.find_all('li')
        for l in li:
            stringv = l.a.text.replace("\n","").replace(" ","").replace('(可试听)','')
            href = l.a.attrs['href']
            m3u8 = find_m3u8(href)
            # m3u8 = "test"
            classarray.append((stringv,href,m3u8))
            # print((stringv,href))
    return classarray


# 找到每节课详情页链接中的m3u8地址
def find_m3u8(url,cookiefile='cookie.txt'):
    time.sleep(2)
    cookies = {}
    cfile = open(cookiefile,'r')
    for line in cfile.readline().split(';'):
        name,value = line.strip().split('=',1)
        cookies[name]=value
    # print(cookies)
    req = requests.get(url,cookies=cookies)
	# 这网站开发者英语是真不行啊，video拼写成vedio，[捂脸][捂脸][捂脸][捂脸]
    regstring = 'vedio\.cdn\.xbnpy\.com.*m3u8'
    soup = BeautifulSoup(req.text,'lxml')
    text1 = soup.find_all(text=re.compile(regstring))
    # print(text1[0])
    matched_string = ''
    for s in text1[0].split('\n'):
        match = re.match(r'.*(\/\/vedio.*m3u8)',s)
        if match:
            # print(s)
            # print(match.string)
            matched_string = match.group(1)
    return "https:"+matched_string


# 主逻辑：

# 遍历工作目录中，下载下来的课程目录网页，找到网页链接，写入课程dict
cur_workingdir = r'C:\Users\administrator\Desktop\download'
cookiefile='cookie.txt'
g = os.walk(cur_workingdir)

# 将所有科目的课程，写入dict
# {科目：[课程名称，课程详情页网址，解析出的m3u8地址]}
dic = {}
for path,dir_list,file_list in g:
    for file_name in file_list:
        # 找到另存的html文件
        if (file_name.split('.')[-1]) == 'html':
            print(f"找到文件： {file_name}")
            file = os.path.join(path, file_name)
            # dic[课程名称]=
            dic[file_name.split('.')[0]] = find_topics(file)

# 课程总数，随便写个数，方便命令行展示用的
count = 112
# 当前在处理的课程序号
cursor = 1

#遍历dict，按批量命令格式，输出m3u8下载命令
for course in dic:
    print(f'::{course}')
    for lession in dic[course]:
        print(f'TITLE "[{cursor}/{count}] - {lession[0]}"')
        cursor += 1
        if not os.path.exists(os.path.join(cur_workingdir,course)):
            os.makedirs(os.path.join(cur_workingdir,course))
        print(f'"N_m3u8DL-CLI.exe" "{lession[2]}" --workDir "{os.path.join(cur_workingdir,course)}" --saveName "{lession[0]}" --enableDelAfterDone ')
