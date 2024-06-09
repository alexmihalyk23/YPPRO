# test_bot.py
import pytest
from telebot import TeleBot
from telebot.types import Message
import main


class MockBot(TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.sent_messages = []

    def send_message(self, chat_id, text, **kwargs):
        self.sent_messages.append((chat_id, text))

@pytest.fixture
def bot():
    mock_bot = MockBot("YOUR_BOT_TOKEN")
    main.bot = mock_bot
    return mock_bot

def test_bot_message(bot):
    message = Message(message_id=1, from_user=None, date=None, chat=None, content_type='text', json_string={})  # Поправлено здесь
    message.text = '/start'
    main.handle_start(message)
    assert len(bot.sent_messages) > 0
    assert bot.sent_messages[0][1] == "Welcome to the bot!"
