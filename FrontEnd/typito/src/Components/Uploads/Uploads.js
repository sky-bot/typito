import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button } from 'react-bootstrap';


class Uploads extends Component {
    
    state = {'status': ""}

    onChangeHandler(e)
    {
        e.preventDefault();
        const data = new FormData();
        let files = e.target.files;
        
        data.append('myfile', files[0])
        console.log("data====>", data)
        
        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: data,
        }).then(responce => responce.json())
        .then(json => {
            console.log("New Implementation")
            this.setState({"status": json.status})
            setTimeout(function(){
                this.setState({"status": ""});
           }.bind(this),5000);

        })
    }

    render() {
        return (
            <div>
                <div onSubmit={this.onFormSubmit} >
                    <input type="file" name="file" onChange={(e)=>this.onChangeHandler(e)} />    
                </div>  
                <h4 className="Status">{this.state.status}</h4>
            </div>
        );
    }
}

export default Uploads;