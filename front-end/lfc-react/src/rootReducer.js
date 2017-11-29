import { combineReducers } from "redux";

import user from "./reducers/user";
import concerts from "./reducers/concert";

export default combineReducers({
  user,
  concerts
});
