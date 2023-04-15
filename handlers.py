from logic import handle_get_current_trains
from constants import URL


def handle_command_options(message, mode):
    command = message.text.split()
    match len(command):
        case 0:  # ""
            answer = "Didn't get any commands"  # should not happen
            # bot.reply_to(message, "Didn't get any commands!")
        case 1:  # "/toWork"
            answer = handle_get_current_trains(URL, mode)
        case 2:  # "/toWork 5"
            answer = handle_get_current_trains(URL, mode, time=command[1])
        case 3:  # "/toWork 5 hours"
            answer = handle_get_current_trains(
                URL, mode, time=command[1], units=command[2]
            )
    return answer
