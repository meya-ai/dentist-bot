# -*- coding: utf-8 -*-
from meya import Component


class CheckEmail(Component):

    def start(self):
        email = self.db.flow.get("email")

        # find the customer
        customers = self.db.table("customers").filter(email=email)

        if customers:
            customer = customers[0]

            # we found the customer
            action = "success"
            self.db.user.set("email", email)
            self.db.user.set("name", customer.get("name"))
            self.db.user.set("phone", customer.get("phone"))

        else:
            # no customer found
            action = "fail"            

        return self.respond(action=action)
