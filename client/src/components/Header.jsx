import React from "react";
import { useSelector } from "react-redux";
import MenuIcon from "./MenuIcon";
import { Link } from "react-router-dom";
const Header = () => {
  const user = useSelector((state) => state.user.value);
  return (
    <header className="flex items-center justify-between bg-violet-400 p-4 text-white">
      <div className="text-2xl font-bold">
        <Link to="/home">Local Assistant</Link>
      </div>
      <div className="flex items-center space-x-4">
        <div className="flex items-center justify-center">
          <span className="text-white-900 mx-2 flex h-10 w-10 items-center justify-center rounded-full bg-black font-bold uppercase">
            {user?.name[0]}
          </span>
        </div>
        <MenuIcon />
      </div>
    </header>
  );
};

export default Header;
