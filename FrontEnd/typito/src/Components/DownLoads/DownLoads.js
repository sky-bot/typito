import React, { Component } from 'react';

class DownLoads extends Component {

    constructor(props) {
        super(props);
        this.state = {
            urls: []
        }
    };


    componentDidMount(){
        fetch('http://127.0.0.1:5000/', {
            method: 'GET'
        }).then((response) => {
            console.log(response)
            this.setState({urls: response})
        });
        console.log(this.state.urls)
    }

    render() {
        return (
            <div>
               <p>;(</p>
            </div>
        );
    }
}

export default DownLoads;