import os
import uvicorn
import dotenv
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from fastapi import FastAPI
from pydantic import BaseModel
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

app = FastAPI()

origins = [
    "https://victorhugomarques-portfolio.netlify.app/",
    "https://victorhugomarques-portfolio.netlify.app",
    "https://api-python-portfolio.herokuapp.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota Raiz
@app.get("/")
def raiz():
    return "Hello World"

# Criar model
class Contato(BaseModel):
    email: str
    assunto: str
    mensagem: str

# Rota Envio de E-mail
@app.post("/contato")
def envia_email(contato: Contato):
    print(contato)

    email_from = os.getenv("USER_EMAIL")
    email_password = os.getenv("USER_PASSWORD")
    email_smtp_server = 'smtp.gmail.com'

    destination = os.getenv("USER_DESTINATION")

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['Subject'] = contato.assunto

    text = contato.mensagem + "<br> Remetente: " + contato.email
    msg_text = MIMEText(text, 'html')
    msg.attach(msg_text)

    try: 
        smtp = smtplib.SMTP(email_smtp_server, 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(email_from, email_password)
        smtp.sendmail(email_from, (destination), msg.as_string())
        smtp.quit()
        print('Email enviado com sucesso!')
    except Exception as err:
        print(f'Falha ao enviar e-mail: {err}')
    
    return "Email enviado!"


if __name__ == "__main__":
    uvicorn.run(app, debug=True)