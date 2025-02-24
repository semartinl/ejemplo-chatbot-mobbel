import React from 'react'
import { DeepChat } from "deep-chat-react";

export default function CustomApi() {
  return (
    <div className="chat-container">
          <h1>CHAT CON API PERSONALIZADA</h1>
          <DeepChat
            connect={{ url: "http://127.0.0.1:8080/chat" }}
          />
    </div>
  )
}
