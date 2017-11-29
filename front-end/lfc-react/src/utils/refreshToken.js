import axios from "axios";

// TODO: Sofu => refresh access token
export default (accessToken, refreshToken) => {
  axios
    .post("http://34.210.127.92:8000/api/auth/token/verify/", {
      token: { accessToken }
    })
    .then(() => return accessToken;).
    catch(
        axios.post("http://34.210.127.92:8000/api/auth/token/refresh/", {token: {refreshToken}}).then(res => {
            return res.data.access;
        });
    );
};

