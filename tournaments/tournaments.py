import math
from abc import ABC, abstractmethod
from classes import Team, Game
from random import shuffle


class BaseTournament(ABC):
    def __init__(self, teams: list[Team], is_draw: bool = False) -> None:
        self.teams = teams
        if is_draw:
            self.draw()
        self.games: list[Game] = list()
        self._create_games()

    def draw(self) -> None:
        shuffle(self.teams)

    def set_score(self, game_index: int, score_1: int, score_2: int) -> None:
        self.games[game_index - 1].set_score(score_1, score_2)
        if self.games[game_index - 1].game_next is not None:
            self.games[game_index - 1].game_next.update()

    @abstractmethod
    def _create_games(self) -> None:
        pass


class PlayOffTournament(BaseTournament):
    def __init__(self, teams: list[Team], is_draw: bool = False) -> None:
        super().__init__(teams, is_draw)
    
    def _create_games(self) -> None:
        index_game = 1
        self.games = list()
        last_n = (1 << math.ceil(math.log2(len(self.teams))))
        round_games: list[Game] = list()
        for t_ind in range(last_n // 2, len(self.teams)):
            game = Game(index_game, self.teams[last_n - t_ind - 1], self.teams[t_ind])
            index_game += 1
            self.games.append(game)
            round_games.append(game)
        for t_ind in range(last_n - len(self.teams) - 1, -1, -1):
            round_games.append(Game(0, self.teams[t_ind]))
        last_n //= 2
        while last_n > 1:
            new_round: list[Game] = list()
            for r_ind in range(last_n // 2):
                game = Game(index_game)
                index_game += 1
                if round_games[-r_ind-1].is_one_team_game():
                    game.match_team_and_game(round_games[-r_ind-1].team_1, round_games[r_ind])
                else:
                    game.match_games(round_games[-r_ind-1], round_games[r_ind])
                new_round.append(game)
                self.games.append(game)
            last_n //= 2
            round_games = new_round


# teams: list[Team] = [Team(f"Команда №{i+1}") for i in range(26)]
# T = PlayOffTournament(teams)
# for g in T.games:
#     print(g)
# print()
# T.set_score(1, 23, 13)
# T.set_score(10, 6, 27)
# T.set_score(6, 9, 12)
# for g in T.games:
#     print(g)
