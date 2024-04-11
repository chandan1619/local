import React from "react";
import { logoutUser } from "../state/userSlice";
import { useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";

const DropdownMenu = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  return (
    <div className="origin-top-right absolute right-0 mt-2 w-52 bg-indigo-300 rounded-md shadow-lg ring-1 ring-black ring-opacity-5">
      <div
        className="py-4 text-center"
        role="menu"
        aria-orientation="vertical"
        aria-labelledby="options-menu"
      >
        {/* Dropdown items */}
        <Link to="/accountsettings" className="text-black hover:text-red-500">
          Account Setting
        </Link>
        <a
          href="#"
          className="block px-4 py-2 text-black hover:text-red-500"
          role="menuitem"
        >
          <button
            className=""
            onClick={() => {
              localStorage.clear("user");
              dispatch(logoutUser());
              navigate("/");
            }}
          >
            Logout
          </button>
        </a>
      </div>
    </div>
  );
};

export default DropdownMenu;
