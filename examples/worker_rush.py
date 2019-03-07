from sc2 import run_game, maps, Race, Difficulty, BotAI
from sc2.player import Bot, Computer
import time

start = time.time()

class WorkerRushBot(BotAI):
    def __init__(self):
        super().__init__()
        self.actions = []
        
    def on_end(self, game_result):
        print('--- on_end called ---')
        print("Game Time: {}".format(self.game_time))

        if game_result == Result.Victory:
            np.save("train_data/{}.npy".format(str(int(time.time()))), np.array(self.train_data))


    async def on_step(self, iteration):
        self.game_time = (self.state.game_loop/22.4) / 60
        self.actions = []

        if iteration == 0:
            target = self.enemy_start_locations[0]

            for worker in self.workers:
                self.actions.append(worker.attack(target))

        await self.do_actions(self.actions)

def main():
    run_game(maps.get("Abyssal Reef LE"), [
        Bot(Race.Zerg, WorkerRushBot()),
        Computer(Race.Protoss, Difficulty.Medium)
    ], realtime=False)

if __name__ == '__main__':
    main()
    print("Elapsed Time: {}".format( time.time() - start ))
