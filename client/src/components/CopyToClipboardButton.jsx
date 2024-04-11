import React, { useState } from "react";

const CopyToClipboardButton = ({ textToCopy }) => {
  const [isCopied, setIsCopied] = useState(false);

  const handleCopyClick = async () => {
    try {
      await navigator.clipboard.writeText(textToCopy);
      setIsCopied(true);
      setTimeout(() => setIsCopied(false), 2000); // Reset the copied state after 2 seconds
    } catch (err) {
      console.error("Failed to copy: ", err);
    }
  };

  return (
    <div className="relative flex items-start space-x-2">
      <div className="p-4  rounded  relative text-left font-mono font-bold text-sm text-blue-500">
        {textToCopy}
        <div
          onClick={handleCopyClick}
          className="cursor-pointer absolute top-0 right-0 p-2 transform translate-x-1/2"
          title="Copy to clipboard"
        >
          <svg
            height="15pt"
            viewBox="-21 0 512 512"
            width="15pt"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="m186.667969 416c-49.984375 0-90.667969-40.683594-90.667969-90.667969v-218.664062h-37.332031c-32.363281 0-58.667969 26.300781-58.667969 58.664062v288c0 32.363281 26.304688 58.667969 58.667969 58.667969h266.664062c32.363281 0 58.667969-26.304688 58.667969-58.667969v-37.332031zm0 0"
              fill="#1976d2"
            />
            <path
              d="m469.332031 58.667969c0-32.40625-26.261719-58.667969-58.664062-58.667969h-224c-32.40625 0-58.667969 26.261719-58.667969 58.667969v266.664062c0 32.40625 26.261719 58.667969 58.667969 58.667969h224c32.402343 0 58.664062-26.261719 58.664062-58.667969zm0 0"
              fill="#2196f3"
            />
          </svg>
        </div>
      </div>

      {/* Optional: Show feedback text */}
      {isCopied && (
        <span className="text-sm text-gray-500 absolute right-0 mt-1 mr-2">
          Copied!
        </span>
      )}
    </div>
  );
};

export default CopyToClipboardButton;
