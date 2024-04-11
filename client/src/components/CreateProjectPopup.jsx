import React, { useState } from "react";
import Loader from "./Loader";
import Toast from "./Toast";
import { toast } from "react-toastify";
import { useSelector } from "react-redux";

const CreateProjectPopup = ({ isOpen, onClose, projectupdate }) => {
  const user = useSelector((state) => state.user.value);
  const [files, setFiles] = useState([]);
  const [uploadProgress, setUploadProgress] = useState(0);

  if (!isOpen) return null;

  const handleFileChange = (event) => {
    const fileArray = Array.from(event.target.files);
    setFiles([...files, ...fileArray]);
  };

  const handleDeleteFiles = (index) => {
    setFiles(files.filter((_, fileindex) => fileindex !== index));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    // Reset progress to 0 at the start of the upload
    setUploadProgress(0);

    const formData = new FormData();
    formData.append("name", event.target.projectName.value);
    formData.append("user_id", user.id);
    files.forEach((file) => formData.append("files", file));

    const xhr = new XMLHttpRequest();

    xhr.timeout = 90000; // 30,000 milliseconds = 30 seconds

    // Listen for the `progress` event
    xhr.upload.onprogress = function (event) {
      if (event.lengthComputable) {
        // Calculate the percentage, going up to 90% to account for server processing time
        const percentComplete = (event.loaded / event.total) * 90;
        setUploadProgress(percentComplete);
      }
    };

    xhr.onload = function () {
      // Once the server responds, manually set the progress to 100%
      setUploadProgress(100);

      if (xhr.status >= 200 && xhr.status < 300) {
        // Handle success
        console.log("Successfully stored data", JSON.parse(xhr.responseText));
        toast(<Toast message="Project created successfully" type="success" />);
        projectupdate();
      } else {
        // Handle error
        console.error("Failed to store data", xhr.statusText);
        toast(<Toast message="Oops something went wrong" type="error" />);
      }
      setUploadProgress(0);
      onClose(); // Optionally close the popup if the upload was successful
    };

    xhr.onerror = function () {
      // In case of request failure, also consider setting progress to 100% to indicate completion
      setUploadProgress(100);
      console.error("Request failed");
      toast(<Toast message="Network error, please try again" type="error" />);
      setUploadProgress(0);
      onClose(); // Optionally consider if you want to close the popup here or allow the user to retry
    };

    // Handle timeout
    xhr.ontimeout = function () {
      console.error("The request for uploading files timed out.");
      toast(
        <Toast message="The request timed out, please try again" type="error" />
      );
      setUploadProgress(0);
      onClose();
    };

    xhr.open("POST", `${process.env.REACT_APP_BACKEND_URL}/create`, true);
    xhr.send(formData);
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
              Project Name
            </label>
            <input
              type="text"
              id="projectName"
              className="mt-1 border-2 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>
          <div className="mb-4 flex flex-col gap-4">
            <label
              htmlFor="files"
              className="block text-sm  text-gray-700 font-bold font-mono"
            >
              Upload Knowledge Base
              <span className="flex justify-center items-center border-4 p-4 cursor-pointer">
                <img
                  alt="image not found"
                  className="h-10 w-10 cursor-pointer"
                  src="data:image/png;base64,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"
                />
              </span>
            </label>
            <input
              type="file"
              id="files"
              multiple
              label="asfda"
              onChange={handleFileChange}
              className="mt-1 border-2 w-full hidden rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            />
          </div>
          <div className="mb-4">
            <ul>
              {files.map((file, index) => (
                <div className="flex gap-2">
                  <li key={index} className="text-sm text-gray-800">
                    {file.name}
                  </li>
                  <img
                    onClick={() => handleDeleteFiles(index)}
                    className="w-5 h-5 cursor-pointer"
                    src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAACXBIWXMAAAsTAAALEwEAmpwYAAAB50lEQVR4nO2Z30rDMBSH46XDm4mIiOALzW627saHcJ3YernX2nRT/PM2Ui9szo0IR4qbxpGlSXuSoOQHuU2/b6Xd+aWMhYSEhPyZwGl+Bkm2wOFkh3pv7E06EOezMr4+Z7bgeZy/Q5Ijj/NHSgn8gp8v9/4glxDhV4tKAgV4YW86CRk8lQRK4EklVPBtJVTwQCGhA99UQgce2kggY1uQZFOdC/ysbFGBacEn2cJw72nFZCYxHG9Dkt+aXKjuTpj88rDaM8keGj9nlBLO4SklvMFTSHiHb/PwldFoxqP03jt8kzvBB2Modg/fXveOkPdT//AmEiv4F8awWjoS3AW8jsQ6vI4EdwmvktgEr5LgPuBlEnXwMgnuE/5bojfpVG+bolsPL0qU0cWzd/iVAPTTu2L/WAu+WkX3gMPJaO5d4FeTGlyijkQFX0YjkP1jO420SdVIiPCbxg4nUTapDRIyePAhodWk1iRU8OBSwqhJLSV04MGFRKOpsp8+8Si9sdHsjNJmJLbR7IxCMc97k0DCMuJcAi00KWcS+B+OVSC+SrQPtgynSqNmF7c5ndOQaDoSazW7mOJ8VCHRdp5HVbMjPaGWSFCVEZQ1OyvfCAQJ6iaFYrOzAS9KWPvENKwksqk1+JCQkBBmI5/G9M0wq45fBQAAAABJRU5ErkJggg=="
                  ></img>
                </div>
              ))}
            </ul>
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
              Create
            </button>
          </div>
          <div className="mt-2">
            <Loader uploadProgress={uploadProgress} />
          </div>
        </form>
      </div>
    </div>
  );
};

export default CreateProjectPopup;
