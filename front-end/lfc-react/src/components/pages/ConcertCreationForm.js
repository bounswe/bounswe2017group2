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
class ConcertCreationForm extends React.Component {
    /*state = {
      data: {
        username: "",
        email: "",
        password: "",
        first_name: "",
        last_name: ""
      },
      loading: false,
      errors: {}
    };*/
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
            location: {'venue':'',
                       'coordinates':''},
            image: null,
            seller_url: null
        },
        address: '0.0 0.0',
        venue_name: '',
        loading: false,
        errors: {}
    };
    selectArtist = (artistData) => {
      this.setState({
        ...this.state,
        data: { ...this.state.data, ['artist']: artistData }
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
        const theToken = localStorage.lfcJWT;
        console.log(theToken);
        	console.log(JSON.stringify(this.state.data));
        axios.post('http://34.210.127.92:8000/newconcert/', this.state.data,{
          'Content-Type': 'application/json',
          
      }
      ).then(res =>res.json())
      .then((responseJson) => {
          console.log(responseJson);
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
          <ArtistForm onArtistSelected={this.selectArtist} />
          
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
          selectedArtist:{}
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
      console.log(data);

      axios.get("http://34.210.127.92:8000/searchartists/",{
          params:data
      }
      ).then(resp => {
        console.log(resp.data);
        this.setState({artists:resp.data});
        console.log(this.state.artists);
      }).catch(err => {console.log(err)});

  }
    
  
  
  
  handleClick(e, data){
    this.setState({selectedArtist:this.state.artists[data.value]});
    this.props.onArtistSelected(this.state.selectedArtist);
    console.log(this.state.selectedArtist);
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
  return (
    <div>
    <label>
      Enter artist name: 
      <input type="text" value={this.state.value} onChange={this.handleChange} />
    </label>
    <input type="submit" value="Submit" onClick={this.handleSubmit} />
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
