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
            'refresh': true
        }
        this.formHandler = this.formHandler.bind(this)
      }



    onChangeHandler(e) {
        e.preventDefault();
        let files = e.target.files;
        this.setState({'file': files})
    }

    formHandler() {

        let file = this.state.file;
        let desc = this.state.desc;

        if(file != null) {
            for(let i=0;i<file.length;i++){
                const data = new FormData();
                data.append('myfile', file[i])

                data.append('desc', desc)
                fetch('http://13.59.9.52:5001/upload', {
                    method: 'POST',
                    body: data,
                }).then(responce => responce.json())
                    .then(json => {
                        this.setState({ "status": json.status })
                        setTimeout(function () {
                            this.setState({"status": ""});
                            
                        }.bind(this), 5000);
                    })

                this.setState({'desc': "", 'file': null})
            }

            let refresh_val = this.state.refresh
            this.setState({'refresh': !refresh_val})
            this.props.refresh(this.state.refresh)
            this.fileInput.value = "";
        }
        
        
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