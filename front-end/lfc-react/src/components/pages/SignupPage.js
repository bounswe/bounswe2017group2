import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import SignupForm from "../forms/SignupForm";
import { signup } from "../../actions/users";
import { login } from "../../actions/auth";

class SignupPage extends React.Component {
  submit = data =>
    this.props
      .signup(data)
      .then(() =>
        this.props.login(data).then(() => this.props.history.push("/home"))
      );

  render() {
    return (
      <div>
        <h2>Signup</h2>

        <SignupForm submit={this.submit} />
      </div>
    );
  }
}

SignupPage.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired
  }).isRequired,
  signup: PropTypes.func.isRequired,
  login: PropTypes.func.isRequired
};

export default connect(null, { signup, login })(SignupPage);
