import json
from dataclasses import asdict, dataclass

from paper_tactics.entities.player_view import PlayerView


@dataclass
class GameView:
    id: str
    size: int
    turns_left: int
    my_turn: bool
    me: PlayerView
    opponent: PlayerView

    def to_json(self) -> str:
        game_dict = asdict(self)
        for player_view in game_dict["me"], game_dict["opponent"]:
            for key in player_view:
                if isinstance(player_view[key], set):
                    player_view[key] = list(player_view[key])
        return json.dumps(game_dict, separators=(",", ":"))
