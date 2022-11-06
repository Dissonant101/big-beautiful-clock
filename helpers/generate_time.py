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
        self.days = [[[True, True, False], [True, False, True], [True, False, True], [True, False, True], [True, False, True], [True, False, True], [True, True, False]],
                     [[False, True, True, False], [True, False, False, True], [True, False, False, True], [
                         True, True, True, True], [True, False, False, True], [True, False, False, True], [True, False, False, True]],
                     [[True, False, True], [True, False, True], [True, False, True], [False, True, False], [
                         False, True, False], [False, True, False], [False, True, False]],
                     [[True, True, True], [True, False, False], [True, False, False], [
                         True, True, True], [False, False, True], [False, False, True], [True, True, True]]
                     ]

    def parse_time_object(self, dt: datetime) -> tuple:
        return dt.hour, dt.minute, dt.second

    def parse_delta_object(self, td: timedelta) -> tuple:
        return td.days * 24, td.seconds // 60, td.seconds % 60

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

    def generate_day_string(self, num_days: int) -> str:
        final_string = ""

        for y in range(7):
            final_string += "⬛"

            for x in self.numbers[num_days // 10][y]:
                final_string += "🟩" if x else "⬛"
            final_string += "⬛"
            for x in self.numbers[num_days % 10][y]:
                final_string += "🟩" if x else "⬛"
            final_string += "⬛⬛⬛"

            for letter in self.days:
                for x1 in letter[y]:
                    final_string += "🟩" if x1 else "⬛"
                final_string += "⬛"

            final_string += "\n"

        return final_string


if __name__ == "__main__":
    generator = GenerateTimeString()
    print(generator.generate_day_string(15))
