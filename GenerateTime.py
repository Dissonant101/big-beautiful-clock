from datetime import datetime, timezone


class GenerateTimeString():
    def __init__(self) -> None:
        self.numbers = {
            0: [[True, True, True, True], [True, False, False, True], [True, False, False, True], [True, True, True, True], [True, False, False, True], [True, False, False, True], [True, True, True, True]],
            1: [[False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True]],
            2: [[], [], [], [], [], [], []],
            3: [[], [], [], [], [], [], []],
            4: [[], [], [], [], [], [], []],
            5: [[], [], [], [], [], [], []],
            6: [[], [], [], [], [], [], []],
            7: [[], [], [], [], [], [], []],
            8: [[], [], [], [], [], [], []],
            9: [[], [], [], [], [], [], []]
        }

    def parse_time_object(dt: datetime) -> tuple:
        am = True
        actual_hours = dt.hour

        if dt.hour > 12:
            actual_hours = dt.hour - 12
            am = False

        return actual_hours, dt.minute, dt.second, am

    def generate_string(self, time_info: tuple) -> str:
        final_string = ""

        for y in range(7):
            final_string += "⬛" * 4
            if time_info[0] > 9:
                for x in self.numbers[1][y]:
                    final_string += "🟩" if x else "⬛"
                final_string += "⬛"
            for x in self.numbers[time_info[0] % 10][y]:
                final_string += "🟩" if x else "⬛"

            final_string += "⬛⬜" if y == 1 or y == 5 else "⬛⬛"  # colons

            for x in self.numbers[time_info[1] // 10][y]:
                final_string += "🟩" if x else "⬛"
            for x in self.numbers[time_info[1] % 10][y]:
                final_string += "🟩" if x else "⬛"

            final_string += "⬛⬜" if y == 1 or y == 5 else "⬛⬛"  # colons

            for x in self.numbers[time_info[2] // 10][y]:
                final_string += "🟩" if x else "⬛"
            for x in self.numbers[time_info[2] % 10][y]:
                final_string += "🟩" if x else "⬛"

        return
