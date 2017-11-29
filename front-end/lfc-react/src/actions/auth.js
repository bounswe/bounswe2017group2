import axios from "axios";
import { USER_LOGGED_IN, USER_LOGGED_OUT } from "../types";
import api from "../api";
import setAuthorizationHeader from "../utils/setAuthorizationHeader";

export const userLoggedIn = user => ({
  type: USER_LOGGED_IN,
  user
});

export const userLoggedOut = () => ({
  type: USER_LOGGED_OUT
});

export const login = credentials => dispatch =>
  api.user.login(credentials).then(res => {
    setAuthorizationHeader(res.access);
    const accessToken = res.access;
    const refreshToken = res.refresh;
    axios
      .get("http://34.210.127.92:8000/user/me/")
      .then(res => {
        const user = {
          username: res.data.username,
          email: res.data.email,
          first_name: res.data.first_name,
          last_name: res.data.last_name,
          access_token: accessToken,
          refresh_token: refreshToken
        };
        localStorage.lfcJWT = user.access_token;
        dispatch(userLoggedIn(user));
      })
      .catch(err => {
        console.log("There is an error with /user/me endpoint: " + err.data);
      });
  });

export const logout = () => dispatch => {
  localStorage.removeItem("state");
  localStorage.removeItem("lfcJWT");
  setAuthorizationHeader();
  dispatch(userLoggedOut());
};
