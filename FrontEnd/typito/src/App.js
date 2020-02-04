import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Jumbotron from 'react-bootstrap/Jumbotron'
import './App.css';
import UpLoads from './Components/Uploads/Uploads'
import DownLoads from './Components/DownLoads/DownLoads'
// import { LazyLoadComponent } from 'react-lazy-load-image-component';

class App extends Component {

  state = {
    "allurls": []
}

  uploadStatusHandler(event){
      this.setState({'upload_status': event.target.value})
  }

  render() {

    const pics = []
    const urls = this.state.allurls
    
    for (let i=0; i<urls.length;i++){
      
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

      {/* <Jumbotron fluid className="Jumbo">{ pics }</Jumbotron> */}

      </div>
    );
  }
 
}

export default App;
