import json
import os


class Settings:
    FILENAME = "data.json"

    def __init__(self) -> None:
        if not os.path.exists(self.FILENAME):
            self.reset_settings()
        else:
            self.read_settings()

    def create_settings(self) -> None:
        with open(self.FILENAME, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    def read_settings(self) -> None:
        try:
            with open(self.FILENAME, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.board_size = data["board_size"]
                self.mode = data["mode"]
                self.difficulty = data["difficulty"]
        except (json.JSONDecodeError, KeyError, FileNotFoundError):
            self.reset_settings()

    def update_settings(self, board_size: int, mode: str, difficulty: str) -> None:
        self.board_size = board_size
        self.mode = mode
        self.difficulty = difficulty

        with open(self.FILENAME, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

    def reset_settings(self) -> None:
        self.board_size = 9
        self.mode = "pve"
        self.difficulty = "easy"
        self.create_settings()

    def formatted_settings(self) -> dict[str, str]:
        sqrt_size = int(self.board_size**0.5)
        result: dict[str, str] = {
            "Размер доски": f"{sqrt_size}x{sqrt_size}",
            "Режим игры": self.mode,
            "Сложность": self.difficulty
        }

        return result

    def to_dict(self) -> dict[str, int | str]:
        result: dict[str, int | str] = {
            "board_size": self.board_size,
            "mode": self.mode,
            "difficulty": self.difficulty,
        }

        return result
