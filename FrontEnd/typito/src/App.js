import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Jumbotron from 'react-bootstrap/Jumbotron'
import './App.css';
import UpLoads from './Components/Uploads/Uploads'
import DownLoads from './Components/DownLoads/DownLoads'
import Search from './Components/Search/Search'

class App extends Component {

  state = {
    "allurls": [],
    "uploading": false,
    "startDate": null,
    "endDate": null
  }

  render() {

    const pics = []
    const urls = this.state.allurls

    for (let i = 0; i < urls.length; i++) {
      pics.push(<img src={urls[i]} alt="pic" className="UploadedPic" />)
    }


    return (
      <div className="App">
        <header className="App-header">
          <h1> SkyLinsta </h1>
        </header>
        <UpLoads/>
        {/* <Jumbotron className="Jumbo_Search"><Search /></Jumbotron> */}

        <DownLoads />
        {/* <Jumbotron fluid className="Jumbo">{ pics }</Jumbotron> */}

      </div>
    );
  }

}

export default App;
