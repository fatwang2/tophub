import requests  # 导入用于发送 HTTP 请求的库
import json  # 导入用于处理 JSON 数据的库
import re  # 导入用于正则表达式匹配的库
import plugins  # 导入自定义的插件模块
from bridge.reply import Reply, ReplyType  # 导入用于构建回复消息的类
from plugins import *  # 导入其他自定义插件
from config import conf  # 导入配置文件

@plugins.register(
    name="Tophub",  # 插件的名称
    desire_priority=1,  # 插件的优先级
    hidden=False,  # 插件是否隐藏
    desc="A plugin for tophub",  # 插件的描述
    version="0.1",  # 插件的版本号
    author="fatwang2",  # 插件的作者
)
class Tophub(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        print("[Tophub] inited")  # 初始化插件时打印一条消息

    def on_handle_context(self, e_context: EventContext):
        content = e_context["context"].content  # 获取事件上下文中的消息内容
        if content == "热榜":  # 如果消息内容为 "热榜"
            token = conf().get("tophub_token")  # 从配置文件中获取 tophub_token
            type = conf().get("tophub_type") # 从配置文件中获取 tophub_type
            url = "https://v2.alapi.cn/api/tophub/get"  # API 的 URL
            payload = f"token={token}&type={type}&format=json"  # 构建请求的参数
            headers = {'Content-Type': "application/x-www-form-urlencoded"}  # 请求头

            try:
                response = requests.request("POST", url, data=payload, headers=headers)  # 发送 POST 请求
                response.raise_for_status()  # 如果状态码不是 200，抛出异常
            except requests.exceptions.RequestException as e:
                print(f"An error occurred when making the request: {e}")  # 请求出错时打印错误消息
                return

            data = json.loads(response.text)  # 解析返回的 JSON 数据
            news_data = data.get('data')  # 获取新闻数据
            if news_data:
                date = news_data.get('last_update')  # 获取更新时间
                news_list = news_data.get('list')  # 获取热榜列表
                name = news_data.get('name')  # 获取热榜名称

                reply = Reply()  # 创建回复消息对象
                reply.type = ReplyType.TEXT  # 设置回复消息的类型为文本
                reply.content = f"🔥🔥🔥{name}\n更新时间: {date}\n\n"  # 设置回复消息的内容

                for i, news_item in enumerate(news_list, 1):
                    title = news_item.get('title', '未知标题') # 获取新闻标题
                    link = news_item.get('link', '未知链接') # 获取新闻链接
                    # 删除任何前置的数字和特殊字符（如果有）
                    title = re.sub(r'^\d+[、.]\s*', '', title)

                    # 添加到回复内容中
                    reply.content += f"{i}. {title}\n{link}\n\n"

                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                print("ERROR: Data not found in response")

    def get_help_text(self, **kwargs):
        help_text = "输入 '热榜'，我会为你抓取每日新闻\n"
        return help_text
