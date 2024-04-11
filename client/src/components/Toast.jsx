import React from "react";

const Toast = ({ message, type }) => {
  return (
    <div
      style={{
        position: "fixed",
        bottom: "20px",
        right: "5px",
        zIndex: 1000,
        width: "400px",
      }}
    >
      <div
        class="max-w-xs bg-green-800 text-sm text-white rounded-md shadow-lg dark:bg-gray-900 mb-3 ml-3 ml-3"
        role="alert"
        style={{ backgroundColor: type === "success" ? "green" : "red" }}
      >
        <div class="flex p-4">
          {message}
          <div class="ml-auto">
            <button
              type="button"
              class="inline-flex flex-shrink-0 justify-center items-center h-4 w-4 rounded-md text-white/[.5] hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-gray-600 transition-all text-sm dark:focus:ring-offset-gray-900 dark:focus:ring-gray-800"
            >
              <span class="sr-only">Close</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Toast;
