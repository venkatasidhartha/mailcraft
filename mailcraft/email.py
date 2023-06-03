import frappe
from mailcraft.email_utility.utility import mailCraft_settings
import requests

class Email:
    def __init__(self):
        self.settings = mailCraft_settings()

    def render_parent_template(self,body_content):
        return frappe.render_template(self.settings.parent_template,{"content":body_content})
    
    def render_mailcontent(self,template_name,params):
        template = frappe.get_doc("MailCraft Template",template_name)
        return frappe.render_template(template.message,params)
    
    def send_mail(self,template_name,params):
        if self.settings.switch:
            mail_content = self.render_mailcontent(template_name,params)
            final_template = self.render_parent_template(mail_content)
            print("*"*100)
            print(final_template)
            print("*"*100)



