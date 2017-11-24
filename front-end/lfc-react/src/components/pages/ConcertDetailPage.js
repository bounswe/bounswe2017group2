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


//default from 'semantic-ui-react/dist/commonjs/collections/Table/TableRow';


const googleMapKey = "AIzaSyCrs1xLdXw8y4rfXc4tiJZZIWcwjmOR7BM";
const userID = 8;
const theToken = localStorage.getItem("lfcJWT");
//lat: 41.015, lng: 28.979

class CommentBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: '',
        }

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({
            value: event.target.value,
        });
    }

    handleSubmit(event) {
        console.log("Bearer " + theToken);
        console.log(this.state.value);
        axios.post('http://34.210.127.92:8000/concert/' + this.props.concertID + '/newcomment/', {
            'content': this.state.value,
        }, {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + theToken
            }).then(response => {
                window.location.reload();
            }, error => {
                console.log("refresh");
            });
        event.preventDefault();
    }

    render() {
        return (
            <form class="ui form" id="commentBox" onSubmit={this.handleSubmit}>
                <div class=" field">
                    <textarea rows="5" value={this.state.value} onChange={this.handleChange}></textarea>
                </div>
                <div class="ui icon buttons">
                    <button class="ui button">
                        <i class="photo icon"></i>
                    </button>
                    <button class="ui button">
                        <i class="sound icon"></i>
                    </button>
                    <button class="ui button">
                        <i class="film icon"></i>
                    </button>
                </div>
                <button class="ui right floated labeled icon button" type="Submit">
                    <i class="icon edit"></i>
                    Comment
                </button>
            </form>
        );
    }
}

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
            axios.get('http://34.210.127.92:8000/concert/' + this.props.match.params.concertID + '/subscribe', {
                'content': this.state.value,
            }, {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + theToken
                }).then(response => {
                    window.location.reload();
                }, error => {
                    console.log("refresh");
                });
        }
        else{
            axios.get('http://34.210.127.92:8000/concert/' + this.props.match.params.concertID + '/unsubscribe', {
                'content': this.state.value,
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
        console.log(this.props.username);
        var visibleMessage = "";
        var invisibleMessage = "";
        var dateOfConcert = new Date(this.state.concert.date_time);
        if (dateOfConcert > Date.now()) {
            visibleMessage = "Attending";
            invisibleMessage = "Not Attending";
        }
        else {
            visibleMessage = "Attended";
            invisibleMessage = "Didn't Attend";
        }
        if (this.state.concert.attendees.indexOf(userID) == -1) {
            var temp;
            temp = visibleMessage;
            visibleMessage = invisibleMessage;
            invisibleMessage = temp;
        }
        let commentBox = null;
        if (theToken) {
            commentBox = <CommentBox concertID={this.props.match.params.concertID} />;
        }
        var coor = this.state.concert.location.coordinates;
        this.state.concert.location.lat = parseFloat(coor.substring(0, coor.indexOf(" ")), 10);
        this.state.concert.location.lng = parseFloat(coor.substring(coor.indexOf(" ")), 10);
        var ConcertLocationMap = compose(
            withProps({
                googleMapURL: "https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=" + googleMapKey,
                loadingElement: <div style={{ height: `100%` }} />,
                containerElement: <div style={{ height: `300px` }} />,
                mapElement: <div style={{ height: `100%` }} />,
            }),
            withScriptjs,
            withGoogleMap,
        )((props) =>
            <GoogleMap
                defaultZoom={12}
                defaultCenter={{ lat: this.state.concert.location.lat, lng: this.state.concert.location.lng }}
            >
                <Marker position={{ lat: this.state.concert.location.lat, lng: this.state.concert.location.lng }} onClick={props.onMarkerClick}>
                    {<InfoWindow>
                        <h3><b>{this.state.concert.location.venue}</b></h3>
                    </InfoWindow>}
                </Marker>
            </GoogleMap>
            )
        return (
            <div class="ui grid segment start">
                <div class="row">
                    <h1 class="sixteen wide column">{this.state.concert.name}</h1>
                </div>
                <div class="row">
                    <div class="ui list sixteen wide column">
                        <div class="item"><b>Artist:</b>{this.state.concert.artist.name}</div>
                        <div class="item"><b>Date:</b>{this.state.concert.date_time}</div>
                        <div class="item"><b>Price:</b>{this.state.concert.price_min}TL-{this.state.concert.price_max}TL</div>
                        <div class="item"><b>Location:</b>{this.state.concert.location.venue}</div>
                    </div>
                </div>

                <div class="row">
                    <img class="ui image five wide column" height="300px" src={this.state.concert.artist.images[0].url} />
                    <div class="eleven wide column" >
                        <ConcertLocationMap
                            isMarkerShown={true}
                        />
                    </div>
                </div>
                <div class="row">
                    <div class="sixteen wide column">
                        <p>{this.state.concert.description}</p>
                        <button class="ui animated fade fluid button" onClick={this.handleFollowButton}>
                            <div class="visible content"> {visibleMessage} </div>
                            <div class="hidden content">
                                Mark as {invisibleMessage}
                            </div>
                        </button>
                    </div>
                </div>
                <div class="row">
                    <div class="sixteen wide column">
                        <div class="ui comments">
                            <h3 class="ui dividing header">Comments</h3>
                            {
                                this.state.concert.comments.map((comment) =>
                                    <div class="ui comment">
                                        <div class="content">
                                            <a class="author">
                                                <Link class="Link" to={"/user/" + 8}>
                                                    {comment.owner.first_name} {comment.owner.last_name}
                                                </Link>
                                            </a>
                                            <div class="text">
                                                {comment.content}
                                            </div>
                                            <div class="actions">
                                                <a>
                                                    <i class="arrow up icon"></i>
                                                </a>
                                                <a>
                                                    <i class="arrow down icon"></i>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                )
                            }
                            {commentBox}
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