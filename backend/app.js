const exp = require('express')
const mongoose = require('mongoose')
const codemodel=require('./schema/code')
const cors=require('cors')

app=exp()
app.use(cors())
app.use(exp.json());

mongoose.connect('mongodb://localhost/DevAgent')
.then(()=>console.log('DB connected sucessfully'))
.catch((error)=>console.log(error))

app.post('/chat',async(req,res)=>{
    try{
        const {code}= req.body
        const saved_cont=await codemodel.create({code:code})
        const id=saved_cont._id.toString()
        try{
            const response_1=await fetch('http://127.0.0.1:8000/question',{
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({id:id})
            })
            console.log(id)
            console.log('successfully send to fastapi')
            const ans=await response_1.json()
            res.status(201).json({status:ans.status,approval_request:ans.approval_request,code:`'''${ans.code}'''`});
        }catch(error){
            console.log(error)
        }
    }catch(error){
        console.error(error)
        res.status(500).json({ error: 'Internal Server Error' });
    }
}
)

app.post('/resume',async(req,res)=>{
    try{
        const {is_approved}=req.body
        try{
            const response=await fetch('http://127.0.0.1:8000/resume',{
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({approve:is_approved})
            })
            const ans=await response.json()
            res.status(200).json({code:ans})
        }catch(error){
            console.log(error)
        }
    }catch(error){
        console.log(error)}
    })

app.listen(3000,'0.0.0.0',()=>{
    console.log('server is running')
})