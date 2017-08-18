# -*- coding: utf-8 -*-
from meya import Component
import arrow
from meya.cards import TextWithButtons, Button

SLOTS = [
    "10:00",
    "13:30",
    "16:00"
]
SUCCESS = "success"
FAIL = "fail"


class FindTime(Component):

    def start(self):
        date = arrow.Arrow.utcfromtimestamp(self.db.flow.get("date"))

        # construct card
        text = "What time works best? (30 min.)"
        
        # build a bunch of time slots as buttons
        buttons = []
        for slot in SLOTS:
            # construct the datetime slot
            date_time = arrow.get("{} {}".format(
                date.format("YYYY-MM-DD"),
                slot
            ))
            time_str = date_time.format("ddd M/D @ h:mma")
            data = {"date_time": date_time.timestamp}

            # add the button
            buttons.append(Button(text=time_str, data=data, action=SUCCESS))

        # add a none button option
        buttons.append(Button(text="None of these", action=FAIL))

        # create the message
        card = TextWithButtons(text=text, buttons=buttons, mode="quick_reply")
        message = self.create_message(card=card)

        return self.respond(message=message)
