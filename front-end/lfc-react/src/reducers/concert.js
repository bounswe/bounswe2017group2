import { FETCH_CONCERTS } from "../types";

export default function concert(state = {}, action = {}) {
  switch (action.type) {
    case FETCH_CONCERTS:
      return action.concerts;
    default:
      return state;
  }
}
