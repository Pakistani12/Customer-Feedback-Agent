import streamlit as st
import smtplib
from email.mime.text import MIMEText
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain.schema.runnable import RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()

# Load OpenAI Model
model = ChatOpenAI()
parser = StrOutputParser()

# Define feedback sentiment classification schema
class Feedback(BaseModel):
    sentiment: Literal['positive', 'negative'] = Field(description='Classify feedback as positive or negative')

parser2 = PydanticOutputParser(pydantic_object=Feedback)

# Sentiment classification prompt
prompt1 = PromptTemplate(
    template='Classify the sentiment of the following feedback text into positive or negative \n {feedback} \n {format_instruction}',
    input_variables=['feedback'],
    partial_variables={'format_instruction': parser2.get_format_instructions()}
)

classifier_chain = prompt1 | model | parser2

# Response prompts
prompt2 = PromptTemplate(
    template='Write an appropriate response to this positive feedback \n {feedback}',
    input_variables=['feedback']
)

prompt3 = PromptTemplate(
    template='Write an appropriate response to this negative feedback \n {feedback}',
    input_variables=['feedback']
)

branch_chain = RunnableBranch(
    (lambda x: x.sentiment == 'positive', prompt2 | model | parser),
    (lambda x: x.sentiment == 'negative', prompt3 | model | parser),
    RunnableLambda(lambda x: "Could not find sentiment")
)

chain = classifier_chain | branch_chain

# Function to send email
def send_email(feedback_text):
    sender_email = os.getenv("EMAIL_SENDER")
    receiver_email = os.getenv("EMAIL_RECEIVER")
    password = os.getenv("EMAIL_PASSWORD")
    
    subject = "Urgent Customer Issue"
    body = f"Customer Feedback: {feedback_text}\n\nPlease reach out to resolve the issue."
    
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        st.success("Email sent to customer support.")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Streamlit App
st.title("Customer Feedback Agent")
feedback_text = st.text_area("Enter customer feedback:")

if st.button("Submit Feedback"):
    if feedback_text:
        result = classifier_chain.invoke({'feedback': feedback_text})
        sentiment = result.sentiment
        response = branch_chain.invoke(result)

        st.write("### AI Response:")
        st.write(response)

        if sentiment == 'positive':
            st.success("Thank you for your positive feedback! Please rate us.")
            
            if "selected_rating" not in st.session_state:
                st.session_state["selected_rating"] = 0
            
            def rate_us(stars):
                st.session_state["selected_rating"] = stars

            st.write("### Click a star to rate:")
            cols = st.columns(5)
            
            for i in range(5):
                if cols[i].button("⭐" * (i + 1), key=f"star_{i+1}"):
                    rate_us(i + 1)
                    st.experimental_rerun()
            
            if st.session_state["selected_rating"] > 0:
                st.success(f"Thank you for rating us {st.session_state['selected_rating']} stars!")
                if st.session_state["selected_rating"] == 5:
                    st.balloons()
        
        elif sentiment == 'negative':
            st.error("We're sorry for your experience. An email has been sent to customer support.")
            send_email(feedback_text)