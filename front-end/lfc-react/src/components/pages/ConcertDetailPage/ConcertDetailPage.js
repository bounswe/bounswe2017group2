/* eslint-disable */

import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import { compose, withProps } from "recompose";
import {
    GoogleMap,
    Marker,
    withScriptjs,
    withGoogleMap,
    InfoWindow
} from "react-google-maps";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { Button, Rating, Label, Popup } from "semantic-ui-react";
import "./design.css";
import decode from "jwt-decode";
import setAuthorizationHeader from "../../../utils/setAuthorizationHeader";
import MiniUserDetail from "../ProfilePage/ProfilePage";
import Segment from "semantic-ui-react/dist/commonjs/elements/Segment/Segment";
import Icon from "semantic-ui-react/dist/commonjs/elements/Icon/Icon";

//default from 'semantic-ui-react/dist/commonjs/collections/Table/TableRow';

const googleMapKey = "AIzaSyCrs1xLdXw8y4rfXc4tiJZZIWcwjmOR7BM";
let userID;
let isLoggedIn = false;
let isRated = [0, 0, 0, 0];
let currentRatings;
const theToken = localStorage.lfcJWT;
let averageRatings;
let isFutureConcert;
let isFollowedConcert = false;
setAuthorizationHeader(theToken);

//lat: 41.015, lng: 28.979

class CommentBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: ""
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        this.setState({
            value: event.target.value
        });
    }

    handleSubmit(event) {
        axios
            .post(
            "http://34.210.127.92:8000/concert/" +
            this.props.concertID +
            "/newcomment/",
            {
                content: this.state.value
            }
            )
            .then(
            response => {
                window.location.reload();
            },
            error => {
                console.log(theToken);
                console.log("refresh");
            }
            );
        event.preventDefault();
    }

    render() {
        return (
            <form className="ui form" id="commentBox" onSubmit={this.handleSubmit}>
                <div className=" field">
                    <textarea
                        rows="5"
                        value={this.state.value}
                        onChange={this.handleChange}
                    />
                </div>
                <div className="ui icon buttons">
                    <button className="ui button">
                        <i className="photo icon" />
                    </button>
                    <button className="ui button">
                        <i className="sound icon" />
                    </button>
                    <button className="ui button">
                        <i className="film icon" />
                    </button>
                </div>
                <button className="ui right floated labeled icon button" type="Submit">
                    <i className="icon edit" />
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
                name: "",
                artist: {
                    name: "",
                    images: [
                        {
                            url: ""
                        }
                    ]
                },
                date_time: "",
                price_min: "",
                price_max: "",
                location: {
                    venue: "",
                    coordinates: "",
                    lat: 0,
                    lng: 0
                },
                description: "",
                comments: [
                    {
                        content: "",
                        owner: {
                            first_name: "",
                            last_name: ""
                        }
                    }
                ],
                attendees: [],
                ratings: [],
                seller_url: '',
                tags: [],
            }
        };

        this.handleFollowButton = this.handleFollowButton.bind(this);
        this.handleRate1 = this.handleRate1.bind(this);
        this.handleRate2 = this.handleRate2.bind(this);
        this.handleRate3 = this.handleRate3.bind(this);
        this.handleRate4 = this.handleRate4.bind(this);
    }

    componentWillMount() {
        axios
            .get(
            "http://34.210.127.92:8000/concert/" +
            this.props.match.params.concertID +
            "/"
            )
            .then(
            response => {
                this.setState({
                    concert: response.data
                });
            },
            error => {
                console.log("refresh");
            }
            );
        axios
            .get(
            "http://34.210.127.92:8000/concert/" +
            this.props.match.params.concertID +
            "/average_ratings/"
            )
            .then(
            response => {
                averageRatings = response.data;
            },
            error => {
                console.log("refresh");
            }
            );
    }

    handleSubmit() { }

    updateRating() {
        if (isRated[0] && isRated[1] && isRated[2] && isRated[3]) {
            axios
                .post(
                "http://34.210.127.92:8000/concert/" +
                this.props.match.params.concertID +
                "/rate/",
                {
                    concert_atmosphere: isRated[3],
                    artist_costumes: isRated[2],
                    music_quality: isRated[0],
                    stage_show: isRated[1]
                }
                )
                .then(
                response => {
                    window.location.reload();
                },
                error => {
                    console.log("refresh");
                }
                );
        }
    }

    handleRate1(event, { rating, maxRating }) {
        currentRatings.music_quality = rating;
        isRated[0] = rating;
        this.updateRating();
    }

    handleRate2(event, { rating, maxRating }) {
        currentRatings.stage_show = rating;
        isRated[1] = rating;
        this.updateRating();
    }
    handleRate3(event, { rating, maxRating }) {
        currentRatings.artist_costumes = rating;
        isRated[2] = rating;
        this.updateRating();
    }
    handleRate4(event, { rating, maxRating }) {
        currentRatings.concert_atmosphere = rating;
        isRated[3] = rating;
        this.updateRating();
    }

    handleFollowButton(event) {
        if (!isFollowedConcert) {
            axios
                .post(
                "http://34.210.127.92:8000/concert/" +
                this.props.match.params.concertID +
                "/subscribe/",
                {}
                )
                .then(
                response => {
                    window.location.reload();
                },
                error => {
                    console.log("refresh");
                }
                );
        } else {
            axios
                .post(
                "http://34.210.127.92:8000/concert/" +
                this.props.match.params.concertID +
                "/unsubscribe/",
                {},
                {
                    "Content-Type": "application/json",
                    Authorization: "Bearer " + theToken
                }
                )
                .then(
                response => {
                    window.location.reload();
                },
                error => {
                    console.log("refresh");
                }
                );
        }
    }

    render() {
        const { token, isAuthenticated } = this.props;
        if (localStorage.lfcJWT) {
            userID = decode(localStorage.lfcJWT).user_id;
            //console.log(localStorage.getItem("lfcJWT"));
        }
        isLoggedIn = isAuthenticated;


        var visibleMessage = "";
        var invisibleMessage = "";
        var dateOfConcert = new Date(this.state.concert.date_time);
        isFutureConcert = dateOfConcert > Date.now();
        let ratingsHeaders;
        if (isFutureConcert) {
            visibleMessage = "Attending";
            invisibleMessage = "Not Attending";
        } else {
            if (averageRatings && averageRatings.music_quality) {
                ratingsHeaders = (
                    <div className="ui grid">
                        <div className="four wide column center ratingHeaders">
                            <div>
                                <h5>Music Quality: {Number(averageRatings.music_quality).toFixed(1)}</h5>
                            </div>
                        </div>
                        <div className="four wide column center ratingHeaders">
                            <div>
                                <h5>Stage Show: {Number(averageRatings.stage_show).toFixed(1)}</h5>
                            </div>
                        </div>
                        <div className="four wide column center ratingHeaders">
                            <div>
                                <h5>Artist Costumes: {Number(averageRatings.artist_costumes).toFixed(1)}</h5>
                            </div>
                        </div>
                        <div className="four wide column center ratingHeaders">
                            <div>
                                <h5>Concert Atmosphere: {Number(averageRatings.concert_atmosphere).toFixed(1)}</h5>
                            </div>
                        </div>
                    </div>
                );
            }
            visibleMessage = "Attended";
            invisibleMessage = "Didn't Attend";
        }

        for (let attendee of this.state.concert.attendees) {
            if (attendee.id == userID) {
                isFollowedConcert = true;
                break;
            }
        }

        if (!isFollowedConcert) {
            var temp;
            temp = visibleMessage;
            visibleMessage = invisibleMessage;
            invisibleMessage = temp;
        }
        let commentBox = null;
        if (isLoggedIn) {
            commentBox = <CommentBox concertID={this.props.match.params.concertID} />;
        }

        let followConcertButton;
        let rateButtons;

        if (isLoggedIn) {
            currentRatings = this.state.concert.ratings.find(function (rating) {
                return rating.owner === userID;
            });
            if (!currentRatings) {
                currentRatings = {
                    music_quality: 0,
                    artist_costumes: 0,
                    stage_show: 0,
                    concert_atmosphere: 0,
                }
            }
            followConcertButton = (
                <button
                    className="ui animated fade fluid button"
                    onClick={this.handleFollowButton}
                >
                    <div className="visible content"> {visibleMessage} </div>
                    <div className="hidden content">Mark as {invisibleMessage}</div>
                </button>
            );
            if (visibleMessage == "Attended") {
                if (!ratingsHeaders) {
                    ratingsHeaders = (
                        <div className="ui grid">
                            <div className="four wide column center ratingHeaders">
                                <div>
                                    <h5>Music Quality</h5>
                                </div>
                            </div>
                            <div className="four wide column center ratingHeaders">
                                <div>
                                    <h5>Stage Show</h5>
                                </div>
                            </div>
                            <div className="four wide column center ratingHeaders">
                                <div>
                                    <h5>Artist Costumes</h5>
                                </div>
                            </div>
                            <div className="four wide column center ratingHeaders">
                                <div>
                                    <h5>Concert Atmosphere</h5>
                                </div>
                            </div>
                        </div>
                    );

                }
                rateButtons = (
                    <div className="ui grid">
                        <div className="four wide column center stars">
                            <Rating
                                icon="star"
                                maxRating={5}
                                defaultRating={currentRatings.music_quality}
                                onRate={this.handleRate1}
                            />
                        </div>
                        <div className="four wide column center stars">
                            <Rating
                                icon="star"
                                maxRating={5}
                                defaultRating={currentRatings.stage_show}
                                onRate={this.handleRate2}
                            />
                        </div>
                        <div className="four wide column center stars">
                            <Rating
                                icon="star"
                                maxRating={5}
                                defaultRating={currentRatings.artist_costumes}
                                onRate={this.handleRate3}
                            />
                        </div>
                        <div className="four wide column center stars">
                            <Rating
                                icon="star"
                                maxRating={5}
                                defaultRating={currentRatings.concert_atmosphere}
                                onRate={this.handleRate4}
                            />
                        </div>
                    </div>
                );
            }
        }

        var coor = this.state.concert.location.coordinates;
        this.state.concert.location.lat = parseFloat(
            coor.substring(0, coor.indexOf(" ")),
            10
        );
        this.state.concert.location.lng = parseFloat(
            coor.substring(coor.indexOf(" ")),
            10
        );
        var ConcertLocationMap = compose(
            withProps({
                googleMapURL:
                    "https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places&key=" +
                    googleMapKey,
                loadingElement: <div style={{ height: `100%` }} />,
                containerElement: <div style={{ height: `300px` }} />,
                mapElement: <div style={{ height: `100%` }} />
            }),
            withScriptjs,
            withGoogleMap
        )(props => (
            <GoogleMap
                defaultZoom={12}
                defaultCenter={{
                    lat: this.state.concert.location.lat,
                    lng: this.state.concert.location.lng
                }}
            >
                <Marker
                    position={{
                        lat: this.state.concert.location.lat,
                        lng: this.state.concert.location.lng
                    }}
                    onClick={props.onMarkerClick}
                >
                    {
                        <InfoWindow>
                            <h3>
                                <b>{this.state.concert.location.venue}</b>
                            </h3>
                        </InfoWindow>
                    }
                </Marker>
            </GoogleMap>
        ));

        let price;
        if (this.state.concert.price_max > this.state.concert.price_min) {
            price = (
                <p>
                    <b>Price: </b>&#8378;{this.state.concert.price_min}-&#8378;{
                        this.state.concert.price_max
                    }
                </p>
            );
        } else {
            price = (
                <p>
                    <b>Price: </b>&#8378;{this.state.concert.price_min}
                </p>
            );
        }

        return (
            <div className="ui grid raised segment">
                <div className="row">
                    <div className="ui grid twelve wide column">
                        <div className="row">
                            <div className="fourteen wide column">
                                <Label as="a" ribbon id="concertNameRibbon">
                                    <h1>{this.state.concert.name}</h1>
                                </Label>
                            </div>
                        </div>
                        <div className="row tagsRow">
                            <div className="sixteen wide column">
                                {this.state.concert.tags.map(tag => (
                                    <div className="ui label">
                                        <i className="hashtag icon"></i>
                                        {tag.value}
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div className="row">
                            <div className="ui list sixteen wide column">
                                <div className="item concertData">
                                    <b>Artist: </b>
                                    {this.state.concert.artist.name}
                                </div>
                                <div className="item concertData">
                                    <b>Date: </b>
                                    {this.state.concert.date_time}
                                </div>
                                <div className="item concertData">{price}
                                </div>
                                <div className="item concertData">
                                    <b>Location: </b>
                                    {this.state.concert.location.venue}
                                </div>
                            </div>
                        </div>
                    </div>
                    {this.state.concert.attendees.length > 0 && (
                        <div className="ui segment" style={{ maxHeight: "250px", width: "280px", paddingTop: "20px" }}>
                            <div>
                                <div className="center">
                                    <Label attached="top">
                                        {this.state.concert.attendees.length} L4C user
                                        {this.state.concert.attendees.length > 1 && ("s ")}
                                        will attend
                                        <Label.Detail>
                                            <a style={{ color: "#800000" }} href={"http://" + this.state.concert.seller_url}>Get ticket</a>
                                        </Label.Detail>
                                    </Label>
                                </div>
                                <div className="ui grid basic segment" style={{ maxHeight: "210px", overflowY: "auto" }}>
                                    <div className="sixteen wide column" style={{ padding: "2px" }}>
                                        {this.state.concert.attendees.map(attendee => (
                                            <div className="row" style={{ marginTop: "3px" }}>
                                                <Segment>
                                                    <Link className="Link" to={"/user/" + attendee.id}>
                                                        <Icon name="user circle" />{attendee.username}
                                                    </Link>
                                                </Segment>
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                    {this.state.concert.attendees.length == 0 && (
                        <div style={{ paddingTop: "20px", width: "280px", textAlign: "right" }}>
                            <a href={"http://" + this.state.concert.seller_url}>
                                <Button>Get ticket</Button>
                            </a>
                        </div>
                    )}
                </div>

                <div className="row">
                    <img
                        className="ui image five wide column"
                        height="300px"
                        src={this.state.concert.artist.images[0].url}
                    />
                    <div className="eleven wide column">
                        <ConcertLocationMap isMarkerShown={true} />
                    </div>
                </div>

                <div className="row">
                    <div className="sixteen wide column">
                        <p>{this.state.concert.description}</p>

                        {ratingsHeaders}
                        {rateButtons}

                        {followConcertButton}
                    </div>
                </div>

                <div className="row">
                    <div className="sixteen wide column">
                        <div className="ui comments">
                            <h3 className="ui dividing header">Comments</h3>
                            {this.state.concert.comments.map(comment => (
                                <div className="ui comment">
                                    <div className="content">
                                        <a className="author">
                                            <Link className="Link" to={"/user/" + comment.owner.id}>
                                                {comment.owner.first_name} {comment.owner.last_name}
                                            </Link>
                                        </a>
                                        <div className="text">{comment.content}</div>
                                        <div className="actions">
                                            <a>
                                                <i className="arrow up icon" />
                                            </a>
                                            <a>
                                                <i className="arrow down icon" />
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            ))}

                            {commentBox}
                        </div>
                    </div>
                </div>
            </div >
        );
    }
}

Concert.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
    userID: PropTypes.string
};

function mapStateToProps(state) {
    return {
        isAuthenticated: !!state.user.access_token,
        token: state.user.access_token,
        userID: state.user.username
    };
}

export default connect(mapStateToProps)(Concert);

/*Oha 34 lira mı??? Kesin gidicem. En sevdiğim grup zaten.*/
