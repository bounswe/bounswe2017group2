/* eslint-disable */

import React from "react";
import ReactDOM from "react-dom";
import axios from "axios";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import "./design.css";
import decode from "jwt-decode";
import { Modal, Button } from "semantic-ui-react";

let theToken = localStorage.getItem("lfcJWT");
let userID;
let isLoggedIn = false;
let profileID;
let spotifyProfile;

class MiniConcertDetail extends React.Component {
  constructor(props) {
    super(props);
    this.handleRemove = this.handleRemove.bind(this);
  }
  render() {
    let removeButton;
    if (this.props.isCurrentUser) {
      removeButton = (
        <button
          className=" circular mini ui icon right floated button"
          onClick={() => this.handleRemove()}
        >
          <i className="remove icon" />
        </button>
      );
    }
    return (
      <div className="ui grid segment">
        <img
          className="ui image three wide column"
          height="100px"
          src={this.props.concert.artist.images[0].url}
        />
        <div className="ten wide column">
          <h3>
            <Link
              className="Link"
              to={"/concert/" + this.props.concert.concert_id}
            >
              {this.props.concert.name}
            </Link>
          </h3>
          <h4>
            {this.props.concert.date_time} {this.props.concert.location.venue}
          </h4>
        </div>
        <div className="three wide column">{removeButton}</div>
      </div>
    );
  }

  handleRemove(event) {
    axios
      .post(
      "http://34.210.127.92:8000/concert/" +
      this.props.concert.concert_id +
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

export class MiniUserDetail extends React.Component {
  constructor(props) {
    super(props);
    this.handleRemove = this.handleRemove.bind(this);
    this.refreshPage = this.refreshPage.bind(this);
  }
  render() {
    let removeButton;
    if (this.props.isRemovable) {
      removeButton = (
        <button
          className=" circular mini ui icon right floated button"
          onClick={() => this.handleRemove()}
        >
          <i className="remove icon" />
        </button>
      );
    }
    return (
      <div className="ui eight wide column miniUser">
        <div className="ui grid segment">
          <img
            className="ui image three wide column"
            height="100px"
            src={"http://34.210.127.92:8000" + this.props.user.image}
          />
          <div className="ten wide column">
            <h3>
              <Link
                className="Link"
                to={"/user/" + this.props.user.id}
                onClick={this.refreshPage}
              >
                {this.props.user.username}
              </Link>
            </h3>
            <h4>
              {this.props.user.first_name} {this.props.user.last_name}
            </h4>
          </div>
          <div className="three wide column">{removeButton}</div>
        </div>
      </div>
    );
  }

  refreshPage() {
    window.location.reload();
  }

  handleRemove(event) {
    axios
      .post(
      "http://34.210.127.92:8000/user/" + this.props.user.id + "/unfollow/",
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

class ProfilePage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      user: {
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        birth_date: "",
        age: 0,
        comments: [],
        concerts: [],
        date_joined: "",
        followers: [],
        following: []
      },
      willAttend: [],
      attended: [],
      accessToken: theToken,
      reportText: ""
    };
    this.handleTab = this.handleTab.bind(this);
    this.handleFollow = this.handleFollow.bind(this);
    this.handleSpotifyConnect = this.handleSpotifyConnect.bind(this);
    this.handleSpotifyDisconnect = this.handleSpotifyDisconnect.bind(this);
    this.handleReportChange = this.handleReportChange.bind(this);
    this.handleReport = this.handleReport.bind(this);
  }

  handleReportChange(event) {
    this.setState({
      reportText: event.target.value
    });
  }

  handleReport() {
    console.log(this.state.reportText);
    axios
      .post(
      "http://34.210.127.92:8000/user/" + profileID + "/report/",
      {
        "reason": this.state.reportText
      }
      )
      .then(
      response => {
        window.location.reload();
      },
      error => {
        console.log(error);
      }
      );
  }

  handleSpotifyConnect() {
    axios
      .post(
      "http://34.210.127.92:8000/user/spotify/authorize/",
      { "redirect_type": "frontend" }
      )
      .then(
      response => {
        window.location.href = response.data.url;
      },
      error => {
        console.log(error);
      }
      );
  }

  handleSpotifyDisconnect() {
    axios
      .post(
      "http://34.210.127.92:8000/user/spotify/disconnect/",
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
  }

  handleFollow(isFollow) {
    if (isFollow) {
      axios
        .post(
        "http://34.210.127.92:8000/user/" +
        profileID +
        "/follow/",
        {},
        {
          "Content-Type": "application/json",
          Authorization: "Bearer " + theToken
        }
        )
        .then(response => {
          window.location.reload();
        });
    } else {
      axios
        .post(
        "http://34.210.127.92:8000/user/" +
        profileID +
        "/unfollow/",
        {},
        {
          "Content-Type": "application/json",
          Authorization: "Bearer " + theToken
        }
        )
        .then(response => {
          window.location.reload();
        });
    }
  }

  removeActive(tabName) {
    if (document.getElementById(tabName).classList.contains("active")) {
      document.getElementById(tabName).classList.remove("active");
      document.getElementById(tabName + "Tab").classList.remove("active");
    }
  }

  handleTab(tabName) {
    this.removeActive("concerts");
    this.removeActive("generalInfo");
    this.removeActive("followedUsers");
    this.removeActive("followers");
    document.getElementById(tabName).classList.add("active");
    document.getElementById(tabName + "Tab").classList.add("active");
  }

  componentWillMount() {
    axios.get("http://34.210.127.92:8000/user/spotify/profile/").then(
      response => {
        spotifyProfile = null;
        if (response.status == 200) {
          spotifyProfile = response.data;
        }
      },
      error => {
        console.log("refresh user");
      }
    );

    if (localStorage.getItem("lfcJWT")) {
      userID = decode(localStorage.lfcJWT).user_id;
      isLoggedIn = true;
    }

    if (this.props.match.params.userID) {
      profileID = this.props.match.params.userID;
    }
    else {
      profileID = userID;
    }

    let params = require('query-string').parse(this.props.location.search);
    if (params.code) {
      axios
        .post(
        "http://34.210.127.92:8000/user/spotify/connect/",
        {
          "code": params.code,
          "state": params.state,
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

    axios.get("http://34.210.127.92:8000/user/" + profileID + "/").then(
      response => {
        var userData = response.data;
        var willAttendList = [];
        var attendedList = [];
        axios
          .get(
          "http://34.210.127.92:8000/user/" + profileID + "/get_concerts/",
          {
            "Content-Type": "application/json",
            Authorization: "Bearer " + theToken
          }
          )
          .then(
          response => {
            for (let concert of response.data) {
              let dateOfConcert = new Date(concert.date_time);
              if (dateOfConcert > Date.now()) willAttendList.push(concert);
              else attendedList.push(concert);
            }

            this.setState({
              willAttend: willAttendList,
              attended: attendedList
            });
          },
          error => {
            console.log("refresh concert");
          }
          );
        this.setState({
          user: userData
        });
      },
      error => {
        console.log("refresh user");
      }
    );
  }

  render() {

    let editFollowButton;
    let spotifyReportButton
    let followedUsersList = this.state.user.following.map(usr => (
      <MiniUserDetail
        user={usr}
        isRemovable={isLoggedIn && userID == profileID}
      />
    ));
    let followersList = this.state.user.followers.map(usr => (
      <MiniUserDetail user={usr} isRemovable={false} />
    ));

    if (isLoggedIn) {
      if (userID == profileID) {
        editFollowButton = (
          <Link className="Link" to={"/EditProfile/"}>
            <button className="ui button">Edit Profile</button>
          </Link>
        );
        if (!spotifyProfile) {
          spotifyReportButton = (
            <button className="ui icon right floated button" onClick={() => this.handleSpotifyConnect()}>
              <i className="spotify icon"></i>Connect
          </button>
          )
        }
        else {
          spotifyReportButton = (
            <button className="ui icon right floated button" onClick={() => this.handleSpotifyDisconnect()}>
              <i className="spotify icon"></i>Disconnect
          </button>
          )
        }
      } else {
        spotifyReportButton = (
          <Modal trigger={<Button>Report</Button>}>
            <Modal.Header>Report User</Modal.Header>
            <Modal.Content>
              <div className="ui form">
                <div className="field">
                  <textarea
                    placeholder="Write a reason..."
                    value={this.state.reportText}
                    onChange={this.handleReportChange}
                  ></textarea>
                </div>
                <button className="ui button" onClick={() => this.handleReport()}>Report</button>
              </div>
            </Modal.Content>
          </Modal>
        );
        if (
          !this.state.user.followers.find(function (user) {
            return user.id === userID;
          })
        ) {
          editFollowButton = (
            <button
              className="ui floated button"
              onClick={() => this.handleFollow(1)}
            >
              Follow
            </button>
          );
        } else {
          editFollowButton = (
            <button
              className="ui  floated button"
              onClick={() => this.handleFollow(0)}
            >
              Unfollow
            </button>
          );
        }
      }
    }
    var attendedConcerts = this.state.attended.map(cncrt => (
      <MiniConcertDetail
        concert={cncrt}
        isCurrentUser={isLoggedIn && userID == profileID}
      />
    ));
    var willAttendConcerts = this.state.willAttend.map(cncrt => (
      <MiniConcertDetail
        concert={cncrt}
        isCurrentUser={isLoggedIn && userID == profileID}
      />
    ));
    var age = Math.floor(
      (Date.now() - new Date(this.state.user.birth_date)) /
      (1000 * 60 * 60 * 24 * 365)
    );

    let spotifyData;

    if (spotifyProfile && userID == profileID) {
      spotifyData = (
        <div className="item userData">
          <b>spotify name</b> &nbsp; {spotifyProfile.display_name}
        </div>)
    }

    return (
      <div className="ui grid" id="profilePage">
        <div className="row">
          <img
            className="ui image two wide column"
            height="130px"
            src={"http://34.210.127.92:8000" + this.state.user.image}
          />
          <div className="ten wide column">
            <div className="ui grid">
              <div className="row usersName">
                {this.state.user.first_name + " " + this.state.user.last_name}
              </div>
              <div className="row username">
                <b>username</b> &nbsp; {this.state.user.username}
              </div>
              <div className="row followCounters">
                <b>followers</b> &nbsp; {this.state.user.followers.length}{" "}
                &nbsp; <b>following</b> &nbsp;{" "}
                {this.state.user.following.length}
              </div>
            </div>
          </div>
          <div className="two wide column">{spotifyReportButton}</div>
          <div className="two wide column">{editFollowButton}</div>
        </div>
        <div className="row">
          <div className="ui top attached tabular menu">
            <a
              className="active item"
              id="concerts"
              onClick={() => this.handleTab("concerts")}
            >
              {" "}
              Concerts
            </a>
            <a
              className="item"
              id="generalInfo"
              onClick={() => this.handleTab("generalInfo")}
            >
              General Information
            </a>
            <a
              className="item"
              id="followedUsers"
              onClick={() => this.handleTab("followedUsers")}
            >
              {" "}
              Followed Users
            </a>
            <a
              className="item"
              id="followers"
              onClick={() => this.handleTab("followers")}
            >
              {" "}
              Followers
            </a>
          </div>
          <div
            className="ui bottom attached active tab segment"
            id="concertsTab"
          >
            <div className="ui grid">
              <div className="eight wide column center">
                <h3>Future Concerts</h3>
                {willAttendConcerts}
              </div>
              <div className="eight wide column center">
                <h3>Concert History</h3>
                {attendedConcerts}
              </div>
            </div>
          </div>
          <div className="ui bottom attached tab segment" id="generalInfoTab">
            <div className="ui list">
              <div className="item userData">
                <b>e-mail</b> &nbsp; {this.state.user.email}
              </div>
              <div className="item userData">
                <b>birth date</b> &nbsp; {this.state.user.birth_date}
              </div>
              <div className="item userData">
                <b>comments</b> &nbsp; {this.state.user.comments.length}
              </div>
              <div className="item userData">
                <b>concerts</b> &nbsp; {this.state.user.concerts.length}
              </div>
              {spotifyData}
            </div>
          </div>
          <div className="ui bottom attached tab segment" id="followedUsersTab">
            <div className="ui grid center">{followedUsersList}</div>
          </div>
          <div className="ui bottom attached tab segment" id="followersTab">
            <div className="ui grid center">{followersList}</div>
          </div>
        </div>
      </div>
    );
  }
}

ProfilePage.propTypes = {
  isAuthenticated: PropTypes.bool.isRequired
};

function mapStateToProps(state) {
  return {
    isAuthenticated: !!state.user.accessToken
  };
}

export default connect(mapStateToProps)(ProfilePage);
