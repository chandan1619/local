import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import Home from "./pages/Home";
import { useSelector } from "react-redux";
import Chat from "./pages/Chat";
import AccountSettings from "./pages/AccountSettings";

const AppRouter = () => {
  const user = useSelector((state) => state.user.value);

  return (
    <Router>
      <Routes>
        {user ? (
          <>
            <Route path="/*" element={<Home />} />
            <Route path="/home/*" element={<Home />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/chat/:id" element={<Chat />} />
            <Route path="/accountsettings" element={<AccountSettings />} />
          </>
        ) : (
          <Route path="/*" element={<LoginPage />} />
        )}
      </Routes>
    </Router>
  );
};

export default AppRouter;
