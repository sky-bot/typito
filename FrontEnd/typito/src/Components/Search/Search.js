import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Search.css'


class Search extends Component {

    state = {
        'status': "",
        'endDate': null,
        'startDate': null
    }

    startDateChangeHandler(e) {
        e.preventDefault();
        this.setState({'startDate': e.target.value})
    }

    endDateChangeHandler(e) {
        e.preventDefault();
        this.setState({'endDate': e.target.value})
    }


    formHandler() {
        console.log("formHandler")
    }

    render() {
        return (
            <div>
                <div>
                    <label className="label">From</label>
                    <input type="date" name="startdate" onChange={(e) => this.startDateChangeHandler(e)} />
                    <label className="label">To</label>
                    <input type="date" name="enddate" onChange={(e) => this.endDateChangeHandler(e)} />
                    <input className="label" type="text" name='tagSearch' placeholder=" TagSearch" onChange={(e) => this.endDateChangeHandler(e)}/>
                    <button type="submit" onClick={this.formHandler}>Submit</button>
                </div>
                <h4 className="Status">{this.state.status}</h4>
                
            </div>
        );
    }
}

export default Search;