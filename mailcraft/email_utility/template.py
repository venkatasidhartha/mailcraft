import frappe
from mailcraft.email_utility.utility import mailCraft_settings
import ast

class EmailTemplate:
    def __init__(self):
        self.settings = mailCraft_settings()
        self.subject = None

    def __set_subject(self,subject):
        self.subject = subject

    def __render_parent_template(self,body_content):
        return frappe.render_template(self.settings.parent_template,{"content":body_content})
    
    def __mailcraftTemplate(self,template_name):
        return frappe.get_doc("MailCraft Template",template_name)

    def __render_mailcontent(self,content,params):
        return frappe.render_template(content,params)
    
    def __render_button(self,button_link):
        return frappe.render_template(self.settings.button_template,{"link":button_link})
    
    def __template_mapping(self):
        data = self.settings.template_mapping
        return ast.literal_eval(data)

    def get_template_docname(self,key):
        data = self.__template_mapping()
        return data[key]

    def get_template(self,template_name,params):
        doc = self.__mailcraftTemplate(template_name)

        # if "button_link" in params:
        #     params["button"] = self.__render_button(button_link=params["button_link"])

        self.__set_subject(doc.subject)
        mail_content = self.__render_mailcontent(doc.message,params)
        final_template = self.__render_parent_template(mail_content)
        return final_template

    def get_subject(self):
        return self.subject


