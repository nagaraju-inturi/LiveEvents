from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
import os

def eventSchedule(cityName, eventName, dateVal):
    load_dotenv()

    # print("Hello LangChain")    

    summary_template = """
    given the travel destination city {cityName} about a person who is attending live event {eventName} at date {dateVal}:
    1. Plan this person's 5 day trip to this city.
    2. Show schedule as a bullet point list
    """
    input_variables = ["cityName", "eventName", "dateVal"]
    summary_prompt_template = PromptTemplate(
        input_variables=input_variables, template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    chain = summary_prompt_template | llm
    res = chain.invoke(input={"cityName": cityName, "eventName": eventName, "dateVal": dateVal})

    res = res.content
    res = res.split('\n\n')
    # print (res)
    return res
