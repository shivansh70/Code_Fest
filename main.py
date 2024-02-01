from langchain_openai import OpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import os
os.environ["OPENAI_API_KEY"] = "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"
filePath = "employee_data.csv"
llm = OpenAI(temperature=0, openai_api_key='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')
agent=create_csv_agent(llm,filePath,verbose=True)
agent.run("what is the name of EMPID 4001")
