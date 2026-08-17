class Board():
    def __init__(self, board_size: int = 9) -> None:
        self.board_size = board_size
        self.status_dict = {_: 0 for _ in range(0, board_size)}

    def draw(self) -> None:
        initial_index = 0

        for _ in range(int(self.board_size ** 0.5)):
            print(" -------------")

            for i in range(initial_index, initial_index + int(self.board_size ** 0.5)):
                if self.status_dict[i] == 0:
                    print(f" |  ", end="")
                elif self.status_dict[i] == -1:
                    print(f" | O", end="")
                else:
                    print(f" | X", end="")

            print(" | ")

        print(" -------------")
