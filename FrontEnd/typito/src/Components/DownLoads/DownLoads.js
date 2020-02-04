import React, { Component } from 'react';
import fetch from 'isomorphic-fetch';
import './DownLoads.css';
import Jumbotron from 'react-bootstrap/Jumbotron'

class DownLoads extends Component {

    state = { 
        urls: [],
        perPage: 4,
        page: 1,
        totalPage: null,
        scrolling: false,
        url_obj: []
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
        const lastList = document.querySelector('ul.urls > div:last-child')
        const lastListOffset = lastList.offsetTop + lastList.clientHeight
        const pageOffset = window.pageYOffset + window.innerHeight
        
        let bottomOffset = 20

        if (pageOffset > lastListOffset - bottomOffset) this.loadMore()
    }

    loadUrls = () => {
        const { perPage, page, urls, url_obj} = this.state
        const url = `http://127.0.0.1:5000/?perPage=${perPage}&page=${page}`
        fetch(url)
        .then(responce => responce.json())
        .then(json => {
            console.log(json)
            const image_urls = json.result 
            const temp_urls = []
            for(let i=0;i<image_urls.length;i++)
            {
                let temp_obj = image_urls[i]
                temp_urls.push(temp_obj.url)
            }
            this.setState({
            urls: [...urls ,...temp_urls],
            url_obj: [...url_obj, ...image_urls],
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
    const url_obj = this.state.url_obj

    

    for (let i=0; i<url_obj.length;i++){    
        pics.push(<div className="imagerow"><img src={url_obj[i].url} alt="pic" className="UploadedPic"/><h4 className="tags"><b><i>Tags:</i></b>{url_obj[i].tags.join(",")}</h4></div>)
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