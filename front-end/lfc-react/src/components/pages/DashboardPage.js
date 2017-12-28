import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Image, Label, Icon, Card, Popup } from "semantic-ui-react";
import { fetch } from "../../actions/concert";
import { Link } from "react-router-dom";
import { search, fetchRecommended } from "../../actions/concert";
import "./design.css";

const ConcertItem = ({ concert }) => (
  <Card>
    <Image as={Link} to={"/concert/" + concert.concert_id}
      src={
        concert.artist &&
          concert.artist.images &&
          concert.artist.images[0] &&
          concert.artist.images[0].url
          ? concert.artist.images[0].url
          : ""
      }
    />
    <Card.Content>
      <Card.Header as={Link} to={"/concert/" + concert.concert_id}>
        {" "}
        <div className="concertNameLink">
          {concert.artist ? concert.artist.name : ""}
        </div>
      </Card.Header>
      <Card.Meta>
        <Icon name="calendar" /> {concert.date_time}
      </Card.Meta>
      <Card.Description>
        <div>
          {concert.attendees.length > 0 && (
            <Popup
              basic
              trigger={<div>Attendees:<Icon name="user" /> {concert.attendees.length}</div>}
              content={
                <div style={{ maxHeight: "100px", overflowY: "auto" }} className="ui grid">
                  <div className="sixteen wide column" style={{ padding: "2px" }}>
                    {concert.attendees.map(attendee => (
                      <div className="row" style={{ marginTop: "3px" }}>
                        <Link to={"user/"+attendee.id}>
                          <Label className="fluid" image>
                            <img src={attendee.image} />{attendee.username}
                          </Label>
                        </Link>
                      </div>
                    ))}
                  </div>
                </div>
              }
              on="click"
              style="backgo"
              position="left bottom"
            />
          )}
          {concert.attendees.length == 0 && (
            <div>Attendees: <Icon name="user" /> 0</div>
          )}
        </div>

      </Card.Description>
    </Card.Content>
    <Card.Content extra>
      <Icon name="tag" />
      {concert.location.venue}
    </Card.Content>
  </Card>
);

const ConcertsList = ({ concerts }) => (
  <div className="ui four cards">
    {concerts.length === 0 ? (
      <div className="ui icon message">
        <i className="icon info" />
        <div className="content">
          <div className="header">There are no concerts listed!</div>
          <p>You can create a new concert event</p>
        </div>
      </div>
    ) : (
        concerts.map(concert => (
          <ConcertItem concert={concert} key={concert.concert_id} />
        ))
      )}
  </div>
);

class DashboardPage extends React.Component {
  componentWillMount() {
    // if(this.props.isAuthenticated) {
    // this.props.fetchRecommended();
    // } else {
    // this.props.fetch();
    // }
    this.props.fetch();
    // this.props.fetch();
    // this.props.search("nadia");
  }
  render() {
    const { concerts } = this.props;
    return (
      <div className="ui container">
        <ConcertsList concerts={concerts} />
      </div>
    );
  }
}

ConcertsList.propTypes = {
  concerts: PropTypes.arrayOf(PropTypes.object).isRequired
};

ConcertsList.defaultProps = {
  concerts: [
    {
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
      location: {
        venue: ""
      },
      description: ""
    }
  ]
};

ConcertItem.propTypes = {
  concert: PropTypes.shape({
    name: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    artist: PropTypes.shape({
      name: PropTypes.string.isRequired,
      images: PropTypes.arrayOf(PropTypes.object).isRequired
    }).isRequired,
    location: PropTypes.shape({ venue: PropTypes.string.isRequired }).isRequired
  }).isRequired
};

DashboardPage.propTypes = {
  concerts: PropTypes.arrayOf(PropTypes.object).isRequired,
  recommended: PropTypes.arrayOf(PropTypes.object).isRequired,
  fetch: PropTypes.func.isRequired,
  search: PropTypes.func.isRequired,
  isAuthenticated: PropTypes.bool.isRequired,
  fetchRecommended: PropTypes.func.isRequired

};

function mapStateToProps(state) {
  return {
    concerts: state.concerts,
    isAuthenticated: !!state.user.access_token
  };
}

export default connect(mapStateToProps, { fetch, search, fetchRecommended })(DashboardPage);
