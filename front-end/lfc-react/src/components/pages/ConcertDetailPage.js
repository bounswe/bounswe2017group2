import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import { compose, withProps } from "recompose";
import { GoogleMap, Marker, withScriptjs, withGoogleMap, InfoWindow } from 'react-google-maps';
import './index.css';


//lat: 41.015, lng: 28.979

class CommentBox extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: '',
            accessToken: '',
        }

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.refreshToken = this.refreshToken.bind(this);
    }

    refreshToken() {
        axios.post('http://34.210.127.92:8000/api/auth/token/refresh/', { "refresh": this.props.refreshToken })
            .then(response => {
                console.log("refreshed");
                console.log(response.data);
                this.state.accessToken = response.data.access;
            })

    }

    handleChange(event) {
        this.setState({
            value: event.target.value,
        });
    }

    handleSubmit(event) {
        axios.post('http://34.210.127.92:8000/concert/2/newcomment/', {
            'content': this.state.value,
        }, {
                headers: { Authorization: 'Bearer ' + this.state.accessToken },
            }).then(response => {
                window.location.reload();
            }, error => {
                this.refreshToken();
                this.handleSubmit(event);
            });
        event.preventDefault();
    }

    render() {
        return (
            <div id="commentFormDiv">
                <form onSubmit={this.handleSubmit}>
                    <textarea rows="5" id="commentBox" value={this.state.value} onChange={this.handleChange}></textarea>
                    <button id="addImageButton">Add Image...</button>
                    <button id="commentButton" type="Submit">Comment</button>
                </form>
            </div>
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
            },
            accessToken: '',
        };

        this.refreshToken = this.refreshToken.bind(this);
    }

    componentWillMount() {
        axios.get('http://34.210.127.92:8000/concert/2/')
            .then(response => {
                this.setState({
                    concert: response.data,
                })
            }, error => {
                this.refreshToken();
                this.componentWillMount();
            });
    }

    handleSubmit() {

    }

    refreshToken() {
        axios.post('http://34.210.127.92:8000/api/auth/token/refresh/', { "refresh": this.props.refreshToken })
            .then(response => {
                console.log("refreshed");
                console.log(response.data);
                this.state.accessToken = response.data.access;
            })

    }

    render() {
        let commentBox = null;
        if (this.state.accessToken) {
            commentBox = <CommentBox refreshToken={this.state.refreshToken} />;
        }
        var coor = this.state.concert.location.coordinates;
        this.state.concert.location.lat = parseFloat(coor.substring(0, coor.indexOf(" ")), 10);
        this.state.concert.location.lng = parseFloat(coor.substring(coor.indexOf(" ")), 10);
        console.log(this.state.concert.location.lat + ' ' + this.state.concert.location.lng);
        var ConcertLocationMap = compose(
            withProps({
                googleMapURL: "https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places",
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
            <div id="concertDetailsDiv">
                <div id="concertDataDiv">
                    <div id="concertNameDiv">
                        <h1 id="concertName">{this.state.concert.name}</h1>
                    </div>
                    <div id="concertInfoDiv">
                        <div id="artistDiv"><b>Artist:</b>{this.state.concert.artist.name}</div>
                        <div id="dateDiv"><b>Date:</b>{this.state.concert.date_time}</div>
                        <div id="priceDiv"><b>Price:</b>{this.state.concert.price_min}-{this.state.concert.price_max}</div>
                        <div id="locationDiv"><b>Location:</b>{this.state.concert.location.venue}</div>
                    </div>
                    <div id="artistAndMapDiv">
                        <div id="artistImageDiv"><img id="artistImage" src={this.state.concert.artist.images[0].url} /></div>
                        <div id="mapDiv" >
                            <ConcertLocationMap
                                isMarkerShown={true}
                            />
                        </div>
                    </div>
                    <div id="concertDescriptionDiv"><p>{this.state.concert.description}</p></div>
                </div>
                <div id="comments">
                    <ul>
                        {
                            this.state.concert.comments.map((comment) =>
                                <li>
                                    <div className="commentDiv">{comment.owner.first_name} {comment.owner.last_name}:<br />{comment.content}</div>
                                </li>
                            )
                        }

                    </ul>
                    {commentBox}

                </div >
            </div >
        );
    }
}


ReactDOM.render(<Concert
    refreshToken=""
/>, document.getElementById("root"));

/*Oha 34 lira mı??? Kesin gidicem. En sevdiğim grup zaten.*/