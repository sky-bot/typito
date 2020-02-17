import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Uploads.css'
import * as Constant from './../../Constants/Constants'



class Uploads extends Component {

    

    constructor(props) {
        super(props)
        this.state = {
            'status': "",
            'file':null,
            'desc': " ",
            'refresh': true
        }
        this.formHandler = this.formHandler.bind(this)
      }



    onChangeHandler(e) {
        e.preventDefault();
        let files = e.target.files;
        this.setState({'file': files})
        
        console.log(files)
    }

    formHandler() {

        console.log(Constant.URL)
        let file = this.state.file;
        let desc = this.state.desc;
        console.log(file.length)
        for(let i=0;i<file.length;i++){
            const data = new FormData();
            data.append('myfile', file[i])
            console.log(file[i])
            data.append('desc', desc)
            fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: data,
            }).then(responce => responce.json())
                .then(json => {
                    this.setState({ "status": json.status })
                    setTimeout(function () {
                        this.setState({"status": ""});
                        let refresh_val = this.state.refresh
        
                        this.setState({'refresh': !refresh_val})
                        this.props.refresh(this.state.refresh)
                    }.bind(this), 5000);
                })
            console.log("It seems working")
            this.setState({'desc': "", 'file': null})
        }
        this.fileInput.value = "";
        
    }
       
    descChangeHandler(e) {
        e.preventDefault()
        this.setState({'desc':e.target.value})

    }


    render() {
        return (
            <div>
                <div>
                    <label><b>UpLoad Pic:  </b></label>
                    <input className="uploadInput" type="file" multiple name="file"  onChange={(e) => this.onChangeHandler(e)} ref={ref=> this.fileInput = ref} />
                    <label><b>Desc: </b></label>
                    <input className="uploadInput" type="text" name="desc" value={this.state.desc}  onChange={(e)=> this.descChangeHandler(e)}></input>
                    <button type="submit" onClick={this.formHandler.bind(this)}>Submit</button>
                </div>
                <h4 className="Status">{this.state.status}</h4>
            </div>
        );
    }
}

export default Uploads;