import openai
import traceback
import settings

class ChatGpt:

    API_KEY = settings.API_KEY
    MAX_TOKENS = 4097 - 100
    ATTEMPTS = 3

    def __init__(self, prompt="", role="", model="gpt-3.5-turbo", max_tokens=-1):
        openai.api_key = ChatGpt.API_KEY
        self.prompt = prompt
        self.role = role
        self.model = model
        self.max_tokens = max_tokens if max_tokens > 0 else (ChatGpt.MAX_TOKENS - len(self.prompt+role) // 3)
        self.task = None


    def run_task(self):
        for i in range(ChatGpt.ATTEMPTS):
            try:
                self.task = openai.ChatCompletion.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    messages=[
                        {"role": "system", "content": self.role},
                        {"role": "user", "content": self.prompt},
                    ]
                )
                return
            except Exception as e:
                print(str(e))
                traceback.print_exc()

    def get_response(self):
        result = ""
        for choice in self.task.choices:
            result += choice.message.content
        return result

    def create_image(self):
        for i in range(ChatGpt.ATTEMPTS):
            try:
                self.task = openai.Image.create(prompt = self.prompt, n=1,size="1024x1024")
                return self.task["data"][0]["url"]
            except Exception as e:
                print((str(e)))
                traceback.print_exc()

#a = ChatGpt(prompt="Create a feature image for Safari Sam online slot game Design a cartoon-style feature image that showcases the adventurous spirit of Safari Sam. The image should feature a happy Maya warrior with glasses, ready to explore the wilds of Africa. The warrior should be shown in a jeep with a camping tent in the background, surrounded by wild animals such as monkeys, zebras, and lions. The image should be vibrant and colorful, with a lively atmosphere that conveys the excitement of the game. Make sure to include the games title, Safari Sam, prominently in the image. Additionally, incorporate elements such as the games logo or symbols to tie it back to the game and entice players to give it a spin. The image should be eye-catching and memorable, making it a great asset for marketing the game.")
#print(a.create_image())