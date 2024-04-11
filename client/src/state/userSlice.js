// userSlice.js
import { createSlice } from "@reduxjs/toolkit";

export const userSlice = createSlice({
  name: "user",
  initialState: {
    value: null, // Initial state of the user is null
  },
  reducers: {
    setUser: (state, action) => {
      state.value = action.payload; // Set the user state to the payload
    },
    logoutUser: (state) => {
      state.value = null; // Reset the user state to null
    },
    // Add other reducers as needed
  },
});

export const { setUser, logoutUser } = userSlice.actions;

export default userSlice.reducer;
