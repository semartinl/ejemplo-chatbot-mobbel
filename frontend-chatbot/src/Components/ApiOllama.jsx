import { DeepChat } from 'deep-chat-react'
import React from 'react'

export default function ApiOllama() {
  return (
    <div className="chat-container">
                  <h1>CHAT CON API EN HUGGING FACE</h1>
                  <DeepChat
                    connect={{ url: "http://127.0.0.1:8080/ollama-chat" }}
                  />
            </div>
  )
}
