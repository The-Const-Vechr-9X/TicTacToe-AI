class Board:
    def __init__(self, board_size: int = 9) -> None:
        self.board_size = board_size
        self.value_list = [" " for _ in range(board_size)]

    def is_valid_cell(self, index_cell: int) -> bool:
        return self.value_list[index_cell] == " "

    def is_full(self) -> bool:
        for i in range(self.board_size):
            if " " == self.value_list[i]:
                return False

        return True

    def is_win(self, symbol: str, line_length: int = 3) -> bool:
        """
        Направления: (dx, dy)
        (1,0) - вправо, (0,1) - вниз, (1,1) - диагональ \\, (1,-1) - диагональ /
        """
        sqrt_size = int(self.board_size**0.5)
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for i in range(self.board_size):
            x = i % sqrt_size
            y = i // sqrt_size

            if self.value_list[i] != symbol:
                continue

            for dx, dy in directions:
                end_x = x + dx * (line_length - 1)
                end_y = y + dy * (line_length - 1)

                if end_x < 0 or end_x >= sqrt_size or end_y < 0 or end_y >= sqrt_size:
                    continue

                win = True
                for step in range(line_length):
                    index = (y + dy * step) * sqrt_size + (x + dx * step)
                    if self.value_list[index] != symbol:
                        win = False
                        break

                if win:
                    return True

        return False

    def update_value_list(self, index_cell: int, symbol: str) -> None:
        self.value_list[index_cell] = symbol
