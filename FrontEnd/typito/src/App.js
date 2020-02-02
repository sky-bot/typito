import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
// import { Button } from 'react-bootstrap';
// {/* <link href="https://fonts.googleapis.com/css?family=Pacifico&display=swap" rel="stylesheet"></link>  */}
import './App.css';
import UpLoads from './Components/Uploads/Uploads'
import DownLoads from './Components/DownLoads/DownLoads'

class App extends Component {

  state = {'urls': ""}

  uploadStatusHandler(event){
      this.setState({'upload_status': event.target.value})
  }

  // componentDidMount(){
  //   console.log("Inside APp")
  //   fetch('http://127.0.0.1:5000/', {
  //       method: 'GET'
  //   }).then((response) => {
  //       console.log(response)
  //       this.setState({urls: response})
  //   });
  //   console.log(this.state.urls)
  // }

  componentDidMount() {
    fetch('http://127.0.0.1:5000/')
    .then(res => res.json())
    .then((data) => {
      console.log(data.result)
      this.setState({ urls: data.result })
    })
    // .catch(console.log)
  }

  render() {

    const pics = []
    const urls = this.state.urls
    for (let i=0; i<urls.length;i++){
      console.log(urls[i])
      pics.push(<img src={urls[i]} alt="pic" className="UploadedPic"/>)
    }


    return (
      <div className="App">
        <header className="App-header">
          <h1> SkyLinsta </h1>
        </header>
        <UpLoads 
          uploadHandler={this.uploadFileHandler}
          upload_status={this.uploadStatusHandler}
        />
        <DownLoads/>

      { pics }
      </div>
    );
  }
  
}

export default App;
