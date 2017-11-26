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
    const user = {
      username: credentials.username,
      accessToken: res.data.access,
      refreshToken: res.data.refresh
    };
    localStorage.lfcJWT = res.data.access; // token -> access and refresh
    setAuthorizationHeader(res.data.access);
    dispatch(userLoggedIn(user));
  });

export const logout = () => dispatch => {
  localStorage.removeItem("lfcJWT");
  setAuthorizationHeader();
  dispatch(userLoggedOut());
};
