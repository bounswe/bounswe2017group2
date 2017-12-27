import { FETCH_CONCERTS, SEARCH_CONCERTS, FETCH_RECOM } from "../types";

export default function concert(state = {}, action = {}) {
  switch (action.type) {
    case FETCH_CONCERTS:
      return action.concerts;
    case SEARCH_CONCERTS:
      return action.results;
    case FETCH_RECOM:
      return action.recommended;
    default:
      return state;
  }
}
