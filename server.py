from fastapi import FastAPI, Request
from sqlalchemy import create_engine
from sqlalchemy import text
from requests import post

from pprint import pprint

from pydantic import BaseModel
class Message(BaseModel):
        id: int = None
        sender: str
        body: str

app = FastAPI()
engine = create_engine("postgresql://postgres:55555555@127.0.0.1/chatapp", echo=True)

@app.get("/")
async def root():
    return {"It": "Works!"}

@app.post("/masry/", status_code=200)
async def masry(request: Request):
    body = b""
    async for chunk in request.stream():
        body += chunk
    print(body)
    return {"status": "printed on Ahmad screen"}

@app.post("/messages/", status_code=201)
async def create_message(message: Message):
    # Broadcast message to all connected clients
    endpoint = 'https://9dea-156-192-146-105.ngrok-free.app/message/notify'
    res = post(endpoint, json={"sender": message.sender, "body": message.body})
    # print(res.text)

    # Save message to database
    with engine.begin() as con:
        con.execute(text('INSERT INTO messages (sender, body) VALUES (:sender, :body);'), {"sender": message.sender, "body": message.body})
    return {"status": "created"}

@app.get("/messages/", status_code=200)
async def get_messages():
    messages = []
    with engine.connect() as con:
        rs = con.execute(text('SELECT * FROM messages;'))
        for row in rs:
            message = Message(sender=row[1], body=row[2], id=row[0])
            messages.append(message)
    return {"messages": messages}