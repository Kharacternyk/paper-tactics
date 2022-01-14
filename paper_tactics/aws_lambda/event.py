import json

from paper_tactics.on_demand_dict import OnDemandDict


class LambdaEvent(OnDemandDict):
    def __init__(self, event_dict):
        super().__init__()
        self._event_dict = event_dict

    @property
    def connection_id(self):
        return self._event_dict["requestContext"]["connectionId"]

    @property
    def game_id(self):
        return self._body["gameId"]

    @property
    def cell(self):
        def get_cell():
            cell = self._body["cell"]
            assert len(cell) == 2
            return cell

        return self.get("cell", get_cell)

    @property
    def _body(self):
        return self.get("body", lambda: json.loads(self._event_dict["body"]))
