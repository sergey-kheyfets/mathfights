from abc import ABC, abstractmethod
from classes import Team, Game, GameResult
from random import shuffle


class BaseTournament(ABC):
    def __init__(self, teams: list[Team], is_draw: bool = False) -> None:
        self.teams = teams
        self._draw(is_shuffle = is_draw)
        self.games: list[Game] = list()
        self.points: dict[str, tuple[int, int]] = {t.team_name: (0, 0) for t in teams}
        self.games_played: int = 0
        self._create_games()

    def _draw(self, is_shuffle: bool) -> None:
        if is_shuffle:
            shuffle(self.teams)

    def set_score(self, game_index: int, score_1: int, score_2: int) -> None:
        if self.games[game_index - 1].result == GameResult.NotStarted and score_1*score_2 > 0:
            self.games_played += 1
        elif self.games[game_index - 1].result != GameResult.NotStarted and score_1 == score_2 == 0:
            self.games_played -= 1
        self.games[game_index - 1].set_score(score_1, score_2)
        self._recount_points(self.games[game_index - 1].team_1)
        self._recount_points(self.games[game_index - 1].team_2)

    def _recount_points(self, t: Team) -> None:
        self.points[t.team_name] = (0, 0)
        for game in self.games:
            self.points[t.team_name][0] += game.get_team_points(t.team_name)
            self.points[t.team_name][1] += game.get_team_scores(t.team_name)

    @abstractmethod
    def _create_games(self) -> None:
        pass

    @abstractmethod
    def update_schedule(self) -> None:
        pass

    @abstractmethod
    def remove_update(self) -> None:
        pass


class SwissTournament(BaseTournament):
    """
    Турнир на чётное кол-во команд по швейцарской системе на 4 тура
    """
    def __init__(self, teams: list[Team], is_draw: bool = False) -> None:
        if len(self.teams) < 6:
            raise ValueError(f"Требуется зарегистрировать хотя бы 6 команд. Зарегистрировано: {len(teams)}")
        if len(self.teams) % 2 != 0:
            raise ValueError(f"Турнир разработан для чётного кол-ва команд. Зарегистрировано: {len(teams)}")
        self.not_played: dict[str, set[str]] = {T.team_name: {t.team_name for t in teams} for T in teams}
        for i in range(len(teams)):
            self.not_played[i].pop(teams[i].team_name)
        self.rounds_created = 0
        super().__init__(teams, is_draw)
    
    def _create_games(self) -> None:
        self._create_new_round()

    def _create_new_round(self) -> None:
        self.rounds_created += 1
        rate: list[Team] = list(*self.teams)
        rate.sort(key=lambda t: self.points[t.team_name])
        new_pairs: list[list[Team]] = list()
        fail_counter = 0
        while len(rate) > 0:
            result = self._search_pair(rate)
            while result is None:
                fail_counter += 1
                p = new_pairs.pop()
                rate = [p[1], *rate, p[0]]
                result = self._search_pair(rate)
            new_pairs.append(result)
            if fail_counter < len(rate):
                rate = [*rate[fail_counter:], *rate[:fail_counter]]
        for p in new_pairs:
            self.games.append(Game(p[0], p[1]))

    def _search_pair(self, rate: list[Team]):
        top_team = rate.pop()
        for t in rate[::-1]:
            if t.team_name in self.not_played[top_team.team_name]:
                rate.pop(rate.index(t.team_name))
                return [top_team, t]
        else:
            rate.append(top_team)
            return None
    
    def update_schedule(self) -> None:
        if self.games_played % (len(self.teams) // 2) == 0:
            self._create_new_round()

    def remove_update(self):
        if len(self.games) > 0:
            self.games = self.games[:-len(self.teams) // 2]


class ClassicTournament(BaseTournament):
    """
    Классический турнир на 8 команд, поделённых на 2 группы и играющих
    в последний день матчи за 1-2, 3-4, 5-6, 7-8 места
    """
    def __init__(self, teams: list[Team], is_draw: bool = False) -> None:
        if len(teams) != 8:
            raise ValueError(f"Турнир разработан для 8 команд. Зарегистрировано: {len(teams)}")
        super().__init__(teams, is_draw)

    def _draw(self, is_shuffle) -> None:
        super()._draw(is_shuffle)
        self.A: list[Team] = self.teams[:4]
        self.B: list[Team] = self.teams[4:]
    
    def _create_games(self) -> None:
        self.games = list()
        index_pairs = [(0, 1), (2, 3), (0, 2), (1, 3), (3, 0), (2, 1)]
        for i in range(0, 6, 2):
            i_p_1, i_p_2 = index_pairs[i], index_pairs[i+1]
            self.games.append(Game(self.A[i_p_1[0]], self.A[i_p_1[1]]))
            self.games.append(Game(self.A[i_p_2[0]], self.A[i_p_2[1]]))
            self.games.append(Game(self.B[i_p_1[0]], self.B[i_p_1[1]]))
            self.games.append(Game(self.B[i_p_2[0]], self.B[i_p_2[1]]))

    def _create_finals(self) -> None:
        A_rate: list[Team] = list(*self.A)
        A_rate.sort(key = lambda t: self.points[t.team_name])
        B_rate: list[Team] = list(*self.B)
        B_rate.sort(key = lambda t: self.points[t.team_name])
        for i in range(4):
            self.games.append(Game(A_rate[i], B_rate[i]))

    def update_schedule(self) -> None:
        if self.games_played == 12:
            self._create_finals()

    def remove_update(self) -> None:
        if len(self.games) == 16:
            self.games = self.games[:12]
