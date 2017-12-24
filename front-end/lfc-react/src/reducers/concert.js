import { FETCH_CONCERTS, SEARCH_CONCERTS } from "../types";

export default function concert(state = {}, action = {}) {
  switch (action.type) {
    case FETCH_CONCERTS:
      return action.concerts;
    case SEARCH_CONCERTS:
      return action.results;
    default:
      return state;
  }
}
