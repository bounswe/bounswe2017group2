import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { Grid, Image } from "semantic-ui-react";
import logo from './logo.png';
import LoginForm from "../forms/LoginForm";
import { login } from "../../actions/auth";

class LoginPage extends React.Component {
  submit = data =>
    this.props.login(data).then(() => this.props.history.push("/home"));

  render() {
    return (
      <Grid centered columns={2}>

      <Grid.Row> 
        <Grid.Column>
          <Image src={logo} size="small" centered/> 
        </Grid.Column>
      </Grid.Row>

      <Grid.Row> 
        <Grid.Column>
          <LoginForm submit={this.submit} />   

        </Grid.Column>
      </Grid.Row>  

      </Grid>  

    );
  }
}

LoginPage.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired
  }).isRequired,
  login: PropTypes.func.isRequired
};

export default connect(null, { login })(LoginPage);
