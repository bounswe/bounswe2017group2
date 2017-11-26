/* eslint-disable */

import api from "../api";
import { login } from "./auth";

export const signup = data => dispatch =>
  api.user.signup(data).then(user => {
    this.props.login(user);
  });
