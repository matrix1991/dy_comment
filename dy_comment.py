import requests
from plugins import Plugin, register
from bridge.reply import Reply, ReplyType
from common.log import logger

API_URL = "https://api.pearktrue.cn/api/dy/comment/"

@register(name="DouYinCommentFetcher",
          desc="抖音评论获取插件",
          version="1.0",
          author="Your Name",
          desire_priority=100)
class DouYinCommentFetcher(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info(f"[{__class__.__name__}] initialized")

    def get_help_text(self, **kwargs):
        help_text = "发送【评论】加视频ID获取抖音视频评论"
        return help_text

    def on_handle_context(self, e_context):
        if e_context['context'].type != ContextType.TEXT:
            return
        content = e_context["context"].content.strip()
        if content.startswith("评论"):
            video_id = content.split()[1]  # 假设命令是 "评论 123456"
            logger.info(f"[{__class__.__name__}] Received message: {content}")
            reply = Reply()
            result = self.fetch_comments(video_id)
            if result is not None:
                reply.type = ReplyType.TEXT
                reply.content = str(result)  # 将评论数据转为字符串形式
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS
            else:
                reply.type = ReplyType.ERROR
                reply.content = "Failed to fetch comments, please try later."
                e_context["reply"] = reply
                e_context.action = EventAction.BREAK_PASS

    def fetch_comments(self, video_id):
        params = {"video_id": video_id}  # 假设API需要一个视频ID参数
        try:
            response = requests.get(url=API_URL, params=params)
            if response.status_code == 200:
                json_data = response.json()
                logger.info(f"API response data: {json_data}")
                return json_data
            else:
                logger.error(f"API request failed with status: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"API request exception: {e}")
            return None

if __name__ == "__main__":
    plugin = DouYinCommentFetcher()
    # Example usage: to simulate, we directly call the fetch method
    result = plugin.fetch_comments("123456")
    if result:
        print("Fetched comments: ", result)
    else:
        print("Failed to fetch comments")
