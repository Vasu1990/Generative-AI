from dotenv import load_dotenv
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
from agents import Agent, trace, Runner, gen_trace_id, function_tool
from typing import Optional

load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

@function_tool
def record_user_details(email: str, name: Optional[str] = None, notes: Optional[str] = None) -> dict:
    """Record user details when they provide an email for follow-up contact.

    Args:
        email (str): The user's email address for follow-up.
        name (str, optional): The user's name. Defaults to None.
        notes (str, optional): Additional notes about the user. Defaults to None.
    """
    name = name or "Name not provided"
    notes = notes or "not provided"
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

@function_tool
def record_unknown_question(question: str) -> dict:
    """Record any question that could not be answered.

    Args:
        question (str): The question that could not be answered.
    """
    push(f"Recording unknown question: {question}")
    return {"recorded": "ok"}

tools = [record_user_details, record_unknown_question]
print(tools)


class Me:

    def __init__(self):
        self.name = "Vasu Nagpal"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        
        self.agent = Agent(name="ResumeBot", instructions=self.system_prompt(), model="gpt-4o-mini",tools=tools)
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt

    async def chat(self, message, history):
         # Feed the user message into the runner
        result = await Runner.run(self.agent,message)
        print(result.final_output)
        return result.final_output
    

if __name__ == "__main__":
    me = Me()
    demo = gr.ChatInterface(me.chat, type="messages")
    demo.launch()
    