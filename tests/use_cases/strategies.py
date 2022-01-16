from hypothesis.strategies import booleans
from hypothesis.strategies import composite
from hypothesis.strategies import text

from tests.use_cases.mocked_ports import MockedPlayerNotifier
from tests.use_cases.mocked_ports import MockedPlayerQueue


@composite
def player_queues(draw) -> MockedPlayerQueue:
    return MockedPlayerQueue(draw(text()) if draw(booleans()) else None)


@composite
def player_notifiers(draw) -> MockedPlayerNotifier:
    return MockedPlayerNotifier(draw(booleans()), draw(booleans()))
