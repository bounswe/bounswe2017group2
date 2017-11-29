import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Image as ImageComponent, Item, Label } from "semantic-ui-react";
import { fetch } from "../../actions/concert";
import { Link } from 'react-router-dom';

const ConcertItem = ({ concert }) => (
  <Item>
    <Item.Image src={concert.artist ? concert.artist.images[2].url : ""} />
    {console.log(concert.artist)}
    <Item.Content>
      <Item.Header as={Link} to={"/concert/" + concert.concert_id}>
        {concert.artist ? concert.artist.name : ""}
      </Item.Header>
      <Item.Meta>
        <span className="cinema">{concert.location.venue}</span>
      </Item.Meta>
      <Item.Description>{concert.description}</Item.Description>
      <Item.Extra>
        <Label>{concert.name}</Label>
      </Item.Extra>
    </Item.Content>
  </Item>
);

const ConcertsList = ({ concerts }) => (
  <Item.Group divided>
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
  </Item.Group>
);

class DashboardPage extends React.Component {
  componentWillMount() {
    this.props.fetch();
  }
  render() {
    const { concerts } = this.props;
    console.log(concerts);
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
  fetch: PropTypes.func.isRequired
};

function mapStateToProps(state) {
  return {
    concerts: state.concerts
  };
}

export default connect(mapStateToProps, { fetch })(DashboardPage);
