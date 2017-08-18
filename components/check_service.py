# -*- coding: utf-8 -*-
import arrow
from meya import Component


class CheckService(Component):

    def start(self):
        action = "notexists"

        # read the api.ai parameters
        parameters = self.db.flow.get("parameters") or {}
        service = parameters.get("service")

        if service:
            # set the date based on api.ai params
            self.db.flow.set("service", service)
            action = "exists"

        return self.respond(action=action)
