from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class TeamRole(Enum):
    Player = 0
    Captian = 1
    Coach = 2
    Referee = 3


@dataclass
class Person:
    name: str
    school: str
    role: TeamRole = TeamRole.Player

    @staticmethod
    def unknown() -> Person:
        return Person('NoName', '')


@dataclass
class Team:
    team_name: str
    coach: Person = field(default_factory=Person.unknown)
    captain: Person = field(default_factory=Person.unknown)
    players: list[Person] = field(default_factory=list)

    @staticmethod
    def unknown() -> Team:
        return Team('Unknown')


class GameResult(Enum):
    NotStarted = -1
    Draw = 0
    Win1 = 1
    Win2 = 2


class Game:
    def __init__(
            self,
            index: int,
            team_1: Team = Team.unknown(),
            team_2: Team = Team.unknown()
        ) -> None:
        self.index: int = index
        self.team_1: Team = team_1
        self.team_2: Team = team_2
        self.game_1: Game | None = None
        self.game_2: Game | None = None
        self.game_next: Game | None = None
        self.referees: list[Person] = list()
        self.set_score(0, 0)

    def __str__(self) -> str:
        team_str_1, team_str_2 = '', ''
        if self.team_1 != Team.unknown():
            team_str_1 = self.team_1.team_name
        elif self.game_1 is not None:
            team_str_1 = f"Победитель матча №{self.game_1.index}"
        else:
            return 'Undefined game'
        if self.team_2 != Team.unknown():
            team_str_2 = self.team_2.team_name
        elif self.game_2 is not None:
            team_str_2 = f"Победитель матча №{self.game_2.index}"
        else:
            return 'Undefined game'
        return f"{self.index}| {team_str_1} {self.score_1}:{self.score_2} {team_str_2}"
    
    def __repr__(self) -> str:
        return str(self)

    def set_referees(self, referees: list[Person]) -> None:
        self.referees = referees

    def set_score(self, score_1: int, score_2: int) -> None:
        self.score_1 = score_1
        self.score_2 = score_2
        if score_1 == score_2 == 0:
            self.result = GameResult.NotStarted
        elif abs(score_2 - score_1) < 4:
            self.result = GameResult.Draw
        elif score_1 > score_2:
            self.result = GameResult.Win1
        else:
            self.result = GameResult.Win2

    def get_points(self) -> tuple[int, int]:
        if self.result == GameResult.Win1:
            return 2, 0
        if self.result == GameResult.Win2:
            return 0, 2
        if self.result == GameResult.Draw:
            return 1, 1
        return 0, 0

    def get_team_points(self, team_name: str) -> int:
        points = self.get_points()
        if team_name == self.team_1.team_name: 
            return points[0]
        if team_name == self.team_2.team_name:
            return points[1]
        return 0
    
    def update(self) -> None:
        if self.game_1 is not None:
            if self.game_1.result == GameResult.Win1:
                self.team_1 = self.game_1.team_1
            if self.game_1.result == GameResult.Win2:
                self.team_1 = self.game_1.team_2
        if self.game_2 is not None:
            if self.game_2.result == GameResult.Win1:
                self.team_2 = self.game_2.team_1
            if self.game_2.result == GameResult.Win2:
                self.team_2 = self.game_2.team_2
    
    def is_one_team_game(self) -> bool:
        """
        Вернёт True, если эта игра - слот для одной команды. 
        Например, при игре в группе с нечётным кол-вом команд или неполной сеткой плэй-офф
        """
        return (self.team_1 != Team.unknown()) and (self.team_2 == Team.unknown()) and (self.game_2 is None)
    
    def match_team_and_game(self, team: Team, game: Game) -> None:
        """
        Создание игры для будущего раунда плэй-офф при одной известной команде
        """
        self.team_1 = team
        self.game_2: Game = game
        game.game_next = self

    def match_games(self, game_1: Game, game_2: Game) -> None:
        """
        Создание игры для будущего раунда плэй-офф
        """
        self.game_1: Game = game_1
        game_1.game_next = self
        self.game_2: Game = game_2
        game_2.game_next = self
