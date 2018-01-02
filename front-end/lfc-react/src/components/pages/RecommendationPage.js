import React from "react";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { connect } from "react-redux";
import { Image, Icon, Card } from "semantic-ui-react";
import { fetch, search, fetchRecommended } from "../../actions/concert";

const ConcertItem = ({ concert }) => (
  <Card>
    <Image
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
        {concert.artist ? concert.artist.name : ""}
      </Card.Header>
      <Card.Meta>
      <div>
          <Link to={"/concert/" + concert.concert_id} >
        <Icon  name="calendar" /> {concert.date_time}
        </Link>
        </div>
      </Card.Meta>
      <Card.Description>
        Attendees: <Icon name="user" />
        {concert.attendees.length}
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
    this.props.fetchRecommended();
  }
  render() {
    const { concerts, isAuthenticated } = this.props;
    return (
      <div className="ui container">
        {isAuthenticated}
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
