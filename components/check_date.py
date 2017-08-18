# -*- coding: utf-8 -*-
import arrow
from meya import Component


class CheckDate(Component):

    def start(self):
        action = "notexists"

        # read the api.ai parameters
        parameters = self.db.flow.get("parameters") or {}
        date_time = parameters.get("date-time")

        if date_time:
            # set the date based on api.ai params
            self.db.flow.set("date", arrow.get(date_time).timestamp)
            date_str = arrow.get(date_time).format("ddd. MMM. DD")
            self.db.flow.set("date_str", date_str)

            action = "exists"

        return self.respond(action=action)
