import React from "react";
import PropTypes from "prop-types";
import { Menu, Input, Button, Form } from "semantic-ui-react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";
import decode from "jwt-decode";
// import gravatarUrl from "gravatar-url";
import * as actions from "../../actions/auth";

const TopNavigation = ({ isAuthenticated, logout }) => (
  <Menu secondary pointing>
    <Menu.Item header as={Link} to="/home">
      LookingForConcerts
    </Menu.Item>
    <Menu.Item>
      <Button color="green">Connect to Spotify</Button>
    </Menu.Item>
    <Menu.Item>
      <Form onSubmit={this.onSubmit}>
        <Input icon="search" placeholder="Search..." />
      </Form>
    </Menu.Item>

    <Menu.Menu position="right">
      {isAuthenticated ? (
        <Menu secondary>
          <Menu.Item
            as={Link}
            to={"/user/" + decode(localStorage.lfcJWT).user_id + "/"}
          >
            Profile
          </Menu.Item>
          <Menu.Item as={Link} to="/">
            Create a Concert
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
