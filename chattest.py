import gradio as gr
from typing import Any
from queue import Queue, Empty
from langchain.callbacks.base import BaseCallbackHandler
from langchain.prompts import PromptTemplate
from threading import Thread
import cohere

q = Queue()
job_done = object()
COHERE_KEY = 'Rn5t8Ya5avkjwVF8gAIG5grNZ99pSWJ4exHXb6ak'

co = cohere.Client(COHERE_KEY)

class QueueCallback(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to a queue."""

    def __init__(self, q):
        self.q = q

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.q.put(token)

    def on_llm_end(self, *args, **kwargs: Any) -> None:
        return self.q.empty()

callbacks = [QueueCallback(q)]
template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate(template=template, input_variables=["question"])

def cohere_generate(question):
    """Call Cohere's API to generate text based on the question."""
    response = co.generate(
        model='command-xlarge-nightly',  # You can also use 'command-xlarge'
        prompt=prompt.format(question=question),
        max_tokens=200,
        temperature=0.75,
        stop_sequences=["\n"]
    )
    return response.generations[0].text

def answer(question):
    def task():
        response = cohere_generate(question)
        for token in response:
            q.put(token)  # Send token to the queue one by one
        q.put(job_done)  # Mark when the job is done

    t = Thread(target=task)
    t.start()


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history):
        question = history[-1][0]
        print("Question: ", question)
        history[-1][1] = ""
        answer(question=question)
        while True:
            try:
                next_token = q.get(True, timeout=1)
                if next_token is job_done:
                    break
                history[-1][1] += next_token
                yield history
            except Empty:
                continue

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, chatbot, chatbot)
    clear.click(lambda: None, None, chatbot, queue=False)

demo.queue()
demo.launch()
