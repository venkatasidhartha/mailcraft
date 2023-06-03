import frappe
import requests
import json
import ast
from mailcraft.email_utility.utility import mailCraft_settings
from mailcraft.email_utility.template import EmailTemplate

class _MailCraft_service:
    def __init__(self) -> None:
        self.settings = mailCraft_settings()

    def send_mail(self,to_user:list,params:dict,template_key:str):
        """
        to_user = [
            {
                "email": "no-reply@karkhana.io",
                "name": "no-reply"
            }
        ]
        params = {
            "FIRSTNAME":"no-reply"
        }

        template_key = "reset_password"
        """
        if self.settings.switch:
            et = EmailTemplate()
            template_docname = et.get_template_docname(key=template_key)
            final_template = et.get_template(template_name=template_docname,params=params)

            url = self.settings.service_url
            payload = {
                "sender": {
                    "email": self.settings.sender_email_address,
                    "name": self.settings.sender_name
                },
                "to": to_user,
                "htmlContent": final_template,
                "subject":et.get_subject()
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "api-key": self.settings.get_password('api_key')
            }
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code != 201:
                frappe.log_error(title='Mail Request Failed',message=response.text)



def send_mail(to_user:list,params:dict,template_key:str):
    """
        to_user = [
            {
                "email": "no-reply@karkhana.io",
                "name": "no-reply"
            }
        ]
        params = {
            "FIRSTNAME":"no-reply"
        }

        template_key = "reset_password"
        """
    mail_class = _MailCraft_service()
    mail_class.send_mail(to_user,params,template_key)