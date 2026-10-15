import Editor from '@monaco-editor/react';
import './App.css'
import { useState } from 'react';

function App(){
  const [code,setcode]=useState('')
  const [interrupt,setinterrupt]=useState('')
  const [res,setres]=useState('')
  function handlechange(e){
    setcode(e)
  }

  const handlebtn= async(e)=>{
    if (e)  e.preventDefault();
    try{
      console.log("1. Sending request...");
      const response=await fetch('http://localhost:3000/chat',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({code:code})
      })
      console.log("2. Response received:", response);
      const data = await response.json();
      setres(data.code);
      setinterrupt(data.approval_request);
    }
    catch(error){
      console.error(error);
    }
  }

  const handle_interrupt=async(res_val)=>{
    try{
      const val=res_val
      console.log('sending response...')
      const response=await fetch('http://localhost:3000/resume',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({is_approved:val})
      })
      const data=await response.json()
      const final_code=data.code.code.slice(3,-3)
      const result = final_code.split('\n').slice(1).join('\n');
      console.log(result)
      setres(result);
      setinterrupt('');
    }
    catch(error){
      console.error(error)
    }
  }
  return(
    <>
      <p className='head'>DevAgent</p>
      <p style={{fontSize:'small',fontWeight:'lighter'}}>A multi-agent system analyzes code for security vulnerabilities, generates fixes, runs tests, and asks the user for approval before submitting PRs</p>
      <div className='main_field'>
        <div>
          <p style={{color:'aliceblue', fontWeight:'lighter' , textShadow: `0 0 5px white`,}}>Your Code</p>
          <Editor 
          defaultLanguage="python" 
          defaultValue="// enter your code here"  
          theme='vs-dark'
          className='editor'
          onChange={handlechange}
          />
          {!interrupt&&
          <div style={{display:'flex',justifyContent:'center',alignItems:'center',marginTop:'-20px'}}>
            <button className='sub-btn' onClick={handlebtn}>Check</button>
          </div>}
        </div>
        <div>
          <p style={{color:'aliceblue', fontWeight:'lighter', textShadow: '0 0 5px white'}}>AI response</p>
          <Editor 
          defaultLanguage="javascript"
          defaultValue='Waiting...'
          theme='vs-dark'
          className='editor'
          value={res}  
          options={{
          readOnly: true,
          }}
          />
          {interrupt && <div style={{display:'flex',justifyContent:'center',alignItems:'center',marginTop:'-20px'}}>
          <p style={{color:'white'}}>{interrupt}</p>
          <button className='approve-btn true-btn' onClick={()=>handle_interrupt('true')}>agree</button>
          <button className='approve-btn false-btn' onClick={()=>handle_interrupt('false')}>Dissagree</button>
          </div>
          }
        </div>
      </div>
    </>
  )
}

export default App