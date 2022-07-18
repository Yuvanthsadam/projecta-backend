from django.core.mail import EmailMessage



def send_email(data):
    try:
        email = EmailMessage(
                subject = data['email_subject'],
                body = data['email_body'],
                to = [data['to_email']],
                # from_email=[data['from_email']]
        )
        res = email.send()
        return {"status" : "success"}
    except Exception as e :
        return {"status" : "error",
                "message" : e
            }