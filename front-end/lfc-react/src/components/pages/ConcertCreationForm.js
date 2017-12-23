import ReactDOM from 'react-dom';
import axios from 'axios';
import { compose, withProps } from "recompose";
import { GoogleMap, Marker, withScriptjs, withGoogleMap, InfoWindow } from 'react-google-maps';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import React from "react";
import PropTypes from "prop-types";
import { Form, Button, Message, Dropdown } from "semantic-ui-react";
import { isEmail, isLength } from "validator";
import InlineError from "..//messages/InlineError";
import setAuthorizationHeader from "../../utils/setAuthorizationHeader";
const googleMapKey = "AIzaSyCrs1xLdXw8y4rfXc4tiJZZIWcwjmOR7BM";
const theToken = localStorage.lfcJWT;
//setAuthorizationHeader(theToken);	
class GoogleLocationChooser extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
      value: null,
      location: {},
      results:[],
      lat: 0.0,
      lng: 0.0
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  render (){
    
    return (
      <div>
      <div><label>
        Enter venue name: 
        <input type="text" value={this.state.value} onChange={this.handleChange} />
      </label>
      <input type="submit" value="Show Location" onClick={this.handleSubmit}/></div>
      <LocationMap lat={this.state.lat} lng={this.state.lng} venue_name={this.state.value}/>
      </div>
      );
  
  }
  handleChange(event) {
  this.setState({value: event.target.value});
  }

  handleSubmit(event) {
  event.preventDefault();
  var data={'name':this.state.value};
  console.log(data);	
  return fetch('https://maps.googleapis.com/maps/api/geocode/json?key='+googleMapKey+'&region=tr&address='+this.state.value)
  .then((response) => response.json())
  .then((responseJson) => {
    console.log(responseJson);
    this.setState({results:responseJson.results});
    this.setState({lat:responseJson.results[0].geometry.location.lat});
    this.setState({lng:responseJson.results[0].geometry.location.lng}); 
    this.setState({location:{'venue':this.state.value,'coordinates':responseJson.results[0].geometry.location.lat+' '+responseJson.results[0].geometry.location.lng}}); 
    this.props.onChange(this.state.location);  
  })
  .catch((error) => {
   console.error(error);
  });
    
  }  
}
class LocationMap extends React.Component{
  shouldComponentUpdate(nextProps,nextState){
      if(nextProps.lat!=this.props.lat)return true;
      return false;
  }
  render(){
  if(this.props.venue_name==null)return <div></div>;
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
            lat: Number(this.props.lat),
            lng: Number(this.props.lng)
        }}
    >
        <Marker
            position={{
                lat: Number(this.props.lat),
                lng: Number(this.props.lng)
            }}
            onClick={this.props.onMarkerClick}
        >
            {
                <InfoWindow>
                    <h3>
                        <b>{this.props.venue_name}</b>
                    </h3>
                </InfoWindow>
            }
        </Marker>
    </GoogleMap>
  ));
    return <ConcertLocationMap lng={this.props.lng} lat={this.props.lat} venue_name={this.props.venue_name} isMarkerShown={true}/>;
  }
}
class ConcertCreationForm extends React.Component {
    state= {
        data: {
            name: "",
            artist: {'name':'',
                    'spotify_id':'',
                    'images':[]
                  },
            date_time: "",
            description: "",
            price_min: 0,
            price_max: 0,
            tags: [],
            location: {'venue':null,
                       'coordinates':null},
            image: null,
            seller_url: null
        },
        loading: false,
        errors: {}
    };
    selectArtist = (artistData) => {
      console.log(artistData);
      console.log(window.location.host);
      this.setState({
        ...this.state,
        data: { ...this.state.data, ['artist']: artistData }
      });

    }
    selectVenue = (venueData) =>{
      console.log(venueData);
      this.setState({
        ...this.state,
        data: { ...this.state.data, ['location']: venueData }
      });
    }
    onChange = e =>
      this.setState({
        ...this.state,
        data: { ...this.state.data, [e.target.name]: e.target.value }
      });
  
    onSubmit = e => {
      e.preventDefault();
      const errors = this.validate(this.state.data);
      this.setState({ errors });
      if (Object.keys(errors).length === 0) {
        //const theToken = localStorage.lfcJWT;
        console.log(theToken);
        	console.log(JSON.stringify(this.state.data));
        axios.post('http://34.210.127.92:8000/newconcert/', this.state.data,{
          'Content-Type': 'application/json',
          Authorization: "Bearer " + theToken
          
      }
      ).then((responseJson) => {
          console.log(responseJson);
          window.open("http://"+window.location.host+"/concert/"+responseJson.data.concert_id,"_self")
      },error=>{
        console.log(error);
      }
    );
      }
    };
  
    validate = data => {
      const errors = {};
  

      return errors;
    };
  
    render() {
      const { data, errors, loading } = this.state;
      let lat,lng,venue_name;
      if(this.state.data.location.venue==null){
        venue_name=null;
      }else{
        lat=this.state.data.location.coordinates.substring(0,this.state.data.location.coordinates.indexOf(" "));
        lng=this.state.data.location.coordinates.substring(this.state.data.location.coordinates.indexOf(" ")+1,this.state.data.location.coordinates.length);
        venue_name=this.state.data.location.venue;
      }
      return (
        <Form onSubmit={this.onSubmit} loading={loading}>
          {errors.global && (
            <Message negative>
              <Message.Header>Something went wrong</Message.Header>
              <p>{errors.global}</p>
            </Message>
          )}
  
          <Form.Field>
            <label htmlFor="name">
              Concert Name
              <input
                name="name"
                value={data.name}
                onChange={this.onChange}
              />
            </label>
            
          </Form.Field>
  
          <Form.Field>
            <label htmlFor="description">
              Description 
              <input
                name="description"
                value={data.description}
                onChange={this.onChange}
              />
            </label>
          </Form.Field>
  
          <Form.Field>
            <label htmlFor="date_time">
              Date
              <input
               
                name="date_time"
                value={data.date_time}
                onChange={this.onChange}
              />
            </label>
          </Form.Field>
  
          <Form.Field>
            <label>
              Minimum ticket price
              <input
                type="number"
                name="price_min"
                value={data.price_min}
                onChange={this.onChange}
              />
            </label>
          </Form.Field>
  
          <Form.Field>
            <label>
              Maximum ticket price
              <input
                type="number"
                name="price_max"
                value={data.price_max}
                onChange={this.onChange}
              />
            </label>
          </Form.Field>
          <Form.Field>
          <ArtistForm onArtistSelected={this.selectArtist} />
          </Form.Field>
          <Form.Field>
            <GoogleLocationChooser onChange={this.selectVenue}/> 
            
          </Form.Field>  
          <Form.Field>
            <label>
              Seller url
              <input
              name="seller_url"
              value={data.seller_url}
              onChange={this.onChange}
              />
              </label>
            </Form.Field>
          <Button primary>Create Concert</Button>
        </Form>
      );
    }
  }
  

  ConcertCreationForm.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
}

class ArtistForm extends React.Component{
  constructor(props) {
  super(props);
  this.state = {
          selectedIndex: null,
          value: '',
          artists: [],
          
  };

  this.handleChange = this.handleChange.bind(this);
  this.handleSubmit = this.handleSubmit.bind(this);
  this.handleClick = this.handleClick.bind(this);
  }
  handleChange(event) {
  this.setState({value: event.target.value});
  }

  handleSubmit(event) {
      event.preventDefault();
      var data={'name':this.state.value};

      axios.get("http://34.210.127.92:8000/searchartists/",{
          params:data
      }
      ).then(resp => {
        this.setState({artists:resp.data});
      }).catch(err => {console.log(err)});

  }
    
  
  
  
  handleClick(e, data){
    let index=data.value;

    //this.setState({selectedArtist:this.state.artists[data.value]});
    let selectedArtist=this.state.artists[index]
    this.props.onArtistSelected(selectedArtist);
  }
  render() {
  var artists=[];
  for(var i=0;i<this.state.artists.length;i++){
    artists.push({
      text:this.state.artists[i].name,
      value:i,
      image:{avatar:true, src:this.state.artists[i].images[2] ? this.state.artists[i].images[2].url:""},

    }
    
  );
  }
  //console.log(artists);
  return (
    <div>
    <label>
      Enter artist name: 
      <input type="text" value={this.state.value} onChange={this.handleChange} />
    </label>
    <input type="submit" value="List Artists" onClick={this.handleSubmit} />
    <Dropdown onChange={this.handleClick} placeholder='Select Artist' fluid selection options={artists} />
    </div>
    
  );
  }
}
function mapStateToProps(state) {
    return {
        isAuthenticated: !!state.user.accessToken,
    }
}

export default connect(mapStateToProps)(ConcertCreationForm);
