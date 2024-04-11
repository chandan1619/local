import React, { useState } from "react";
import CreateChatPopup from "./CreateChatPopup";

const ChatCreate = () => {
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  const handleOpenPopup = () => setIsPopupOpen(true);
  const handleClosePopup = () => setIsPopupOpen(false);
  return (
    <div className="w-96 h-40 border-4 shadow-md flex flex-row justify-center items-center gap-2 rounded-2xl  hover:shadow-black">
      <svg
        fill="#000000"
        height="35px"
        width="35px"
        version="1.1"
        id="Capa_1"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 60 60"
      >
        <path
          d="M30,1.5c-16.542,0-30,12.112-30,27c0,5.205,1.647,10.246,4.768,14.604c-0.591,6.537-2.175,11.39-4.475,13.689
	c-0.304,0.304-0.38,0.769-0.188,1.153C0.276,58.289,0.625,58.5,1,58.5c0.046,0,0.093-0.003,0.14-0.01
	c0.405-0.057,9.813-1.412,16.617-5.338C21.622,54.711,25.738,55.5,30,55.5c16.542,0,30-12.112,30-27S46.542,1.5,30,1.5z"
        />
      </svg>
      <button
        className="font-bold border-full hover:bg-green-600 px-4 py-2 rounded-full font-mono border-dotted border-2 border-green-600"
        onClick={handleOpenPopup}
      >
        Chat with Project
      </button>
      <CreateChatPopup isOpen={isPopupOpen} onClose={handleClosePopup} />
    </div>
  );
};

export default ChatCreate;
