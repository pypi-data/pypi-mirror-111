from dcss.agent.base import BaseAgent
from dcss.state.game import GameState
from dcss.actions.action import Action
from dcss.actions.command import Command
from dcss.websockgame import WebSockGame
from dcss.connection.config import WebserverConfig

import random


class MyAgent(BaseAgent):

    def __init__(self):
        super().__init__()
        self.gamestate = None

    def action_sequence(self):
        actions = [Command.MOVE_OR_ATTACK_E,
                   Command.CHARACTER_OVERVIEW]
        return actions

    def get_action(self, gamestate: GameState):
        self.gamestate = gamestate
        # get all possible actions
        actions = Action.get_all_move_commands()
        # pick an action at random
        print(self.gamestate.get_player_stats_vector(verbose=True))
        return random.choice(self.action_sequence())


if __name__ == "__main__":
    my_config = WebserverConfig

    # set game mode to Tutorial #1
    my_config.game_id = 'dcss-web-trunk'
    my_config.always_start_new_game = False
    my_config.auto_start_new_game = False

    # create game
    game = WebSockGame(config=my_config, agent_class=MyAgent)
    game.run()
