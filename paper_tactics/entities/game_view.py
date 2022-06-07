import json
from dataclasses import asdict, dataclass

from paper_tactics.entities.cell import Cell
from paper_tactics.entities.game import Game
from paper_tactics.entities.player import Player


@dataclass
class PlayerView:
    units: set[Cell]
    walls: set[Cell]
    reachable: set[Cell]
    view_data: dict[str, str]
    is_gone: bool
    is_defeated: bool

    def __init__(self, player: Player):
        self.units = player.units.copy()
        self.walls = player.walls.copy()
        self.reachable = player.reachable.copy()
        self.is_gone = player.is_gone
        self.is_defeated = player.is_defeated
        self.view_data = player.view_data.copy()


@dataclass
class GameView:
    id: str
    size: int
    turns_left: int
    my_turn: bool
    me: PlayerView
    opponent: PlayerView

    def __init__(self, game: Game, player_id: str):
        self.id = game.id
        self.size = game.size
        self.turns_left = game.turns_left

        if player_id == game.active_player.id:
            self.my_turn = True
            self.me = PlayerView(game.active_player)
            self.opponent = PlayerView(game.passive_player)
        elif player_id == game.passive_player.id:
            self.my_turn = False
            self.me = PlayerView(game.passive_player)
            self.opponent = PlayerView(game.active_player)
        else:
            raise ValueError("No such player")

    def to_json(self) -> str:
        game_dict = asdict(self)
        for player_view in game_dict["me"], game_dict["opponent"]:
            for key in player_view:
                if isinstance(player_view[key], set):
                    player_view[key] = list(player_view[key])
        return json.dumps(game_dict, separators=(",", ":"))
