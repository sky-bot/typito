import React, { Component } from 'react';

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
                    <button type="button" onClick={this.handleLogin}>Submit</button>
                </div>  
            </div>
        );
    }
}

export default Uploads;