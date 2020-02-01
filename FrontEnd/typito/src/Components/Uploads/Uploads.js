import React, { Component } from 'react';
import axios, { post } from 'axios';

class Uploads extends Component {
    constructor(props) {
        super(props);
        this.state = {
            image: ""
        }
    };


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
        // let reader = new FileReader();
        // reader.readAsDataURL(files[0])
        
      
        // reader.onload=(e) => {
        //     console.log('Reaching Handler')
        //     console.log(e.target.result)

        // const url = "http://127.0.0.1:5000/upload"
        // // const formData={'myfile':e.target.result}
        // return post(url, formData).then(response => console.log(response));
        // }
    }


    render() {
        return (
            <div onSubmit={this.onFormSubmit}>
                <input type="file" name="file" onChange={(e)=>this.onChangeHandler(e)}/>
                <button type="button" onClick={this.handleLogin}>Submit</button>
            </div>
        );
    }
}

export default Uploads;