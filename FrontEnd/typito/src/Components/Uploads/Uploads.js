import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button } from 'react-bootstrap';
class Uploads extends Component {
    


    onChangeHandler(e)
    {
        e.preventDefault();
        const data = new FormData();
        let files = e.target.files;
        // console.log(this.input.target)
        console.log("============================================================")
        data.append('myfile', files[0])
        console.log("data====>", data)
        
        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: data,
        })


    }


    render() {
        return (
            <div>
                <div onSubmit={this.onFormSubmit} >
                    <input type="file" name="file" onChange={(e)=>this.onChangeHandler(e)} />
                    
                </div>  
            </div>
        );
    }
}

export default Uploads;