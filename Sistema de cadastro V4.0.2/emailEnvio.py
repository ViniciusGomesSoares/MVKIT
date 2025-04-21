import os
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def enviar_codigo_autenticacao(destinatario_email): # <- vc coloca o email que vai receber time!!
    codigo = ''.join([str(random.randint(0, 9)) for _ in range(6)])

    email_gmail = os.getenv('GMAIL_USER')
    senha_gmail = os.getenv('GMAIL_PASS')

    if not email_gmail or not senha_gmail:
        print("Credenciais de e-mail não encontradas nas variáveis de ambiente.")
        return None

    # Criar e configurar o e-mail
    mensagem = EmailMessage()
    mensagem['Subject'] = 'Seu código de autenticação'
    mensagem['From'] = email_gmail
    mensagem['To'] = destinatario_email
    mensagem.set_content(f'Seu código de autenticação é: {codigo}')

    try:
        # Enviar via SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_gmail, senha_gmail)
            smtp.send_message(mensagem)
        print('Código enviado com sucesso!')
        return codigo
    except Exception as e:
        print(f'Erro ao enviar e-mail: {e}')
        return None
    
destinatario_email = ""
enviar_codigo_autenticacao(destinatario_email)