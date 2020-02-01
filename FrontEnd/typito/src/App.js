import React, { Component } from 'react';

import './App.css';
import UpLoads from './Components/Uploads/Uploads'
import DownLoads from './Components/DownLoads/DownLoads'

class App extends Component {

  state = {'upload_status': "p"}

  uploadStatusHandler(event){
      this.setState({'upload_status': event.target.value})
  }

  render() {
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

        <h3>{this.state.upload_status}</h3>
      </div>
    );
  }
  
}

export default App;
