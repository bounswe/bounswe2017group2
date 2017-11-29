import React from "react";
import PropTypes from "prop-types";
import { Menu, Input, Button } from "semantic-ui-react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import gravatarUrl from "gravatar-url";
import * as actions from "../../actions/auth";

const TopNavigation = ({ isAuthenticated, user, logout }) => (
  <Menu secondary pointing>
    <Menu.Item header as={Link} to="/">
      LookingForConcerts
    </Menu.Item>
    <Menu.Item>
      <Button color="green">Connect to Spotify</Button>
    </Menu.Item>
    <Menu.Item>
      <Input icon="search" placeholder="Search..." />
    </Menu.Item>

    <Menu.Menu position="right">
      {isAuthenticated ? (
        <Menu secondary>
          <Menu.Item as={Link} to="/profile">
            Profile
          </Menu.Item>
          <Menu.Item as={Link} to="/">
            Newsfeed
          </Menu.Item>
          <Menu.Item onClick={() => logout()}>Logout</Menu.Item>
        </Menu>
      ) : (
        <Menu secondary>
          <Menu.Item as={Link} to="/login">
            Login
          </Menu.Item>
          <Menu.Item as={Link} to="/signup">
            Signup
          </Menu.Item>
        </Menu>
      )}
    </Menu.Menu>
  </Menu>
);

TopNavigation.propTypes = {
  isAuthenticated: PropTypes.bool.isRequired,
  logout: PropTypes.func.isRequired
};

function mapStateToProps(state) {
  return {
    user: state.user,
    isAuthenticated: !!state.user.access_token
  };
}

export default connect(mapStateToProps, { logout: actions.logout })(
  TopNavigation
);
