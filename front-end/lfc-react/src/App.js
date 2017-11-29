import React from "react";
import { connect } from "react-redux";
import PropTypes from "prop-types";
import { Route } from "react-router-dom";
// import HomePage from "./components/pages/HomePage";
import LoginPage from "./components/pages/LoginPage";
import DashboardPage from "./components/pages/DashboardPage";
import ConcertDetailPage from "./components/pages/ConcertDetailPage/ConcertDetailPage";
import ProfilePage from "./components/pages/ProfilePage/ProfilePage";
import SignupPage from "./components/pages/SignupPage";
// import UserRoute from "./components/routes/UserRoute";
import GuestRoute from "./components/routes/GuestRoute";
import TopNavigation from "./components/navigation/TopNavigation";

const App = ({ location, isAuthenticated }) => (
  <div className="ui container">
    <TopNavigation />
    <Route location={location} path="/" exact component={DashboardPage} />
    <Route location={location} path="/concert/:concertID/" exact component={ConcertDetailPage} />
    <Route location={location} path="/user/:userID/" exact component={ProfilePage} />
    <GuestRoute location={location} path="/login" exact component={LoginPage} />
    <GuestRoute
      location={location}
      path="/signup"
      exact
      component={SignupPage}
    />
  </div>
);

App.propTypes = {
  location: PropTypes.shape({
    pathname: PropTypes.string.isRequired
  }).isRequired,
  isAuthenticated: PropTypes.bool.isRequired
};

function mapStateToProps(state) {
  return {
    isAuthenticated: !!state.user.access_token
  };
}

export default connect(mapStateToProps)(App);
