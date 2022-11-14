# send report by email
from decouple import config

import os
import base64

import sendgrid
from sendgrid.helpers.mail import *

from zipReport import create_zip

SENDGRID_ID = config("SENDGRID_KEY", cast=str)


def send_report(HTMLcontent,
                reportName,
                email="aleksendric@gmail.com",
                subject="Statistica"):

    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_ID)
    from_email = Email("report@freethrow.rs")
    to_email = To(email)

    content = Content(
        "text/plain",
        "this is dynamic text, potentially coming from our database")

    mail = Mail(from_email,
                to_email,
                subject,
                content,
                html_content=HTMLcontent)

    create_zip()

    with open(reportName, "rb") as f:
        data = f.read()
        f.close()
    encoded_file = base64.b64encode(data).decode()

    attachedFile = Attachment(
        FileContent(encoded_file),
        FileName(reportName),
        FileType("application/zip"),
        Disposition("attachment"),
    )
    mail.attachment = attachedFile

    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response)
        print("Sending email")
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        print(e)
        print("Could not send email")
