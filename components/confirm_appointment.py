# -*- coding: utf-8 -*-
from meya import Component
import arrow
import requests


def send_email(email, date_time, service, name, phone, api_key):
    business = "Allure Dental Center"
    first_name = name.split(" ")[:1][0]

    # message parts
    subject = "Appointment confirmed: {}".format(date_time.format("ddd M/D @ h:mma"))
    message = (
        "Hi {first_name}\n\n"
        "We've confirmed an appointment with {business}.\n\n"
        "Service: {service}\n"
        "Date: {date_time}\n"
        "Your phone: {phone}\n\n"
        "Thanks!"
    ).format(
        first_name=first_name,
        business=business,
        service=service,
        date_time=date_time.format("ddd M/D @ h:mma"),
        phone=phone
    )

    # send the email
    return requests.post(
        "https://api.mailgun.net/v3/locl.co/messages",
        auth=("api", api_key),
        data={"from": "{} <bots+alluredental@meya.ai>".format(business),
              "to": [email],
              "subject": subject,
              "text": message})


class ConfirmAppointment(Component):

    def start(self):
        # read data
        service = self.db.flow.get("service")
        date_time = arrow.Arrow.utcfromtimestamp(self.db.flow.get("date_time"))
        email = self.db.user.get("email")
        name = self.db.user.get("name")
        phone = self.db.user.get("phone")
        api_key = self.db.bot.settings.get("mailgun_api_key")

        # send email
        send_email(email, date_time, service, name, phone, api_key)

        # construct response
        text = (
            "You're booked for a {} appointment on {}!\n"
            "We've sent an email confirmation to {}.\n"
            "See you soon 😀"
        ).format(service, date_time.format("ddd M/D @ h:mma"), email)
        message = self.create_message(text=text)
        return self.respond(message=message, action="next")
