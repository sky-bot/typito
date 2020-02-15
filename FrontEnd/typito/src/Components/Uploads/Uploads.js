import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Uploads.css'



class Uploads extends Component {

    state = {
        'status': "",
        'file': null,
        'desc': ""
    }


    onChangeHandler(e) {
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
                this.setState({ "status": json.status })
                setTimeout(function () {
                    this.setState({"status": ""});
                }.bind(this), 5000);
            })
    }

    formHandler() {
        console.log("formHandler")
    }

    descChangeHandler(e) {
        e.preventDefault()
        console.log("inside desc Handler")
        console.log(e.target.value)
        this.setState({'desc':e.target.value})

    }

    render() {
        return (
            <div>
                <div>
                    <label><b>UpLoad Pic:  </b></label>
                    <input className="uploadInput" type="file" name="file" onChange={(e) => this.onChangeHandler(e)} />
                    <label><b>Desc: </b></label>
                    <input className="uploadInput" type="text" name="desc" onChange={(e)=> this.descChangeHandler(e)}></input>

                </div>
                <h4 className="Status">{this.state.status}</h4>
            </div>
        );
    }
}

export default Uploads;