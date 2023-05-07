import json
import os

import tiktoken
import aiohttp
ENGINE = os.environ.get("GPT_ENGINE") or "gpt-3.5-turbo"
ENCODER = tiktoken.get_encoding("gpt2")


class Chatbot:
    """
    Official ChatGPT API
    """

    def __init__(
        self,
        api_key: str,
        engine: str = None,
        proxy: str = None,
        max_tokens: int = 3000,
        temperature: float = 0.5,
        top_p: float = 1.0,
        reply_count: int = 1,
        system_prompt: str = "You are ChatGPT, a large language model trained by OpenAI. Respond conversationally",
    ) -> None:
        """
        Initialize Chatbot with API key (from https://platform.openai.com/account/api-keys)
        """
        self.engine = engine or ENGINE
        self.session: aiohttp.ClientSession = aiohttp.ClientSession()
        self.api_key = api_key
        self.proxy = proxy
        if self.proxy:
            proxies = {
                "http": self.proxy,
                "https": self.proxy,
            }
            self.session.proxies = proxies
        self.conversation: list = [
            {
                "role": "system",
                "content": system_prompt,
            },
        ]
        self.system_prompt = system_prompt
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.reply_count = reply_count

        initial_conversation = "\n".join(
            [x["content"] for x in self.conversation])
        if len(ENCODER.encode(initial_conversation)) > self.max_tokens:
            raise Exception("System prompt is too long")

    def __add_to_conversation(self, message: str, role: str):
        """
        Add a message to the conversation
        """
        self.conversation.append({"role": role, "content": message})

    def __truncate_conversation(self):
        """
        Truncate the conversation
        """
        while True:
            full_conversation = "\n".join(
                [x["content"] for x in self.conversation])
            if (
                len(ENCODER.encode(full_conversation)) > self.max_tokens
                and len(self.conversation) > 1
            ):
                # Don't remove the first message
                self.conversation.pop(1)
            else:
                break

    async def ask_stream(self, prompt: str, role: str = "user", **kwargs) -> str:
        """
        Ask a question
        """
        self.__add_to_conversation(prompt, "user")
        self.__truncate_conversation()
        # Get responses
        
        response = await self.session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {kwargs.get('api_key', self.api_key)}"},
            json={
                "model": self.engine,
                "messages": self.conversation,
                "stream": True,
                # kwargs
                "temperature": kwargs.get("temperature", self.temperature),
                "top_p": kwargs.get("top_p", self.top_p),
                "n": kwargs.get("n", self.reply_count),
                "user": role,
            },
        )
        if response.status != 200:
            raise Exception(
                f"Error: {response.status} {response.reason} {response.text}",
            )
        response_role: str = None
        full_response: str = ""
        async for line in response.content:

            if not line:
                continue
            line = line.decode("utf-8")[6:]
            if line == "[DONE]":
                break
            
            if not line.startswith("{"):
                continue

            resp: dict = json.loads(line)
            choices = resp.get("choices")
            if not choices:
                continue
            delta = choices[0].get("delta")
            if not delta:
                continue
            if "role" in delta:
                response_role = delta["role"]
            if "content" in delta:
                content = delta["content"]
                full_response += content
                yield content
        self.__add_to_conversation(full_response, response_role)

    async def ask(self, prompt: str, role: str = "user", **kwargs):
        """
        Non-streaming ask
        """
        response = self.ask_stream(prompt, role, **kwargs)
        full_response = ""
        async for line in response:
            full_response += line
        return full_response

    async def rollback(self, n: int = 1):
        """
        Rollback the conversation
        """
        for _ in range(n):
            self.conversation.pop()

    async def reset(self):
        """
        Reset the conversation
        """
        self.conversation = [
            {"role": "system", "content": self.system_prompt},
        ]

    async def save(self, file: str):
        """
        Save the conversation to a JSON file
        """
        try:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(self.conversation, f, indent=2)
        except FileNotFoundError:
            print(f"Error: {file} cannot be created")

    async def load(self, file: str):
        """
        Load the conversation from a JSON  file
        """
        try:
            with open(file, encoding="utf-8") as f:
                self.conversation = json.load(f)
        except FileNotFoundError:
            print(f"Error: {file} does not exist")
