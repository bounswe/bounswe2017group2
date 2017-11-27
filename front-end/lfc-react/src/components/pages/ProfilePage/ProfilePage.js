import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import './design.css';
import decode from "jwt-decode";


let theToken = localStorage.getItem("lfcJWT");
let userID = decode(localStorage.lfcJWT).user_id;


class MiniConcertDetail extends React.Component {
    constructor(props) {
        super(props);
        this.handleRemove = this.handleRemove.bind(this);
    }
    render() {
        let removeButton;
        if (this.props.isCurrentUser) {
            removeButton = (
                <button className=" circular mini ui icon right floated button" onClick={() => this.handleRemove()}>
                    <i className="remove icon"></i>
                </button>
            );
        }
        return (
            <div className="ui grid segment">
                <img className="ui image three wide column" height="100px" src={this.props.concert.artist.images[0].url} />
                <div className="ten wide column">
                    <h3><Link className="Link" to={"/concert/" + this.props.concert.concert_id}>{this.props.concert.name}</Link></h3>
                    <h4>{this.props.concert.date_time} {this.props.concert.location.venue}</h4>
                </div>
                <div className="three wide column">
                    {removeButton}
                </div>
            </div>
        )
    }

    handleRemove(event) {
        axios.post('http://34.210.127.92:8000/concert/' + this.props.concert.concert_id + '/unsubscribe/', {
        }, {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + theToken
            }).then(response => {
                window.location.reload();
            }, error => {
                console.log("refresh");
            });
    }
}

class ProfilePage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            user: {
                username: '',
                email: '',
                first_name: '',
                last_name: '',
                birth_date: '',
                age: 0,
                comments: [],
                concerts: [],
                date_joined: '',
            },
            willAttend: [],
            attended: [],
            followers: [],
            following: [],
            accessToken: theToken,
        };
        this.handleTab = this.handleTab.bind(this);
    }

    removeActive(tabName){
        if (document.getElementById(tabName).classList.contains("active")){
            document.getElementById(tabName).classList.remove("active");
            document.getElementById(tabName+"Tab").classList.remove("active");
        }
    }

    handleTab(tabName) {
        this.removeActive("concerts");
        this.removeActive("generalInfo");
        this.removeActive("followedUsers");
        this.removeActive("followers");
        document.getElementById(tabName).classList.add("active");
        document.getElementById(tabName+"Tab").classList.add("active");
    }

    componentWillMount() {
        let userID = this.props.match.params.userID;
        axios.get('http://34.210.127.92:8000/user/' + userID + '/')
            .then(response => {
                var userData = response.data;
                var willAttendList = [];
                var attendedList = [];
                axios.get('http://34.210.127.92:8000/user/get_concerts/', {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + theToken
                })
                    .then(response => {
                        for (let concert of response.data) {
                            let dateOfConcert = new Date(concert.date_time);
                            if (dateOfConcert > Date.now())
                                willAttendList.push(concert);
                            else
                                attendedList.push(concert);
                        }

                        this.setState({
                            willAttend: willAttendList,
                            attended: attendedList,
                        })
                    }, error => {
                        console.log("refresh concert");
                    });
                console.log(userData);
                this.setState({
                    user: userData,
                })
            }, error => {
                console.log("refresh user");
            });
    }


    render() {
        console.log(userID + " " + this.props.match.params.concertID);
        var attendedConcerts = this.state.attended.map((cncrt) =>
            <MiniConcertDetail concert={cncrt} isCurrentUser={userID == this.props.match.params.userID} />
        );
        var willAttendConcerts = this.state.willAttend.map((cncrt) =>
            <MiniConcertDetail concert={cncrt} isCurrentUser={userID == this.props.match.params.userID} />
        );
        var age = Math.floor((Date.now() - (new Date(this.state.user.birth_date))) / (1000 * 60 * 60 * 24 * 365));
        return (
            <div className="ui grid" id="profilePage">
                <div className="row">
                    <img className="ui image two wide column" height="130px" src={"http://34.210.127.92:8000" + this.state.user.image} />
                    <div className="twelve wide column">
                        <div className="ui grid">
                            <div className="row usersName">{this.state.user.first_name + ' ' + this.state.user.last_name}</div>
                            <div className="row username"><b>username</b> &nbsp; {this.state.user.username}</div>
                            <div className="row followCounters"><b>followers</b> &nbsp; {this.state.followers.length} &nbsp; <b>following</b> &nbsp; {this.state.following.length}</div>
                        </div>
                    </div>
                    <div className="two wide column">
                        <button className="ui  floated button">
                            Edit Profile
                        </button>
                    </div>
                </div>
                <div className="row">
                    <div className="ui top attached tabular menu">
                        <a className="active item" id="concerts" onClick={() => this.handleTab("concerts") }> Concerts</a>
                        <a className="item" id="generalInfo" onClick={() => this.handleTab("generalInfo")}>General Information</a>
                        <a className="item" id="followedUsers" onClick={() => this.handleTab("followedUsers")} > Followed Users</a>
                        <a className="item" id="followers" onClick={() => this.handleTab("followers")} > Followers</a>
                    </div>
                    <div className="ui bottom attached active tab segment" id="concertsTab">
                        <div className="ui grid">
                            <div className="eight wide column center">
                                <h3>Future Concerts</h3>
                                {willAttendConcerts}
                            </div>
                            <div className="eight wide column center">
                                <h3>Concert History</h3>
                                {attendedConcerts}
                            </div>
                        </div>
                    </div>
                    <div className="ui bottom attached tab segment" id="generalInfoTab">
                        <div className="ui list">
                            <div className="item userData"><b>e-mail</b> &nbsp; {this.state.user.email}</div>
                            <div className="item userData"><b>birth date</b> &nbsp; {this.state.user.birth_date}</div>
                            <div className="item userData"><b>comments</b> &nbsp; {this.state.user.comments.length}</div>
                            <div className="item userData"><b>concerts</b> &nbsp; {this.state.user.concerts.length}</div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

ProfilePage.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
}

function mapStateToProps(state) {
    return {
        isAuthenticated: !!state.user.accessToken,
    }
}

export default connect(mapStateToProps)(ProfilePage);