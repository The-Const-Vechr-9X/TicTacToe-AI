class Board():
    def __init__(self, board_size: int = 9) -> None:
        self.board_size = board_size
        self.status_dict = {_: 0 for _ in range(0, board_size)}

    def draw(self) -> None:
        initial_index = 0
        sqrt_board_size = int(self.board_size ** 0.5)

        for _ in range(sqrt_board_size):
            print(" -" + "----" * sqrt_board_size)

            for i in range(initial_index, initial_index + sqrt_board_size):
                if self.status_dict[i] == 0:
                    print(f" |  ", end="")
                elif self.status_dict[i] == -1:
                    print(f" | O", end="")
                else:
                    print(f" | X", end="")

            print(" | ")

        print(" -" + "----" * sqrt_board_size)
