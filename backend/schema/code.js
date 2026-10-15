const mongoose = require('mongoose')

const codeschema=new mongoose.Schema(
    {
        code:{
            type:String,
            require:true
        }
    }
)

module.exports = mongoose.model('codes',codeschema)