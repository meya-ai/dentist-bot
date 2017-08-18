# -*- coding: utf-8 -*-
from meya import Component


class RegisterEmail(Component):

    def start(self):
        email = self.db.user.get("email")

        if not self.db.table("customers").filter(email=email):
            self.db.table("customers").add({
                "email": email,
                "name": self.db.user.get("name"),
                "phone": self.db.user.get("phone")
            })
                    

        return self.respond(action="next")
