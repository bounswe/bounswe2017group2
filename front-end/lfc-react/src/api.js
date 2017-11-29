import axios from "axios";

export default {
  user: {
    login: credentials =>
      axios
        .post("http://34.210.127.92:8000/api/auth/token/obtain/", {
          username: credentials.username,
          password: credentials.password
        })
        .then(res => res.data),
    signup: user =>
      axios
        .post("http://34.210.127.92:8000/signup/", {
          username: user.username,
          password: user.password,
          first_name: user.first_name,
          last_name: user.last_name,
          email: user.email
        })
        .then(res => res.data)
  }
};
