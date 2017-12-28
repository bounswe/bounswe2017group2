import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Grid, Image } from "semantic-ui-react";
import logo from '../../assets/images/logo.png';
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
      <Grid centered columns={2}>

      <Grid.Row> 
        <Grid.Column>
          <Image src={logo} size="medium" centered/> 
        </Grid.Column>
      </Grid.Row>

      <Grid.Row> 
        <Grid.Column>
          <SignupForm submit={this.submit} />   

        </Grid.Column>
      </Grid.Row>  

      </Grid>  
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
