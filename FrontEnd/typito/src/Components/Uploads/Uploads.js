import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Uploads.css'



class Uploads extends Component {

    state = {
        'status': "",
        'endDate': null,
        'startDate': null
    }

    startDateChangeHandler(e) {
        e.preventDefault();
        this.setState({'startDate': e.target.value})
    }

    endDateChangeHandler(e) {
        e.preventDefault();
        this.setState({'endDate': e.target.value})
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

    render() {
        return (
            <div>
                <div>
                    <input className="uploadInput" type="file" name="file" onChange={(e) => this.onChangeHandler(e)} />
                </div>
                <h4 className="Status">{this.state.status}</h4>
                
            </div>
        );
    }
}

export default Uploads;