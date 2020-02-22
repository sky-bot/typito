import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

import './App.css';
import UpLoads from './Components/Uploads/Uploads'
import DownLoads from './Components/DownLoads/DownLoads'


class App extends Component {

  state = {
    "allurls": [],
    "uploading": false,
    "startDate": null,
    "endDate": null,
    "refresh": true
  }

  refreshHandler() {
    let refresh_val = this.state.refresh
    this.setState({'refresh':!refresh_val});
    console.log("Can be submitted")
  }

  render() {

    const pics = []
    const urls = this.state.allurls

    for (let i = 0; i < urls.length; i++) {
      pics.push(<img src={urls[i]} alt="pic" className="UploadedPic" />)
    };

   


    return (
      <div className="App">
        <header className="App-header">
          <h1 className="heading"> SkyLinsta </h1>
        </header>
        <UpLoads refresh={this.refreshHandler.bind(this)}/>

        <DownLoads refresh={this.refreshHandler.bind(this)}/>

      </div>
    );
  }

}

export default App;
