from threading import Thread
from time import sleep
from typing import Tuple, List
from dataclasses import dataclass, field
from teamfightchaticts.settings import TwitchSettings
from teamfightchaticts.tft_command import TFTCommand
from teamfightchaticts.twitch_connection import TwitchConnection, LineBuffer


@dataclass
class IrcSocketMock:
    text_to_return: str
    text_received: str=''
    closed: bool=True
    buffer_id: int=0
    encoding: str='utf-8'

    def connect(self, _: Tuple[str, int]):
        self.closed = False

    def close(self):
        self.closed = True

    def recv(self, bufsize: int) -> bytes:
        text_enc = self.text_to_return.encode(self.encoding)
        start, end = self.buffer_id * bufsize, (self.buffer_id + 1) * bufsize
        self.buffer_id += 1
        sleep(0.01)
        return text_enc[start:min(end, len(text_enc))] if start < len(text_enc) else bytes([])

    def send(self, data: bytes) -> int:
        self.text_received += data.decode(self.encoding)
        sleep(0.01)


@dataclass
class RemoteControlMock:
    received_commands: List[TFTCommand]=field(init=False, default_factory=list)

    def execute_cmd(self, tft_cmd: TFTCommand):
        self.received_commands.append(tft_cmd)


def msg_padding(sequence: str, repetitions: int, separator: str=''):
    return separator.join([sequence for _ in range(repetitions)])


def test_should_connect_to_chat():
    conn_settings = TwitchSettings('foobar.com', 6667, 'twitch_test', 'my_chatbot', 'somepwd')
    text_to_return = "End of /NAMES list\r\n"
    connection = TwitchConnection(conn_settings, lambda: IrcSocketMock(text_to_return))
    connection.connect_to_server()
    exp_text_buffer = 'PASS somepwd\nNICK my_chatbot\nJOIN #twitch_test\n'
    socket: IrcSocketMock = connection.websocket
    assert not socket.closed and socket.text_received == exp_text_buffer


# def test_should_fail_to_connect_to_chat_after_timeout():
#     # TODO: use asyncio for this feature. threads are very clunky to achieve this.
#     conn_settings = TwitchSettings('twitch.tv', 6667, 'twitch_test', 'my_chatbot', 'somepwd')
#     connection = TwitchConnection(conn_settings, lambda: IrcSocketMock(''), timeout_seconds=0.5)
#     connection.connect_to_server()
#     sleep(0.6)
#     print(connection)
#     assert connection.irc is None


# # TODO: make this test work
def test_should_disconnect_from_chat_gracefully():
    conn_settings = TwitchSettings('twitch.tv', 6667, 'twitch_test', 'my_chatbot', 'somepwd')
    text_to_return = "End of /NAMES list\r\n" + msg_padding(' ', 1024) \
        + "\r\n::w3w4\r\n::lock\r\n::some text\r\n::lvl\r\n"
    connection = TwitchConnection(conn_settings, lambda: IrcSocketMock(text_to_return))
    msgs_received: List[TFTCommand] = []
    shutdown_requested = False

    def observe_twitch_chat():
        connection.connect_to_server()
        connection.register_message_listener(msgs_received.append)
        connection.receive_messages_as_daemon(lambda: shutdown_requested)
    conn_thread = Thread(target=observe_twitch_chat)
    conn_thread.start()

    sleep(1)
    shutdown_requested = True
    conn_thread.join(timeout=0.1)

    assert set(['w3w4', 'lock', 'lvl']) <= set(msgs_received)


def test_line_buffer():
    def process_read_buffer(text_buffer, remainder):
        buf = LineBuffer(remainder)
        return buf.process(text_buffer), buf.remainder

    assert process_read_buffer('', '') == ([], '')
    assert process_read_buffer('', 'abc') == ([], 'abc')
    assert process_read_buffer('abc\r\n', '') == (['abc'], '')
    assert process_read_buffer('abc\r\ndef', '') == (['abc'], 'def')
    assert process_read_buffer('abc\r\ndef\r\nghi', '') == (['abc', 'def'], 'ghi')
    assert process_read_buffer('\ndef', 'abc\r') == (['abc'], 'def')
    assert process_read_buffer('\r\ndef', 'abc') == (['abc'], 'def')
    assert process_read_buffer('abc\r\ndef\r\n', '') == (['abc', 'def'], '')


def test_should_send_chat_pong():
    conn_settings = TwitchSettings('twitch.tv', 6667, 'twitch_test', 'my_chatbot', 'somepwd')
    text_to_return = "End of /NAMES list\r\n" + msg_padding(' ', 1024) \
        + "\r\n::w3w4\r\n::lock\r\n::some text\r\nPING :tmi.twitch.tv\r\n::lvl\r\n"
    connection = TwitchConnection(conn_settings, lambda: IrcSocketMock(text_to_return))
    shutdown_requested = False

    def observe_twitch_chat():
        connection.connect_to_server()
        connection.receive_messages_as_daemon(lambda: shutdown_requested)
    conn_thread = Thread(target=observe_twitch_chat)
    conn_thread.start()

    sleep(1)
    shutdown_requested = True
    conn_thread.join(timeout=0.1)

    socket: IrcSocketMock = connection.websocket
    assert 'PONG :tmi.twitch.tv' in socket.text_received


# TODO: test the chatbot with all kinds of emoticons and make sure it doesn't crash
