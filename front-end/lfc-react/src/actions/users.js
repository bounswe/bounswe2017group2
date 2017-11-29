import api from "../api";
// import axios from "axios";
import { USER_SIGNED_UP } from "../types";

export const userSignedUp = () => ({
  type: USER_SIGNED_UP
});

export const signup = data => dispatch =>
  api.user.signup(data).then(() => {
    dispatch(userSignedUp);
  });
