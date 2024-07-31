import asyncio
from fastapi import FastAPI, Form, status
from fastapi.responses import FileResponse, RedirectResponse
from twilio.rest import Client
import config

app = FastAPI()
settings = config.Settings()


@app.get('/')
async def index():
    return FileResponse('index.html')

@app.post('/')
async def handle_form(phone: str = Form(...), action: str = Form(...)):
    if action == 'sms':
        await asyncio.get_event_loop().run_in_executor(
            None, send_sms, phone, 'ElderSafe')
    elif action == 'call':
        await asyncio.get_event_loop().run_in_executor(
            None, make_call, phone, 'ElderSafe')
    return RedirectResponse('/success', status_code=status.HTTP_303_SEE_OTHER)


@app.get('/success')
async def success():
    return FileResponse('success.html')


def send_sms(to_number, body):
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    return client.messages.create(from_=settings.twilio_phone_number,
                                  to=to_number, body=body)

def make_call(to_number, body):
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    return client.calls.create(
        from_=settings.twilio_phone_number,
        to=to_number,
        twiml=f'<Response><Say>{body}</Say></Response>'
    )