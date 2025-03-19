# Customer-Feedback-Agent
This Streamlit application classifies customer feedback as positive or negative using OpenAI's language model
## **Features**

- Classifies feedback sentiment (positive/negative) using AI

- Provides a clickable star rating system for positive feedback

- Sends an automated email for negative feedback

- Displays AI-generated responses to customer feedback

## **Installation**

## Prerequisites

- Python 3.8+

- Streamlit

- OpenAI API Key

- SMTP email credentials (for automated emails)
## **Install dependencies:**
```sh
pip install -r requirements.txt
```
## **Set environment variables:**
```sh
OPENAI_API_KEY="your_openai_api_key"
EMAIL_SENDER="your_email@gmail.com"
EMAIL_RECEIVER="support_email@gmail.com"
EMAIL_PASSWORD="your_email_password"
```
## **Run the application**
```sh
streamlit run app.py
```
## **Usage**

- Enter customer feedback in the text area.

- Click "Submit Feedback."

- If the feedback is positive, click on a star (⭐) to submit a rating.

- If the feedback is negative, an automated email is sent to customer support.
  
## **Dependencies**

- streamlit

- openai

- langchain

- pydantic

- smtplib

- email.mime

## **License**

This project is licensed under the MIT License.
