# xbnpy-downloader

[该网站](https://online.xbnpy.com/)  视频批量下载

特殊说明：没有账号密码，是不能下载滴，别多想，啊~~

1.  需要登录，获取cookie，cookie文件放在工作目录中，文件名：cookie.txt

2.  将需要下载的科目的目录页另存为html，放在工作目录中。文件名就是课程文件夹的名字。

3.  运行本程序

4.  在 https://github.com/nilaoda/N_m3u8DL-CLI/releases 下载m3u8下载器，随便将一个m3u8路径写入临时文件，拖入N_m3u8DL-CLI-SimpleG.exe。程序会自动生成一个bat文件。
5. 注意：如果下载zip压缩包，由于Newtonsoft.Json.dll可能误报毒，需要手工白名单一下。
6. 打开该bat文件，将本程序生成的一大堆代码替换进去
7. 运行bat文件，rock and row





Feature：

**Ver 0.01**    2020-02-06

* 支持各课程单独文件夹，不同文件夹分别下载不同课程名称。