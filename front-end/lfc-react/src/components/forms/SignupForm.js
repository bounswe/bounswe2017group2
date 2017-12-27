import React from "react";
import PropTypes from "prop-types";
import { Form, Button, Message, Icon } from "semantic-ui-react";
import { isEmail, isLength } from "validator";
import InlineError from "..//messages/InlineError";

class SignupForm extends React.Component {
  state = {
    data: {
      username: "",
      email: "",
      password: "",
      first_name: "",
      last_name: ""
    },
    loading: false,
    errors: {}
  };

  onChange = e =>
    this.setState({
      ...this.state,
      data: { ...this.state.data, [e.target.name]: e.target.value }
    });

  onSubmit = e => {
    e.preventDefault();
    const errors = this.validate(this.state.data);
    this.setState({ errors });
    if (Object.keys(errors).length === 0) {
      this.setState({ loading: true });
      this.props.submit(this.state.data).catch(
        err =>
          err.response !== undefined
            ? this.setState({
                errors: {
                  ...this.state.errors,
                  global: err.response.data.username
                },
                loading: false
              })
            : this.setState({
                errors: {
                  ...this.state.errors,
                  global: "Connection Error"
                },
                loading: false
              })
      );
    }
  };

  validate = data => {
    const errors = {};

    if (!isEmail(data.email)) errors.email = "Invalid email";
    if (!data.username) errors.username = "Invalid username";
    if (!data.password || !isLength(data.password, { min: 5, max: 16 }))
      errors.password = "Password should be between 5-16 characters";

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

        <Form.Field error={!!errors.first_name}>
            <input
              name="first_name"
              value={data.first_name}
              onChange={this.onChange}
              placeholder="first name"
            />
          {errors.first_name && <InlineError text={errors.first_name} />}
        </Form.Field>

        <Form.Field error={!!errors.last_name}>
          <label htmlFor="last_name">
            <input
              name="last_name"
              value={data.last_name}
              onChange={this.onChange}
              placeholder="last name"
            />
          </label>
          {errors.last_name && <InlineError text={errors.last_name} />}
        </Form.Field>

        <Form.Field error={!!errors.email}>
          <label htmlFor="email">
            
            <input
              type="email"
              name="email"
              value={data.email}
              onChange={this.onChange}
              placeholder="email"
            />
          </label>
          {errors.email && <InlineError text={errors.email} />}
        </Form.Field>

        <Form.Field error={!!errors.username}>
          <label htmlFor="username">
            
            <input
              name="username"
              value={data.username}
              onChange={this.onChange}
              placeholder="user name"
            />
          </label>
          {errors.username && <InlineError text={errors.username} />}
        </Form.Field>

        <Form.Field error={!!errors.password}>
          <label htmlFor="password">
            
            <input
              type="password"
              id="password"
              name="password"
              value={data.password}
              onChange={this.onChange}
              placeholder="password"
            />
          </label>
          {errors.password && <InlineError text={errors.password} />}
        </Form.Field>

        <Button fluid color='red'>SIGN UP</Button>
      </Form>
    );
  }
}

SignupForm.propTypes = {
  submit: PropTypes.func.isRequired
};

export default SignupForm;
