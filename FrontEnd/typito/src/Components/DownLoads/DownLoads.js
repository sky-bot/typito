import React, { Component } from 'react';
import fetch from 'isomorphic-fetch';
import './DownLoads.css';
import Jumbotron from 'react-bootstrap/Jumbotron'

class DownLoads extends Component {

    state = { 
        urls: [],
        perPage: 12,
        page: 1,
        totalPage: null,
        scrolling: false
    }


    componentDidMount(){
       this.loadUrls()
       this.scrollListener = window.addEventListener('scroll', (e) => {
           this.handleScroll(e)
       })
    }

    handleScroll = (e) => {
        const { scrolling, totalPage, page } =  this.state
        if (scrolling) return
        if (totalPage <= page) return
        const lastList = document.querySelector('ul.urls > img:last-child')
        const lastListOffset = lastList.offsetTop + lastList.clientHeight
        const pageOffset = window.pageYOffset + window.innerHeight
        
        let bottomOffset = 20

        if (pageOffset > lastListOffset - bottomOffset) this.loadMore()
    }

    loadUrls = () => {
        const { perPage, page, urls} = this.state
        const url = `http://127.0.0.1:5000/?perPage=${perPage}&page=${page}`
        fetch(url)
        .then(responce => responce.json())
        .then(json => {
            console.log(json)
            this.setState({
            urls: [...urls ,...json.result],
            scrolling : false,
            totalPage: json.count,
        })
    })
}

    loadMore = () => {
        this.setState(prevState => ({
            page: prevState.page + 1,  
            scrolling: true
        }), this.loadUrls);
    }


    render() {
    const pics = []
    const urls = this.state.urls
    

    for (let i=0; i<urls.length;i++){
        
        pics.push(<img src={urls[i]} alt="pic" className="UploadedPic"/>)
    }
        return (
            <div>
                <Jumbotron className="Jumbo">
                <ul className="urls">
                    {pics}
                </ul>
                </Jumbotron>
               
              
            </div>
        );
    }
}

export default DownLoads;