from fastapi import FastAPI,HTTPException
from graph import invoker,resumer
from pydantic import BaseModel
import uvicorn
from pymongo import MongoClient
from bson import ObjectId

app=FastAPI(title="AI Code Auditor API", version="1.0")

client=MongoClient('mongodb://localhost:27017')
db=client['DevAgent']
collections=db['codes']

class inp_model(BaseModel):
  id:str

class approval_req(BaseModel):
    approve:bool

def is_interrupt(result):
    if '__interrupt__' in result:
        interrupts = result["__interrupt__"]
        return interrupts[-1].value
    return None

@app.post('/question')
def receive(model:inp_model):
    document = collections.find_one({
    "_id": ObjectId(model.id)
    })
    if document is None:
        return {"msg": "Document not found", "id": model.id}
    try:
        result=invoker(document['code'])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to execute the code audit workflow"
            )
    interrupt_data=is_interrupt(result)
    return {
        "status": 'waiting for approval',
        "approval_request": interrupt_data['question'],
        'code':interrupt_data['code'][-1]['text']
    }

@app.post('/resume')
def approve_execution(model: approval_req):
    try:
        approve = model.approve
        result = resumer(approve)
        last_msg = result['messages'][-1].content[-1]
        if isinstance(last_msg,dict):
            code=last_msg.get('text','')
        elif isinstance(last_msg,str):
            code=last_msg
        else:
            code=str(last_msg)
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ERROR: {str(e)}"
        )
        
    return {
        "status": "success",
        "code": code
    }

if __name__=='__main__':
   uvicorn.run('main:app',host='127.0.0.1',port=8000,reload=True)