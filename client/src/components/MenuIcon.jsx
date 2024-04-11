import DropdownMenu from "./DropdownMenu";
import { useState, useRef, useEffect } from "react";

const MenuIcon = () => {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef(null);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleClickOutside = (event) => {
    if (menuRef.current && !menuRef.current.contains(event.target)) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("click", handleClickOutside);
    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  }, []);
  return (
    <div className="relative inline-block text-left" ref={menuRef}>
      <div>
        <button
          type="button"
          onClick={toggleMenu}
          className="inline-flex justify-center w-full rounded-md  shadow-sm px-4 py-2 bg-transparent text-sm font-medium text-gray-700 hover:bg-indigo-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-100"
          id="options-menu"
          aria-haspopup="true"
          aria-expanded="true"
        >
          <svg
            className="cursor-pointer"
            onClick={toggleMenu}
            id="Menus"
            enableBackground="new 0 0 512 512"
            height="40"
            viewBox="0 0 512 512"
            width="40"
            xmlns="http://www.w3.org/2000/svg"
          >
            <g>
              <g fill="#213250">
                <path d="m153.825 178.172h303.222c21.715 0 39.382-17.667 39.382-39.382s-17.667-39.382-39.382-39.382h-303.222c-21.715 0-39.382 17.667-39.382 39.382s17.667 39.382 39.382 39.382zm0-58.764h303.222c10.688 0 19.382 8.695 19.382 19.382 0 10.688-8.694 19.382-19.382 19.382h-303.222c-10.687 0-19.382-8.695-19.382-19.382s8.695-19.382 19.382-19.382z" />
                <path d="m457.047 333.828h-303.222c-21.715 0-39.382 17.667-39.382 39.382s17.667 39.382 39.382 39.382h303.222c21.715 0 39.382-17.667 39.382-39.382s-17.667-39.382-39.382-39.382zm0 58.764h-303.222c-10.687 0-19.382-8.694-19.382-19.382s8.695-19.382 19.382-19.382h303.222c10.688 0 19.382 8.694 19.382 19.382s-8.695 19.382-19.382 19.382z" />
                <path d="m457.047 216.618h-303.222c-21.715 0-39.382 17.667-39.382 39.382s17.667 39.382 39.382 39.382h303.222c21.715 0 39.382-17.667 39.382-39.382s-17.667-39.382-39.382-39.382zm0 58.764h-303.222c-10.687 0-19.382-8.694-19.382-19.382 0-10.687 8.695-19.382 19.382-19.382h303.222c10.688 0 19.382 8.695 19.382 19.382 0 10.688-8.695 19.382-19.382 19.382z" />
              </g>
              <path
                d="m54.953 99.408c-21.715 0-39.382 17.667-39.382 39.382s17.667 39.382 39.382 39.382 39.382-17.667 39.382-39.382-17.667-39.382-39.382-39.382zm0 20c5.523 0 10 4.477 10 10 0 5.321-4.156 9.672-9.399 9.982-.311 5.243-4.661 9.399-9.982 9.399-5.523 0-10-4.477-10-10-.001-10.686 8.694-19.381 19.381-19.381z"
                fill="#0090fb"
              />
              <path
                d="m45.571 148.79c5.321 0 9.672-4.156 9.982-9.399 5.243-.311 9.399-4.661 9.399-9.982 0-5.523-4.477-10-10-10-10.687 0-19.382 8.695-19.382 19.382.001 5.521 4.478 9.999 10.001 9.999z"
                fill="#fff"
              />
              <ellipse
                cx="54.953"
                cy="256"
                fill="#0090fb"
                rx="39.382"
                ry="39.382"
                transform="matrix(.383 -.924 .924 .383 -202.59 208.803)"
              />
              <path
                d="m54.953 333.828c-21.715 0-39.382 17.667-39.382 39.382s17.667 39.382 39.382 39.382 39.382-17.667 39.382-39.382-17.667-39.382-39.382-39.382zm0 58.764c-5.523 0-10-4.478-10-10 0-5.321 4.157-9.672 9.4-9.982.311-5.243 4.661-9.399 9.982-9.399 5.523 0 10 4.478 10 10 0 10.686-8.694 19.381-19.382 19.381z"
                fill="#0090fb"
              />
              <path
                d="m64.335 363.21c-5.321 0-9.672 4.156-9.982 9.399-5.243.311-9.4 4.661-9.4 9.982 0 5.522 4.477 10 10 10 10.688 0 19.382-8.694 19.382-19.382 0-5.521-4.477-9.999-10-9.999z"
                fill="#fff"
              />
            </g>
          </svg>
        </button>
      </div>

      {/* Dropdown menu */}
      {isOpen && <DropdownMenu />}
    </div>
  );
};

export default MenuIcon;
