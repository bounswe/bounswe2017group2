import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import './design.css'

const theToken = localStorage.getItem("lfcJWT");

function refreshToken(cmpnnt) {
    axios.post('http://34.210.127.92:8000/api/auth/token/refresh/', { "refresh": cmpnnt.props.refreshToken })
        .then(response => {
            console.log("refreshed");
            console.log(response.data);
            cmpnnt.accessToken = response.data.access;
        })

}

class MiniConcertDetail extends React.Component {
    render() {
        console.log(this.props.concert);
        return (
            <div class="ui grid segment">
                <img class="ui image three wide column" height="100px" src={this.props.concert.artist.images[0].url} />
                <div class="ten wide column">
                    <h3><Link class="Link" to={"/concert/" + this.props.concert.concert_id}>{this.props.concert.name}</Link></h3>
                    <h4>{this.props.concert.date_time} {this.props.concert.location.venue}</h4>
                </div>
                <div class="three wide column">
                    <button class=" circular mini ui icon right floated button">
                        <i class="remove icon"></i>
                    </button>
                </div>
            </div>
        )
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
            },
            willAttend: [],
            attended: [],
            accessToken: theToken,
        };
    }

    componentWillMount() {
        let userID = this.props.match.params.userID;
        console.log(userID);
        axios.get('http://34.210.127.92:8000/user/' + userID + '/')
            .then(response => {
                var userData = response.data;
                var willAttendList = [];
                var attendedList = [];
                for (let concertID of response.data.concerts) {
                    axios.get('http://34.210.127.92:8000/concert/' + concertID + '/')
                        .then(response => {
                            var concert = response.data;
                            var dateOfConcert = new Date(concert.date_time);
                            if (dateOfConcert > Date.now())
                                willAttendList.push(concert);
                            else
                                attendedList.push(concert);
                            this.setState({
                                user: userData,
                                willAttend: willAttendList,
                                attended: attendedList,
                            })
                        }, error => {
                            refreshToken(this);
                            this.componentWillMount();
                        });
                }
                this.setState({
                    user: userData,
                    willAttend: willAttendList,
                    attended: attendedList,
                })
            }, error => {
                refreshToken(this);
                this.componentWillMount();
            });
    }

    handleSubmit() {

    }

    render() {
        refreshToken(this);
        var attendedConcerts = this.state.attended.map((cncrt) =>
            <MiniConcertDetail concert={cncrt} past={true} />
        );
        var willAttendConcerts = this.state.willAttend.map((cncrt) =>
            <MiniConcertDetail concert={cncrt} past={false} />
        );
        var age = Math.floor((Date.now() - (new Date(this.state.user.birth_date))) / (1000 * 60 * 60 * 24 * 365));
        return (
            <div class="ui grid" id="profilePage">
                <div class="row">
                    <div class="sixteen wide column">
                        <div class="item usersName">{this.state.user.first_name + ' ' + this.state.user.last_name}</div>
                    </div>
                </div>
                <div class="row">
                    <div class="ui top attached tabular menu">
                        <a class="active item" data-tab="concerts">Concerts</a>
                        <a class="item" data-tab="followedUsers">Followed Users</a>
                        <a class="item" data-tab="followers">Followers</a>
                    </div>
                    <div class="ui bottom attached active tab segment" data-tab="concerts">
                        <div class="ui grid">
                            <div class="eight wide column center">
                                <h3>Future Concerts</h3>
                                {willAttendConcerts}
                            </div>
                            <div class="eight wide column center">
                                <h3>Concert History</h3>
                                {attendedConcerts}
                            </div>
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