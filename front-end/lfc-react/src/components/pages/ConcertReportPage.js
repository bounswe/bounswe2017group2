import ReactDOM from 'react-dom';
import axios from 'axios';
import { compose, withProps } from "recompose";
import { GoogleMap, Marker, withScriptjs, withGoogleMap, InfoWindow } from 'react-google-maps';
import { connect } from 'react-redux';
import { Link } from 'react-router-dom';
import{TagForm,ArtistForm,GoogleLocationChooser}from '../forms/ConcertForms.js'
import React from "react";
import PropTypes from "prop-types";
import { Form, Button, Message, Dropdown } from "semantic-ui-react";
import { isEmail, isLength } from "validator";
import DayPickerInput from 'react-day-picker/DayPickerInput';
import 'react-day-picker/lib/style.css';
import InlineError from "..//messages/InlineError";

import decode from "jwt-decode";
const googleMapKey = "AIzaSyCrs1xLdXw8y4rfXc4tiJZZIWcwjmOR7BM";
const theToken = localStorage.lfcJWT;
class SingleReport extends React.Component{
  onApprove=e=>{
    axios
    .post(
    "http://34.210.127.92:8000/concertreport/" +
    this.props.reportID +
    "/upvote/",
    {},{
      'Content-Type': 'application/json',
      Authorization: "Bearer " + theToken      
  }
    )
    .then(
    response => {
        console.log(response);
        if(response.status==200){
          window.location.reload();
        }
    },
    error => {
        console.log(error);
        alert(JSON.parse(error.request.response)['error']);
    }
    );
  }
  onDelete=e=>{
    axios
    .delete(
    "http://34.210.127.92:8000/concertreport/"+this.props.reportID+
    "/delete/",
    {},{
      'Content-Type': 'application/json',
      Authorization: "Bearer " + theToken      
  }
    )
    .then(
    response => {
        console.log(response);
        if(response.status==204){
          window.location.reload();
        }
    },
    error => {
        console.log(error);

        alert(JSON.parse(error.request.response)['error']);
    }
    );
  }
  render(){
    let printString=this.props.suggestion;
    let upvotes=this.props.upvoteCount;
    let reportType=this.props.reportType;
    let reporter=this.props.reporterID;
    if(reporter==decode(localStorage.lfcJWT).user_id)
    return(
      <div>
        {reportType}:{printString} Upvotes:{upvotes}<Button onClick={this.onDelete}>Delete report</Button>
      </div>
      );
    else 
    return(
    <div>
      {reportType}:{printString} Upvotes:{upvotes}<Button onClick={this.onApprove}>Vote up</Button>
    </div>
    );
  }
}
class ReportForm extends React.Component{
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
        this.props.onSubmit(this.state.data);
    };
  
    validate = data => {
      const errors = {};
  

      return errors;
    };
  
    render() {
      const { data, errors, loading } = this.state;
      let lat,lng,venue_name;
      let reportType=this.props.type;
      if(this.state.data.location.venue==null){
        venue_name=null;
      }else{
        lat=this.state.data.location.coordinates.substring(0,this.state.data.location.coordinates.indexOf(" "));
        lng=this.state.data.location.coordinates.substring(this.state.data.location.coordinates.indexOf(" ")+1,this.state.data.location.coordinates.length);
        venue_name=this.state.data.location.venue;
      }
      let description=this.state.data['description'];
      let formField=(
          <div></div>
      );
      if(reportType==1)formField=(<Form.Field>
        <label htmlFor="name">
          Concert Name
          <input
            name="name"
            value={data.name}
            onChange={this.onChange}
          />
        </label>
        
      </Form.Field>);
      if(reportType==2)formField=(
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
      );
      if(reportType==3)formField=(
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

      );
      if(reportType==4)formField=(        
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
      );
      if(reportType==5)formField=(          
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
        );
        if(reportType==8)formField=(              
          <Form.Field>
          <label htmlFor="date_time">
            Date
            <div>
            <DayPickerInput onDayChange={this.dayChange}/>
            </div>
          </label>
        </Form.Field>
        );
        if(reportType==6)formField=(
            <Form.Field>
            <div>
            <GoogleLocationChooser onChange={this.selectVenue}/> 
            </div>
            </Form.Field>
        );
        if(reportType==7)formField=(
            <Form.Field>
            <ArtistForm onArtistSelected={this.selectArtist} />
            </Form.Field>
        );
        if(reportType==9)formField=(  
            <Form.Field>
              <TagForm  tagSelected={this.selectTag} />
            </Form.Field>
        );
        
      return (
        <Form onSubmit={this.onSubmit} loading={loading}>
          {errors.global && (
            <Message negative>
              <Message.Header>Something went wrong</Message.Header>
              <p>{errors.global}</p>
            </Message>
          )} 
          {formField}
          <Button>Suggest this change</Button>
        </Form>
      );
    }
}
class ConcertReportPage extends React.Component {
    state= {
        reportType:0,
        data:"",
        loading: false,
        reports:[],
        errors: {}
    };
  

    submitReport=data=>{
        let reportTypeToSubmit=this.state.reportType;
        let reportTypeString;
        let reportString;
        if(reportTypeToSubmit==1){
            reportTypeString="NAME";
            reportString=data.name;
        }
        if(reportTypeToSubmit==2){
          reportTypeString="DESCRIPTION";
          reportString=data.description;
        }if(reportTypeToSubmit==3){
          reportTypeString="MIN_PRICE";
          reportString=data.price_min;
        }if(reportTypeToSubmit==4){
          reportTypeString="MAX_PRICE";
          reportString=data.price_max;
        }if(reportTypeToSubmit==5){
          reportTypeString="SELLER_URL";
          reportString=data.seller_url;
        }if(reportTypeToSubmit==6){
          reportTypeString="LOCATION";
          reportString=JSON.stringify(data.location);
        }if(reportTypeToSubmit==7){
          reportTypeString="ARTIST";
          reportString=JSON.stringify(data.artist);
        }if(reportTypeToSubmit==8){
          reportTypeString="DATE_TIME";
          reportString=data.date_time;
        }
        axios
                .post(
                "http://34.210.127.92:8000/concert/" +
                this.props.match.params.concertID +
                "/report/",
                {
                    report_type: reportTypeString,
                    suggestion: reportString
                },{
                  'Content-Type': 'application/json',
                  Authorization: "Bearer " + theToken
                  
              }
                )
                .then(
                response => {
                    console.log(response);
                    if(response.status==200){
                      window.location.reload();
                    }
                },
                error => {
                    console.log(error);
                    let errorString="";
                    for (let name in JSON.parse(error.request.response)){
                        errorString+=name+":";
                        errorString+=JSON.parse(error.request.response)[name]+"\n";
                    }
                    alert(errorString);
                }
                );
    };
    validate = data => {
      const errors = {};
      return errors;
    };
    typeChanged=(e, data)=>{
        let index=data.value;
        this.setState({reportType:index});
      };
     getSuggestion(report_type,suggestion){
      if(report_type=="LOCATION"){
        let locationObj=JSON.parse(suggestion);
        return locationObj['venue'];
      }
      if(report_type=="ARTIST"){
        let artistObj=JSON.parse(suggestion);
        return artistObj['name'];
      }
      return suggestion;
      };
      getReportType(report_type){
          if(report_type=="MIN_PRICE")return "MINUMUM TICKET PRICE";
          if(report_type=="MAX_PRICE")return "MAXIMUM TICKET PRICE";
          if(report_type=="SELLER_URL")return "TICKET SELLER URL";
          if(report_type=="DATE_TIME")return "CONCERT DATE";
          return report_type;
      };
      componentWillMount(){
        let reportsOfThisConcert=[];
      let concertID=this.props.match.params.concertID;
      axios.get("http://34.210.127.92:8000/concertreports/").then(
        response => {
            reportsOfThisConcert=reportsOfThisConcert.concat(response.data.filter(function (item){
              let thisConcert=false;
              if(item['concert']==concertID){
                thisConcert=true;
                return thisConcert;
              }
              return thisConcert;
            }
            ));
          this.setState({reports:reportsOfThisConcert});
        }, error => {});

      };
    render() {
      const { data, errors, loading } = this.state;
      let reportOptions=[{
          text:"Concert Name",
          value:1,
      },
      {
        text:"Description",
        value:2,
    },{
        text:"Minimum Price",
        value:3,
    },{
        text:"Maximum Price",
        value:4
    },{
        text:"Seller URL",
        value:5
    },{
        text:"Venue",
        value:6
    },{
        text:"Artist",
        value:7
    },{
        text:"Date",
        value:8
    }
      ];
      let reportList= this.state.reports.map(report => (
        <div>
        <p></p>
        <SingleReport reportID={report['concert_report_id']} suggestion={this.getSuggestion(report['report_type'],report['suggestion'])} upvoteCount={report['upvoters'].length} reportType={this.getReportType(report['report_type'])} reporterID={report['reporter']} />
        </div>              
    ));
      return (
          <div>
          <Dropdown onChange={this.typeChanged}placeholder="Select Information to Report" fluid selection options={reportOptions}/>
          <ReportForm type={this.state.reportType} onSubmit={this.submitReport}/>
          {reportList}
          </div>
      );
    }
  }
  ConcertReportPage.propTypes = {
    isAuthenticated: PropTypes.bool.isRequired,
}

function mapStateToProps(state) {
    return {
        isAuthenticated: !!state.user.accessToken,
    }
}

export default connect(mapStateToProps)(ConcertReportPage);
