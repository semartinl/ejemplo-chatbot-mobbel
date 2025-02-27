import { DeepChat } from 'deep-chat-react'
import React from 'react'

export default function ApiColab() {
  return (
    <div className="chat-container">
              <h1>CHAT CON API EN COLAB</h1>
              <DeepChat
                connect={{ url: "https://19dd-34-124-212-79.ngrok-free.app/chat" }}
              />
        </div>
  )
}
