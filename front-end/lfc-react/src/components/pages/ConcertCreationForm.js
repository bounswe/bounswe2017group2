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
import DayPickerInput from 'react-day-picker/DayPickerInput';
import{TagForm,ArtistForm,GoogleLocationChooser}from '../forms/ConcertForms.js'
import 'react-day-picker/lib/style.css';
import InlineError from "..//messages/InlineError";
const googleMapKey = "AIzaSyCrs1xLdXw8y4rfXc4tiJZZIWcwjmOR7BM";
const theToken = localStorage.lfcJWT;
//setAuthorizationHeader(theToken);	

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
            location: {'venue':"",
                       'coordinates':""},
            image: null,
            seller_url: null
        },
        loading: false,
        errors: {}
    };
    selectArtist = (artistData) => {
      this.setState({
        ...this.state,
        data: { ...this.state.data, ['artist']: artistData }
      });

    }
    selectVenue = (venueData) =>{
      this.setState({
        ...this.state,
        data: { ...this.state.data, ['location']: venueData }
      });
    }
    dayChange = (day) =>{
      if(day)
      this.setState({
        ...this.state,
        data: { ...this.state.data, ['date_time']: day.getFullYear()+'-'+(day.getMonth()+1)+'-'+day.getDate() }
      });
      
    }
    selectTag=(tags)=>{
      this.setState({
        ...this.state,
        data: { ...this.state.data, ['tags']: tags }
      });
    }
    onChange = e =>{
      if(e.target.name=="seller_url")e.target.value=e.target.value.replace(/^(https?:|)\/\//,'');
      this.setState({
        ...this.state,
        data: { ...this.state.data, [e.target.name]: e.target.value }
      });
    }
    onSubmit = e => {
      e.preventDefault();
      const errors = this.validate(this.state.data);
      this.setState({ errors });
      if (Object.keys(errors).length === 0) {
        	console.log(JSON.stringify(this.state.data));
        axios.post('http://34.210.127.92:8000/newconcert/', this.state.data,{
          'Content-Type': 'application/json',
          Authorization: "Bearer " + theToken
          
      }
      ).then((responseJson) => {
          window.open("http://"+window.location.host+"/concert/"+responseJson.data.concert_id,"_self")
      },error=>{
        console.log(error);
        let errorString="";
        for (let name in JSON.parse(error.request.response)){
            errorString+=name+":";
            errorString+=JSON.parse(error.request.response)[name]+"\n";
        }
        alert(errorString);
      }
    );
      }else{
        let errorString="";
        for (let name in errors){
            errorString+=name+":";
            errorString+=errors[name]+"\n";
        }
        alert(errorString);
      }
    };
  
    validate = data => {
      let errors = {};
      if(data.name=="")errors.concert_name="Please enter a concert name.";
      if(data.artist.name=="")errors.artist="Please choose an artist.";
      if(data.date_time=="")errors.date_time="Please select the concert date";
      if(data.location.coordinates=="")errors.location="Please set the venue";

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
      let description=this.state.data['description'];
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
              <div>
              <DayPickerInput onDayChange={this.dayChange}/>
              </div>
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
            <Form.Field>
              <TagForm  tagSelected={this.selectTag} />
            </Form.Field>

          <Button>Create Concert</Button>
        </Form>
      );
    }
  }
  

  ConcertCreationForm.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
}

function mapStateToProps(state) {
    return {
        isAuthenticated: !!state.user.accessToken,
    }
}

export default connect(mapStateToProps)(ConcertCreationForm);
