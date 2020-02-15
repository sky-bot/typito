import React, { Component } from 'react';
import fetch from 'isomorphic-fetch';
import './DownLoads.css';
import Jumbotron from 'react-bootstrap/Jumbotron'

class DownLoads extends Component {

    constructor(props) {
        super(props)
        this.state = {
            urls: [],
            perPage: 8,
            page: 1,
            totalPage: null,
            scrolling: false,
            url_obj: [],
            date: "",
            // to: "",
            tags: "",
        }
        this.formHandler = this.formHandler.bind(this)
      }


    componentDidMount() {
        this.loadUrls()
        this.scrollListener = window.addEventListener('scroll', (e) => {
            this.handleScroll(e)
        })
    }

    handleScroll = (e) => {
        const { scrolling, totalPage, page } = this.state
        if (scrolling) return
        if (totalPage <= page) return
        const lastList = document.querySelector('ul.urls > div:last-child')
        const lastListOffset = lastList.offsetTop + lastList.clientHeight
        const pageOffset = window.pageYOffset + window.innerHeight

        let bottomOffset = 20

        if (pageOffset > lastListOffset - bottomOffset) this.loadMore()
    }

    loadUrls = () => {
        const { perPage, page, urls, url_obj } = this.state
        const url = `http://127.0.0.1:5000/?perPage=${perPage}&page=${page}`
        fetch(url)
            .then(responce => responce.json())
            .then(json => {
                console.log(json)
                const image_urls = json.result
                const temp_urls = []
                for (let i = 0; i < image_urls.length; i++) {
                    let temp_obj = image_urls[i]
                    temp_urls.push(temp_obj.url)
                }
                this.setState({
                    urls: [...urls, ...temp_urls],
                    url_obj: [...url_obj, ...image_urls],
                    scrolling: false,
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

    startDateChangeHandler(e) {
        e.preventDefault();
        this.setState({'date': e.target.value})
        console.log(e.target.value)
    }

    endDateChangeHandler(e) {
        e.preventDefault();
        this.setState({'endDate': e.target.value})
    }

    tagHandler(e) {
        e.preventDefault();
        this.setState({tags: e.target.value})
    }

    formHandler() {
        console.log("formHandler")
        console.log(this.state)
        const { tags } = this.state

        const url = `http://127.0.0.1:5000/search?&search=${tags}`
        console.log(url)
        fetch(url)
            .then(responce => responce.json())
            .then(json => {
                console.log("Its working")
                const image_urls = json.result
                console.log(image_urls)
                const temp_urls = []
                for (let i = 0; i < image_urls.length; i++) {
                    let temp_obj = image_urls[i]
                    temp_urls.push(temp_obj.url)
                }
                this.setState({
                    urls: temp_urls,
                    url_obj: image_urls,
                    scrolling: false,
                    totalPage: json.count,
                })
            })
    }

    render() {
        const pics = []
        const url_obj = this.state.url_obj



        for (let i = 0; i < url_obj.length; i++) {
            pics.push(<div className="imagerow box">
                <h5 className="upload_date"><i>Uploaded On: </i>{url_obj[i].day}-{url_obj[i].month}-{url_obj[i].year}</h5>
                <img src={url_obj[i].url} alt="pic" className="UploadedPic" />
                <div>
                <h5 className="tags"><b><i>Tags: </i></b>{url_obj[i].tags.join(", ")}</h5>
                <h5 className="desc"><b><i>Desc: </i></b>{url_obj[i].desc}</h5>
                </div>
               
               
            </div>)
        }
        return (
            <div>
                <Jumbotron className="search">
                    <input className="tag_search" type="text" name='tagSearch' placeholder=" TagSearch" onChange={(e) => this.tagHandler(e)} />
                    <button type="submit" onClick={this.formHandler}>Submit</button>
                </Jumbotron>
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


