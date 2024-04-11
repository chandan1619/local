import "./App.css";
import AppRouter from "./router";
import { Provider } from "react-redux";
import { store } from "./state/store";
import Modal from "react-modal";
import { setUser } from "./state/userSlice";

// Set the main content element for accessibility
Modal.setAppElement("#root");

function App() {
  const loadUserFromStorage = () => {
    const userJson = localStorage.getItem("user");
    if (userJson) {
      const user = JSON.parse(userJson);
      store.dispatch(setUser(user));
    }
  };

  loadUserFromStorage();
  return (
    <Provider store={store}>
      <AppRouter />
    </Provider>
  );
}

export default App;
