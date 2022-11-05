from datetime import datetime, timezone


class GenerateTimeString():
    def __init__(self) -> None:
        self.numbers = {
            0: [[True, True, True, True], [True, False, False, True], [True, False, False, True], [True, False, False, True], [True, False, False, True], [True, False, False, True], [True, True, True, True]],
            1: [[False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True]],
            2: [[True, True, True, True], [False, False, False, True], [False, False, False, True], [True, True, True, True], [True, False, False, False], [True, False, False, False], [True, True, True, True]],
            3: [[True, True, True, True], [False, False, False, True], [False, False, False, True], [True, True, True, True], [False, False, False, True], [False, False, False, True], [True, True, True, True]],
            4: [[True, False, False, True], [True, False, False, True], [True, False, False, True], [True, True, True, True], [False, False, False, True], [False, False, False, True], [False, False, False, True]],
            5: [[True, True, True, True], [True, False, False, False], [True, False, False, False], [True, True, True, True], [False, False, False, True], [False, False, False, True], [True, True, True, True]],
            6: [[True, True, True, True], [True, False, False, False], [True, False, False, False], [True, True, True, True], [True, False, False, True], [True, False, False, True], [True, True, True, True]],
            7: [[True, True, True, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True], [False, False, False, True]],
            8: [[True, True, True, True], [True, False, False, True], [True, False, False, True], [True, True, True, True], [True, False, False, True], [True, False, False, True], [True, True, True, True]],
            9: [[True, True, True, True], [True, False, False, True], [True, False, False, True], [True, True, True, True], [False, False, False, True], [False, False, False, True], [True, True, True, True]]
        }
        self.indicators = {
            "AM": [[False, False, False, False, False, False, False, False, False], [False, True, False, False, True, False, False, False, True], [True, False, True, False, True, True, False, True, True], [True, True, True, False, True, True, True, True, True], [True, False, True, False, True, False, True, False, True], [True, False, True, False, True, False, True, False, True], [False, False, False, False, False, False, False, False, False]],
            "PM": [[False, False, False, False, False, False, False, False, False], [True, True, True, False, True, False, False, False, True], [True, False, True, False, True, True, False, True, True], [True, True, True, False, True, True, True, True, True], [True, False, False, False, True, False, True, False, True, ], [True, False, False, False, True, False, True, False, True, ], [False, False, False, False, False, False, False, False, False]]
        }

    def parse_time_object(dt: datetime) -> tuple:
        am = True
        actual_hours = dt.hour

        if dt.hour > 12:
            actual_hours = dt.hour - 12
            am = False

        return actual_hours, dt.minute, dt.second, am

    def generate_string(self, time_info: tuple, current_time: bool) -> str:
        final_string = ""

        for y in range(7):
            final_string += "⬛" * 4
            if time_info[0] > 9:
                for x in self.numbers[1][y]:
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
            final_string += "⬛⬛⬛"

            if current_time:
                indicator = "AM" if time_info[3] else "PM"

                for x in self.indicators[indicator][y]:
                    final_string += "⬜" if x else "⬛"
                final_string += "⬛"

            final_string += "\n"

        return final_string
