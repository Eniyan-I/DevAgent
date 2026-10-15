from langchain_core.messages import SystemMessage,AIMessage,HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessagesState,StateGraph,END
from typing import Literal
from langgraph.types import interrupt,Command
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class Codestate(MessagesState):
  next_agent:str
  context:str
  is_approved:bool
  retries:int

llm=ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite',
                           api_key=GOOGLE_API_KEY )

def analyzer(State:Codestate):
  message=State['messages']
  sys_msg=SystemMessage(content='Act as an AI Code Auditor & PR Assistant and chech the code for security rules/OWASP vulnerabilities and respond only with True if the code needs to rewritten or False')
  res=llm.invoke([sys_msg]+message)
  content = res.content
  if isinstance(content, str):
        content = content.strip().lower()
  if content=='false':
    return {
        'messages':[AIMessage(content='Your code does not contain any risks')],
        'next_agent':'end'
    }
  else:
    sys_msg=SystemMessage(content='Generate vulnerabilities that are present in the code.Do not generate the code')
    res=llm.invoke([sys_msg]+message)
    content = res.content
    return {
        'context':content,
        'next_agent':'human_approval'
    }

def human_approval(State:Codestate):
  decision=interrupt({
    'question':'Do you want to generate code?',
    'code':State['context']
  })
  return{
    'is_approved':decision,
    'next_agent':'rewritter' if decision else 'end'
  }

def rewritter(State:Codestate):
  message=State['messages']
  sys_msg=SystemMessage(content='Act as an senior code writer and rewriter the following code such that it satsify security rules/OWASP vulnerabilities.Generte only the code')
  if message and isinstance(message[-1], AIMessage):
      message.append(HumanMessage(content=message[-1].content))
  res=llm.invoke([sys_msg]+message)
  return {
      'messages':[AIMessage(content=res.content)],
      'next_agent':'tester'
  }

def tester(State: Codestate):
    message = State['messages']
    no_retries = State.get('retries', 0)
    
    if no_retries < 3:
        sys_msg = SystemMessage(content='Act as a code tester. Test the following code with security rules/OWASP vulnerabilities and respond only with true if it passes test or else return false.')
        if message and isinstance(message[-1], AIMessage):
            message.append(HumanMessage(content=message[-1].content))
        res = llm.invoke([sys_msg] + message)
        content = res.content
        if isinstance(content, str):
              content = content.strip().lower()
        if content == 'true':
            return {
                'messages': [AIMessage(content='hello')],
                'next_agent': 'end',
                'is_approved': True
            }
        else:
            return {
                'messages': message,
                'retries': no_retries + 1,
                'next_agent': 'rewritter',
                'is_approved': False
            }
    else:
        return {
            'messages': [AIMessage(content='Maximum number of retries reached. Manual rewrite required.')],
            'next_agent': 'end',
            'is_approved': False
        }

def router(State:Codestate) -> Literal['rewritter','tester','end']:
  return State['next_agent']

builder=StateGraph(Codestate)
memory=InMemorySaver()
builder.add_node('analyzer',analyzer)
builder.add_node('rewritter',rewritter)
builder.add_node('human_approval',human_approval)
builder.add_node('tester',tester)

builder.set_entry_point('analyzer')
builder.add_conditional_edges(
    'analyzer',
    router,
     {
        'human_approval':'human_approval',
        'end':END,
    }
)
builder.add_conditional_edges(
  'human_approval',
  router,{
    'rewritter':'rewritter',
    'end':END,
  }
)
builder.add_edge('rewritter','tester')
builder.add_edge('tester',END)

graph=builder.compile(checkpointer=memory)
config={'configurable':{'thread_id':'thread_1'}}

def invoker(msg):
  result=graph.invoke({"messages": [HumanMessage(content=f'"""{msg}"""')]},config=config)
  return result

def resumer(is_approved):
  return graph.invoke(Command(resume=is_approved),config=config)