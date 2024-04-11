import React from "react";
import { useNavigate } from "react-router-dom";

const CreateChatPopup = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  if (!isOpen) return null;
  const handleSubmit = (e) => {
    e.preventDefault();
    navigate(`/chat?${e.target.projectName.value}`);
  };
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center">
      <div className="bg-white p-5 rounded-lg shadow-lg max-w-sm w-full">
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label
              htmlFor="projectName"
              className="block font-mono font-bold text-sm  text-gray-700"
            >
              Project Id
            </label>
            <input
              type="text"
              id="projectName"
              className="mt-1 border-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>

          <div className="flex justify-end">
            <button
              type="button"
              onClick={onClose}
              className="mr-2 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-500 hover:bg-red-700"
            >
              Close
            </button>

            <button
              type="submit"
              className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-700"
            >
              Chat Now
            </button>
          </div>
          <div className="mt-2"></div>
        </form>
      </div>
    </div>
  );
};

export default CreateChatPopup;
