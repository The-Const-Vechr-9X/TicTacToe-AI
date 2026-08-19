class Board():
    def __init__(self, board_size: int = 9) -> None:
        self.board_size = board_size
        self.value_dict = {_: ' ' for _ in range(0, board_size)}

    def draw(self) -> None:
        index = 0
        sqrt_board_size = int(self.board_size ** 0.5)

        for _ in range(sqrt_board_size):
            print(" -" + "----" * sqrt_board_size)

            for _ in range(index, index + sqrt_board_size):
                print(f" | {self.value_dict[index]}", end="")
                index += 1

            print(" | ")

        print(" -" + "----" * sqrt_board_size)
