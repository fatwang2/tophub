本项目为ChatGPT-ON-Wechat插件，支持今日热榜新闻抓取推送，效果如下：
![Alt text](image.png)

1. 需自行注册申请token，免费，API来源于https://alapi.cn/api/view/50
2. 为方便配置，直接取的是根目录下的变量，需在config.py和config.json中新增两个变量，用来输入不同类型新闻与token 
    "tophub_token":"",
    "tophub_type":"",
3. 通过切换type，可支持不同类型的新闻内容，理论上api能支持的均可以使用
![Alt text](image-1.png)

4. 本插件参考JC0v0的早报、星座插件修改，本人0代码基础，感谢伟大的AI，让编程变得如此简单