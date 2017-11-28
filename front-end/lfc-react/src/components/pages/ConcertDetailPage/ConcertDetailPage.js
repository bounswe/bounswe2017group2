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
            <form className="ui form" id="commentBox" onSubmit={this.handleSubmit}>
                <div className=" field">
                    <textarea rows="5" value={this.state.value} onChange={this.handleChange}></textarea>
                </div>
                <div className="ui icon buttons">
                    <button className="ui button">
                        <i className="photo icon"></i>
                    </button>
                    <button className="ui button">
                        <i className="sound icon"></i>
                    </button>
                    <button className="ui button">
                        <i className="film icon"></i>
                    </button>
                </div>
                <button className="ui right floated labeled icon button" type="Submit">
                    <i className="icon edit"></i>
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

        let price;
        if (this.state.concert.price_max > this.state.concert.price_min) {
            price=(<p><b>Price:</b>&#8378;{this.state.concert.price_min}-&#8378;{this.state.concert.price_max}</p>);
        }
        else{
            price=(<p><b>Price:</b>&#8378;{this.state.concert.price_min}</p>)
        }


        return (
            <div className="ui grid segment">
                <div className="row">
                    <h1 className="sixteen wide column">{this.state.concert.name}</h1>
                </div>
                <div className="row">
                    <div className="ui list sixteen wide column">
                        <div className="item"><b>Artist:</b>{this.state.concert.artist.name}</div>
                        <div className="item"><b>Date:</b>{this.state.concert.date_time}</div>
                        <div className="item">{price}</div>
                        <div className="item"><b>Location:</b>{this.state.concert.location.venue}</div>
                    </div>
                </div>

                <div className="row">
                    <img className="ui image five wide column" height="300px" src={this.state.concert.artist.images[0].url} />
                    <div className="eleven wide column" >
                        <ConcertLocationMap
                            isMarkerShown={true}
                        />
                    </div>
                </div>



                <div className="row">
                    <div className="sixteen wide column">
                        <p>{this.state.concert.description}</p>

                        <button className="ui animated fade fluid button" onClick={this.handleFollowButton}>
                            <div className="visible content"> {visibleMessage} </div>
                            <div className="hidden content">
                                Mark as {invisibleMessage}
                            </div>
                        </button>

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
                                            <a className="author">
                                                <Link className="Link" to={"/user/" + comment.owner.id}>
                                                    {comment.owner.first_name} {comment.owner.last_name}
                                                </Link>
                                            </a>
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