import React, { useState } from "react";
import CreateProjectPopup from "./CreateProjectPopup";

const ProjectCreate = ({ projectupdate }) => {
  const [isPopupOpen, setIsPopupOpen] = useState(false);

  const handleOpenPopup = () => setIsPopupOpen(true);
  const handleClosePopup = () => setIsPopupOpen(false);
  return (
    <div className="w-96 h-40 border-4 shadow-md flex flex-row justify-center items-center gap-2 rounded-2xl  hover:shadow-black">
      <img
        className="cursor-pointer w-10 h-10"
        src="data:image/png;base64,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"
      ></img>
      <button
        className="font-bold border-full hover:bg-blue-600 px-4 py-2 rounded-full font-mono border-dotted border-2 border-green-600"
        onClick={handleOpenPopup}
      >
        Create New Project
      </button>
      <CreateProjectPopup
        isOpen={isPopupOpen}
        onClose={handleClosePopup}
        projectupdate={projectupdate}
      />
    </div>
  );
};

export default ProjectCreate;
