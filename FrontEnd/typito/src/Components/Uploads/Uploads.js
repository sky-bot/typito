import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Uploads.css'



class Uploads extends Component {

    

    constructor(props) {
        super(props)
        this.state = {
            'status': "",
            'file':null,
            'desc': " ",
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
        
        const data = new FormData();
        let file = this.state.file;
        let desc = this.state.desc;
        console.log(file.length)
        for(let i=0;i<file.length;i++){
            data.append('myfile', file[0])
            console.log(file[0])
            data.append('desc', desc)
    
            fetch('http://127.0.0.1:5000/upload', {
                method: 'POST',
                body: data,
                // headers:{'Content-Type': 'multipart/form-data', 'enctype':'multipart/form-data'}
            }).then(responce => responce.json())
                .then(json => {
                    this.setState({ "status": json.status })
                    setTimeout(function () {
                        this.setState({"status": ""});
                    }.bind(this), 2000);
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
                    <button type="submit" onClick={this.formHandler}>Submit</button>
                </div>
                <h4 className="Status">{this.state.status}</h4>
            </div>
        );
    }
}

export default Uploads;