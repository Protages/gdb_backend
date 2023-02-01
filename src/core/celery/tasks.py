import httpx

from pydantic import EmailStr
from jinja2 import Environment, select_autoescape, PackageLoader

from src.core.config import settings
from src.core.celery.celery import celery


env = Environment(
    loader=PackageLoader('src', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


@celery.task
def send_email_confirm_notification(to_email: EmailStr, username: str, url: str):
    template = env.get_template('verification.html')
    html = template.render(
        url=url,
        first_name=username,
        subject="Confirm your email"
    )

    headers = {
        'accept': 'application/json',
        'api-key': settings.EMAIL_API_KEY,
        'content-type': 'application/json'
    }
    data = {  
        "sender": {  
            "name": settings.EMAIL_NAME,
            "email": settings.EMAIL_FROM
        },
        "to": [  
            {  
                "email": to_email,
                "name": username
            }
        ],
        "subject": "Confirm your email",
        "htmlContent": html
    }

    response = httpx.post(settings.EMAIL_URL, headers=headers, json=data)

    return response.text
