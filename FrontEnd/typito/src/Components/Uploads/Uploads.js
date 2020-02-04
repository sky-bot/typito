import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Button } from 'react-bootstrap';
class Uploads extends Component {
    


    onChangeHandler(e)
    {
        e.preventDefault();
        const data = new FormData();
        let files = e.target.files;
        data.append('myfile', files[0])
        
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
                    <Button variant="success" className="mr-2" onClick={this.handleLogin}>Submit</Button>
                </div>  
            </div>
        );
    }
}

export default Uploads;