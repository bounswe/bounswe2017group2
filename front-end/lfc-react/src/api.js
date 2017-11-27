import axios from "axios";

export default {
  user: {
    login: credentials =>
      axios.post("http://34.210.127.92:8000/api/auth/token/obtain/", {
        username: credentials.username,
        password: credentials.password
      }),
    signup: user =>
      axios
        .post("http://34.210.127.92:8000/signup/", {
          username: user.username,
          email: user.email,
          password: user.password
        })
        .then(res => res.data)
  }
};
