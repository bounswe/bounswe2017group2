import React from "react";
import PropTypes from "prop-types";
import { Menu, Input, Form, Icon } from "semantic-ui-react";
import { connect } from "react-redux";
import { Link } from "react-router-dom";

// import gravatarUrl from "gravatar-url";
import * as actions from "../../actions/auth";
import setAuthorizationHeader from "../../utils/setAuthorizationHeader";
import axios from "axios";
import logo from './l4clogo1.png';


let input;

const onChange = e => {
  input = e.target.value;
}

const onSubmit = e => {
  console.log(input);
  window.history.pushState({urlPath:'/?search='+input},"",'/?search='+input);
  window.location.reload();
}


const TopNavigation = ({ isAuthenticated, logout }) => (
  <Menu secondary pointing>
    <Menu.Item header as={Link} to="/home">
      <img src={logo}/>
      LookingForConcerts
    </Menu.Item>
    <Menu.Item>
      <Form onSubmit={onSubmit}>
        <Input icon="search" onChange = {onChange} type='text' placeholder='Search..' />
      </Form>
    </Menu.Item>

    <Menu.Menu position="right">
      {isAuthenticated ? (
        <Menu secondary>
          <Menu.Item as={Link} to="/recommended">
            <Icon name="idea" />Recommendations
          </Menu.Item>
          <Menu.Item
            as={Link}
            to="/me"
          >
            Profile
          </Menu.Item>
          <Menu.Item as={Link} to="/createconcert/">
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
  logout: PropTypes.func.isRequired,
  onChange: PropTypes.func.isRequired
};

function mapStateToProps(state) {
  return {
    user: state.user,
    isAuthenticated: !!state.user.access_token
  };
}

export default connect(mapStateToProps, { logout: actions.logout })(
  TopNavigation,
);
