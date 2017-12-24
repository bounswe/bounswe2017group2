/* eslint-disable */
import axios from "axios";
import { FETCH_CONCERTS, SEARCH_CONCERTS } from "../types";

export const fetchConcerts = concerts => ({
  type: FETCH_CONCERTS,
  concerts
});

export const searchConcerts = results => ({
  type: SEARCH_CONCERTS,
  results
})

export const fetch = () => dispatch =>
  axios
    .get("http://34.210.127.92:8000/concerts/")
    .then(res => {
      const concertsArray = Array.from(res.data);
      dispatch(fetchConcerts(concertsArray));
    })
    .catch(() => console.log("Connection Error while fetching concerts!"));

export const search = (searchInput) => dispatch => axios
.get("http://34.210.127.92:8000/concerts/search/?search=" + searchInput)
.then(res => {
  const searchArray = Array.from(res.data);
  dispatch(fetchConcerts(searchArray));
})
.catch(() => console.log("Connection Error while searching concerts!"));