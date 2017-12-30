import React from "react";
import PropTypes from "prop-types";
import { Form, Button, Message, Icon } from "semantic-ui-react";
import InlineError from "../messages/InlineError";
import './design.css';

class LoginForm extends React.Component {
  state = {
    data: {
      username: "",
      password: ""
    },
    loading: false,
    errors: {}
  };

  onChange = e =>
    this.setState({
      data: { ...this.state.data, [e.target.name]: e.target.value }
    });

  onSubmit = () => {
    const errors = this.validate(this.state.data);
    this.setState({ errors });
    if (Object.keys(errors).length === 0) {
      this.setState({ loading: true });
      this.props.submit(this.state.data).catch(err =>
        this.setState({
          errors: {
            ...this.state.errors,
            global: err.response.data.non_field_errors
          },
          loading: false
        })
      );
    }
  };

  validate = data => {
    const errors = {};
    if (!data.username) errors.username = "Invalid username";
    if (!data.password) errors.password = "Can't be blank";
    return errors;
  };

  render() {
    const { data, errors, loading } = this.state;

    return (
      <Form onSubmit={this.onSubmit} loading={loading}>
        {errors.global && (
          <Message negative>
            <Message.Header>Something went wrong</Message.Header>
            <p>{errors.global}</p>
          </Message>
        )}
        <Form.Field error={!!errors.username}>
          <div className="ui left icon input">
          <Icon name="user" />
            <input
              name="username"
              value={data.username}
              onChange={this.onChange}
              placeholder= "user name"
            />
          </div> 
          {errors.username && <InlineError text={errors.username} />}
        </Form.Field>
        <Form.Field error={!!errors.password}>
          <div className="ui left icon input">
          <Icon name="lock" />
            <input
              type="password"
              name="password"
              value={data.password}
              onChange={this.onChange}
              placeholder="password"
            />
          </div>
          {errors.password && <InlineError text={errors.password} />}
        </Form.Field>
        <Button fluid>LOG IN</Button>
      </Form>
    );
  }
}

LoginForm.propTypes = {
  submit: PropTypes.func.isRequired
};

export default LoginForm;
