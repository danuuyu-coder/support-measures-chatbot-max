from gigachat import GigaChatAsyncClient
from gigachat.models import Chat, Messages, MessagesRole

class GigaClient:
    def __init__(self, token: str):
        self._giga = GigaChatAsyncClient(credentials=token, verify_ssl_certs=False)

    async def ask(self, prompt: str, message: str):
        payload = Chat(
            messages = [
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=prompt
                ),
                Messages(
                    role=MessagesRole.USER,
                    content=message
                )
            ]
        )
        response = await self._giga.achat(payload)
        return response.choices[0].message.content
