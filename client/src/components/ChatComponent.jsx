import React, { useState, useEffect, useRef } from "react";
import BotIcon from "./BotIcon";
import HumaneIcon from "./HumaneIcon";
import ModelInfo from "./ModelInfo";

const ChatComponent = ({ id }) => {
  const [models, setModels] = useState([]);
  const [isPopupOpen, setIsPopupOpen] = useState(false);
  const handleOpenPopup = () => setIsPopupOpen(true);
  const handleClosePopup = () => setIsPopupOpen(false);
  const [selectedModel, setSelectedModel] = useState("");
  // const ollamaModels = ["Ollama X", "Ollama M", "Ollama Lite"];
  const [prompt, setPrompt] = useState("");
  const messagesEndRef = useRef(null);

  const [userInput, setUserInput] = useState([]);

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/models`);

    const data = await response.json();

    setModels(data);
    setSelectedModel(data[0].id);
    console.log(models);
    console.log(`models = ${data}`);
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [userInput]);

  const handleSelectChange = (e) => {
    setSelectedModel(e.target.value);
    handleOpenPopup(true);
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return; // Avoid sending empty messages

    // Add the user's message to the chat display.
    setUserInput((prevInput) => [
      ...prevInput,
      { type: "user", icon: "A", message: prompt },
    ]);

    setUserInput((prevInput) => [
      ...prevInput,
      {
        type: "bot-typing-icon",
        icon: "B",

        message: (
          <span className="blinking-dots text-6xl text-black-500">...</span>
        ),
      },
    ]);

    const url = `${
      process.env.REACT_APP_BACKEND_URL
    }/chat/stream?q=${encodeURIComponent(
      prompt
    )}&project_id=${id}&model_id= ${selectedModel}`;

    setPrompt(""); // Reset the prompt for the next message

    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          Accept: "text/event-stream",
        },
      });

      if (!response.ok || !response.body) {
        throw new Error("Stream response not ok");
      }

      console.log("resposne is", response);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      // Function to process and display each chunk as it arrives
      const processAndDisplayChunk = async (isFirstChunk = true) => {
        const { value, done } = await reader.read();
        if (done) {
          finalizeBotTypingMessage();
          return;
        }

        let chunk = decoder.decode(value, { stream: true });

        console.log("CHUNK IS ", chunk);
        // Prepend a newline to each chunk if it's not the first chunk
        if (!isFirstChunk && chunk) {
          chunk = "\n  " + chunk;
        }

        if (chunk) {
          await simulateTypingEffect(chunk, isFirstChunk);
          await processAndDisplayChunk(false); // Process the next chunk
        } else {
          await processAndDisplayChunk(isFirstChunk); // Continue with the current state of isFirstChunk
        }
      };

      await processAndDisplayChunk(); // Start processing with the first chunk
    } catch (error) {
      console.error("Failed to fetch stream:", error);
    }
  };

  const simulateTypingEffect = async (chunk, isFirstChunk) => {
    if (isFirstChunk) {
      setUserInput((prevInput) =>
        prevInput.map((input, index) =>
          input.type === "bot-typing-icon"
            ? { ...input, message: "", type: "bot-typing" } // Replace with an empty string or another message
            : input
        )
      );
    }
    let currentIndex = -1;
    return new Promise((resolve) => {
      const typeNextChar = () => {
        if (currentIndex < chunk.length) {
          setUserInput((prevInput) => {
            const lastInput = prevInput[prevInput.length - 1];
            const updatedMessage =
              lastInput?.type === "bot-typing"
                ? lastInput.message + chunk.charAt(currentIndex)
                : chunk.charAt(currentIndex);

            // If the last message is a typing message, update it; otherwise, create a new typing message.
            const updatedInput =
              lastInput?.type === "bot-typing"
                ? [
                    ...prevInput.slice(0, prevInput.length - 1),
                    { ...lastInput, message: updatedMessage },
                  ]
                : [
                    ...prevInput,
                    { type: "bot-typing", icon: "B", message: updatedMessage },
                  ];

            return updatedInput;
          });

          currentIndex++;
          setTimeout(typeNextChar, 10); // Adjust the typing speed as needed.
        } else {
          resolve(); // Resolve the promise once all characters have been "typed".
        }
      };

      typeNextChar();
    });
  };

  const finalizeBotTypingMessage = () => {
    setUserInput((prevInput) =>
      prevInput.map((input) =>
        input.type === "bot-typing" ? { ...input, type: "bot" } : input
      )
    );
  };

  return (
    <div className="flex flex-col h-screen overflow-y-auto">
      <div className="flex-grow flex flex-col bg-gray-100 overflow-y-auto mb-16">
        <div className="flex flex-grow flex-col justify-end p-6">
          <div className="grid grid-cols-12 gap-y-2">
            {userInput &&
              userInput.map((obj, index) => {
                if (obj.type !== "user") {
                  return (
                    <div
                      className="col-start-1 col-end-8 p-3 rounded-lg"
                      key={index}
                    >
                      <div className="flex flex-row items-center">
                        <div className="flex items-center justify-center h-16 w-16 rounded-full bg-teal-500 flex-shrink-0">
                          <BotIcon />
                        </div>
                        <div
                          ref={messagesEndRef}
                          className="relative ml-3 font-sans text-lg leading-relaxed tracking-wide shadow-md px-4 rounded-xl"
                        >
                          <div>{obj.message}</div>
                        </div>
                      </div>
                    </div>
                  );
                } else {
                  return (
                    <div
                      className="col-start-6 col-end-13 p-3 rounded-lg"
                      key={index}
                    >
                      <div className="flex items-center justify-start flex-row-reverse">
                        <div className="flex items-center justify-center h-16 w-16 rounded-full bg-teal-500 flex-shrink-0">
                          <HumaneIcon />
                        </div>
                        <div
                          ref={messagesEndRef}
                          className="relative font-sans text-lg leading-relaxed tracking-wide mr-3 shadow-md px-4 rounded-xl"
                        >
                          <div>{obj.message}</div>
                        </div>
                      </div>
                    </div>
                  );
                }
              })}
          </div>
        </div>
      </div>
      <div className="flex-shrink-0 bg-white border-t border-gray-200 p-4 flex justify-between items-center fixed bottom-0 w-screen mr-96">
        <div className="relative w-full mx-4 flex flex-row">
          <select
            value={selectedModel}
            onChange={handleSelectChange}
            name="ollama-model"
            id="ollama-model"
            className="block pl-5 mr-2 py-2 bg-inherit font-mono font-bold from-neutral-900 border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
          >
            {models &&
              models.map((model, index) => (
                <option key={model.id} value={model.id}>
                  {model.name}
                </option>
              ))}
          </select>
          <input
            id="userMessage" // Added id to the input field
            type="text"
            className="flex w-full border-4 border-solid border-blue-500 rounded-xl focus:outline-none focus:border-indigo-300 pl-4 h-10"
            onChange={(e) => setPrompt(e.target.value)}
            value={prompt}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault(); // Prevent the default action to avoid submitting the form
                handleSendMessage(e);
              }
            }}
            autocomplete="off"
          />
          <button
            onClick={handleSendMessage}
            className="absolute flex items-center justify-center h-full w-12 right-0 top-0 text-gray-400 hover:text-gray-600"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
          </button>
        </div>
        <button
          className="flex items-center justify-center bg-indigo-500 hover:bg-indigo-600 rounded-xl text-white px-4 py-1 flex-shrink-0 mr-10"
          onClick={handleSendMessage}
        >
          <span>Send</span>
          <span className="ml-2">
            <svg
              className="w-4 h-4 transform rotate-45 -mt-px"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
              ></path>
            </svg>
          </span>
        </button>
      </div>

      <ModelInfo
        modelid={selectedModel}
        models={models}
        isPopupOpen={isPopupOpen}
        handleOpenPopup={handleOpenPopup}
        handleClosePopup={handleClosePopup}
      />
    </div>
  );
};

export default ChatComponent;
