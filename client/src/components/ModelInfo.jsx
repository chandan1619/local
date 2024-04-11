import { useState } from "react";
import CopyToClipboardButton from "./CopyToClipboardButton";

const ModelInfo = ({
  modelid,
  models,
  isPopupOpen,
  handleOpenPopup,
  handleClosePopup,
}) => {
  const [logs, setLogs] = useState("");
  const [modelname, setModelName] = useState("mixtral"); // Assuming you have a way to set this

  if (!isPopupOpen) return null;
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex justify-center items-center">
      <div className="bg-white p-5 rounded-lg shadow-lg max-w-md w-full">
        <div className="flex flex-col space-y-4">
          <h2 className="text-lg font-semibold">Model Details</h2>
          {models &&
            models.map((model, index) => {
              if (model.id == modelid) {
                return (
                  <>
                    <p>
                      <strong>Model Name:</strong> {model.name}
                    </p>
                    <p>
                      <strong>Number of Parameters:</strong> {model.parameters}
                    </p>{" "}
                    {/* Example value */}
                    <p>
                      <strong>RAM Required:</strong> {model.ram_size}
                    </p>{" "}
                    {/* Example value */}
                    <p>
                      <strong>Model Size:</strong> {model.model_size}
                    </p>{" "}
                    {/* Example value */}
                    <p>
                      <strong>Hugging Face URL:</strong>{" "}
                      <a
                        href={model.hugging_face_url}
                        className="text-blue-500 hover:underline"
                      >
                        {model.hugging_face_url}
                      </a>
                    </p>
                    <strong>
                      Download model by running the below command in your
                      terminal:
                    </strong>{" "}
                    <CopyToClipboardButton textToCopy={model.install_command} />
                    <div className="flex justify-center">
                      <button
                        onClick={handleClosePopup}
                        type="button"
                        className=" justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-red-500 hover:bg-red-700"
                      >
                        Close
                      </button>
                    </div>
                  </>
                );
              }
            })}
        </div>
      </div>
    </div>
  );
};

export default ModelInfo;
