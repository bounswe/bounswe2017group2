import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import { compose, withProps } from "recompose";
import { GoogleMap, Marker, withScriptjs, withGoogleMap, InfoWindow } from 'react-google-maps';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { Button } from 'semantic-ui-react';
import './design.css';
import $ from 'jquery';
import decode from "jwt-decode";

//default from 'semantic-ui-react/dist/commonjs/collections/Table/TableRow';


const googleMapKey = "AIzaSyCrs1xLdXw8y4rfXc4tiJZZIWcwjmOR7BM";
var userID;
const theToken = localStorage.getItem("lfcJWT");
//lat: 41.015, lng: 28.979

class Concert extends React.PureComponent {
    constructor(props) {
        super(props);
        this.state = {
            concert: {
                name: '',
                artist: {
                    name: '',
                    images: [{
                        url: '',
                    }],
                },
                date_time: '',
                price_min: '',
                price_max: '',
                location: {
                    venue: '',
                    coordinates: '',
                    lat: 0,
                    lng: 0,
                },
                description: '',
                comments: [{
                    content: '',
                    owner: {
                        first_name: '',
                        last_name: '',
                    },
                }],
                attendees: [],
            },
        };

        this.handleFollowButton = this.handleFollowButton.bind(this);

    }

    componentWillMount() {
        axios.get('http://34.210.127.92:8000/concert/' + this.props.match.params.concertID + '/')
            .then(response => {
                this.setState({
                    concert: response.data,
                })
            }, error => {
                console.log("refresh");
            });
    }

    handleSubmit() {

    }

    handleFollowButton(event) {
        if (this.state.concert.attendees.indexOf(userID) == -1) {
            axios.post('http://34.210.127.92:8000/concert/' + this.props.match.params.concertID + '/subscribe/', {
            }, {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + theToken
                }).then(response => {
                    window.location.reload();
                }, error => {
                    console.log("refresh");
                });
        }
        else {
            axios.post('http://34.210.127.92:8000/concert/' + this.props.match.params.concertID + '/unsubscribe/', {
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

    render() {
        userID = decode(localStorage.lfcJWT).user_id;
        console.log(userID);
        return (
            <div className="ui grid segment start">
                <div className="row">
                    <h1 className="sixteen wide column">{this.state.concert.name}</h1>
                </div>
                <div className="row">
                    <div className="ui list sixteen wide column">
                        <div className="item"><b>Artist:</b>{this.state.concert.artist.name}</div>
                        <div className="item"><b>Date:</b>{this.state.concert.date_time}</div>
                        <div className="item"><b>Price:</b>{this.state.concert.price_min}TL-{this.state.concert.price_max}TL</div>
                        <div className="item"><b>Location:</b>{this.state.concert.location.venue}</div>
                    </div>
                </div>

                <div className="row">
                    <img className="ui image five wide column" height="300px" src={this.state.concert.artist.images[0].url} />

                </div>



                <div className="row">
                    <div className="sixteen wide column">
                        <p>{this.state.concert.description}</p>

                        
                    </div>
                </div>

                <div className="row">
                    <div className="sixteen wide column">
                        <div className="ui comments">
                            <h3 className="ui dividing header">Comments</h3>
                            {
                                this.state.concert.comments.map((comment) =>
                                    <div className="ui comment">
                                        <div className="content">
                                            <a className="author">{comment.owner.first_name} {comment.owner.last_name}</a>
                                            <div className="text">
                                                {comment.content}
                                            </div>
                                            <div className="actions">
                                                <a>
                                                    <i className="arrow up icon"></i>
                                                </a>
                                                <a>
                                                    <i className="arrow down icon"></i>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                )
                            }
                        </div>
                    </div>
                </div >
            </div >


        );
    }
}

Concert.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
    userID: PropTypes.string,
}

function mapStateToProps(state) {
    return {
        isAuthenticated: !!state.user.accessToken,
        userID: state.user.username,
    }
}

export default connect(mapStateToProps)(Concert);

/*Oha 34 lira mı??? Kesin gidicem. En sevdiğim grup zaten.*/