import React from "react";
import ChatComponent from "../components/ChatComponent";
import Header from "../components/Header";
import { useParams } from "react-router-dom";

const Chat = () => {
  const { id } = useParams();
  console.log(id);
  return (
    <div className="">
      <div className="fixed top-0 w-screen z-50">
        <Header />
      </div>
      <div className="">
        <ChatComponent id={id} />
      </div>
    </div>
  );
};

export default Chat;
