from datetime import datetime, timezone, timedelta


class GenerateTimeString():
    def __init__(self) -> None:
        self.numbers = {
            0: [[True, True, True], [True, False, True], [True, False, True], [True, False, True], [True, False, True], [True, False, True], [True, True, True]],
            1: [[False, True], [False, True], [False, True], [False, True], [False, True], [False, True], [False, True]],
            2: [[True, True, True], [False, False, True], [False, False, True], [True, True, True], [True, False, False], [True, False, False], [True, True, True]],
            3: [[True, True, True], [False, False, True], [False, False, True], [True, True, True], [False, False, True], [False, False, True], [True, True, True]],
            4: [[True, False, True], [True, False, True], [True, False, True], [True, True, True], [False, False, True], [False, False, True], [False, False, True]],
            5: [[True, True, True], [True, False, False], [True, False, False], [True, True, True], [False, False, True], [False, False, True], [True, True, True]],
            6: [[True, True, True], [True, False, False], [True, False, False], [True, True, True], [True, False, True], [True, False, True], [True, True, True]],
            7: [[True, True, True], [False, False, True], [False, False, True], [False, False, True], [False, False, True], [False, False, True], [False, False, True]],
            8: [[True, True, True], [True, False, True], [True, False, True], [True, True, True], [True, False, True], [True, False, True], [True, True, True]],
            9: [[True, True, True], [True, False, True], [True, False, True], [True, True, True], [False, False, True], [False, False, True], [True, True, True]]
        }

    def parse_time_object(self, dt: datetime) -> tuple:
        return dt.hour, dt.minute, dt.second

    def generate_string(self, time_info: tuple) -> str:
        final_string = ""

        for y in range(7):
            for x in self.numbers[time_info[0] // 10][y]:
                final_string += "🟩" if x else "⬛"
            final_string += "⬛"
            for x in self.numbers[time_info[0] % 10][y]:
                final_string += "🟩" if x else "⬛"

            final_string += "⬛⬜⬛" if y == 1 or y == 5 else "⬛⬛⬛"  # colons

            for x in self.numbers[time_info[1] // 10][y]:
                final_string += "🟩" if x else "⬛"
            final_string += "⬛"
            for x in self.numbers[time_info[1] % 10][y]:
                final_string += "🟩" if x else "⬛"

            final_string += "⬛⬜⬛" if y == 1 or y == 5 else "⬛⬛⬛"  # colons

            for x in self.numbers[time_info[2] // 10][y]:
                final_string += "🟩" if x else "⬛"
            final_string += "⬛"
            for x in self.numbers[time_info[2] % 10][y]:
                final_string += "🟩" if x else "⬛"

            final_string += "\n"

        return final_string


if __name__ == "__main__":
    generator = GenerateTimeString()
    print(generator.generate_string(
        generator.parse_time_object(datetime.now())))
