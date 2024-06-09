from telebot import TeleBot
from telebot.types import Message, User, Chat
import pytest
import main

class MockBot(TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.sent_messages = []

    def send_message(self, chat_id, text, **kwargs):
        self.sent_messages.append((chat_id, text))

@pytest.fixture
def bot():
    mock_bot = MockBot("7158514154:AAFeFxYJrzWbC_-IHDDk6Y609uI7GgH0gSQ")
    main.bot = mock_bot
    return mock_bot

def test_bot_message(bot):
    user = User(1, False, 'TestUser')
    chat = Chat(1, 'private')
    message = Message(
        message_id=1,
        from_user=user,
        date=None,
        chat=chat,
        content_type='text',
        json_string={'text': '/start'}
    )
    main.handle_start(message)
    assert len(bot.sent_messages) > 0
    assert bot.sent_messages[0][1] == "Welcome to the bot!"
