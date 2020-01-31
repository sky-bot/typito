import React, { Component } from 'react';

import './App.css';
import UpLoads from './Components/Uploads/Uploads'

class App extends Component {

  uploadFileHandler = (event) => {
    event.preventDefault();
    console.log('Hello')
    console.log(event.target.files, "$$$$$");
    // console.log(event.target.files[0], "$$$$")

  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <h1> SkyLinsta </h1>
        </header>
        <UpLoads 
          uploadHandler={this.uploadFileHandler}
        />
      </div>
    );
  }
  
}

export default App;
