import React from "react";
import PropTypes from "prop-types";
import { Form, Button, Message } from "semantic-ui-react";
import isEmail from "validator/lib/isEmail";
import InlineError from "../messages/InlineError";

class SignupForm extends React.Component {
  state = {
    data: {
      username: "",
      email: "",
      password: "",
      first_name: "",
      last_name: "",
      birth_date: null,
      avatar: null
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
      this.props.submit(this.state.data).catch(err =>
        this.setState({
          errors: {
            ...this.state.errors,
            global: err.response.data.username
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

        <Form.Group widths={1}>
          <Form.Input label="First name">
            <input
              name="first_name"
              value={data.first_name}
              onChange={this.onChange}
            />
          </Form.Input>
          <Form.Input label="Last name">
            <input
              name="last_name"
              value={data.last_name}
              onChange={this.onChange}
            />
          </Form.Input>
        </Form.Group>

        <Form.Field error={!!errors.username} width={5}>
          <label htmlFor="username">
            User name
            <input
              name="username"
              value={data.username}
              onChange={this.onChange}
            />
          </label>
          {errors.username && <InlineError text={errors.username} />}
        </Form.Field>

        <Form.Field error={!!errors.email} width={5}>
          <label htmlFor="email">
            Email
            <input
              type="email"
              name="email"
              value={data.email}
              onChange={this.onChange}
            />
          </label>
          {errors.email && <InlineError text={errors.email} />}
        </Form.Field>

        <Form.Field error={!!errors.password} width={5}>
          <label htmlFor="password">
            Password
            <input
              type="password"
              id="password"
              name="password"
              value={data.password}
              onChange={this.onChange}
            />
          </label>
          {errors.password && <InlineError text={errors.password} />}
        </Form.Field>

        <Button primary>Sign Up</Button>
      </Form>
    );
  }
}

SignupForm.propTypes = {
  submit: PropTypes.func.isRequired
};

export default SignupForm;
