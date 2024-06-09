from telebot import TeleBot
from telebot.types import Message, User, Chat
import pytest
from unittest.mock import Mock, patch
import main
import dialog_manager
class MockBot(TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.sent_messages = []

    def send_message(self, chat_id, text, **kwargs):
        self.sent_messages.append((chat_id, text))

    def send_chat_action(self, chat_id, action):
        pass

@pytest.fixture
def bot():
    mock_bot = MockBot(main.TG_TOKEN)
    main.bot = mock_bot
    return mock_bot

@patch('dialog_manager.bot_utils.File')
@patch('dialog_manager.bot_utils.States')
@patch('main.extract_chat_data')
def test_bot_message(mock_extract_chat_data, MockScreenManager, MockFile, bot):
    mock_extract_chat_data.return_value = (123, '/start')
    mock_screen = MockScreenManager.return_value
    mock_screen.current_screen.return_value.run.return_value = [("Welcome to the bot!", None)]
    mock_screen.current_screen.return_value.next_screen_name = 'next_screen'

    user = User(1, False, 'TestUser')
    chat = Chat(1, 'private')
    message = Message(
        message_id=1,
        from_user=user,
        date=None,
        chat=chat,
        content_type='text',
        options={},
        json_string={'text': '/start'}
    )
    
    main.command_handler(message)
    
    assert len(bot.sent_messages) > 0
    assert bot.sent_messages[0][1] == "Welcome to the bot!"
    mock_extract_chat_data.assert_called_once_with(message)
    mock_screen.current_screen.assert_called_once_with(123, '/start')
    mock_screen.update_screen.assert_called_once_with(123, 'next_screen')
