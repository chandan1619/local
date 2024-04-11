// store.js
import { configureStore } from "@reduxjs/toolkit";
import userReducer from "./userSlice"; // We will create this slice in the next step
import { setUser } from "../state/userSlice";
export const store = configureStore({
  reducer: {
    user: userReducer,
  },
});

const loadUserFromStorage = () => {
  const userJson = localStorage.getItem("user");
  if (userJson) {
    const user = JSON.parse(userJson);
    store.dispatch(setUser(user));
  }
};

loadUserFromStorage();
