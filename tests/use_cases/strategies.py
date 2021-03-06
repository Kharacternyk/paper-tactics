from hypothesis.strategies import booleans, composite, iterables

from tests.entities.strategies import match_requests
from tests.use_cases.mocked_ports import MockedMatchRequestQueue, MockedPlayerNotifier


@composite
def match_request_queues(draw) -> MockedMatchRequestQueue:
    return MockedMatchRequestQueue(draw(iterables(match_requests())))


@composite
def player_notifiers(draw) -> MockedPlayerNotifier:
    return MockedPlayerNotifier(draw(booleans()), draw(booleans()))
