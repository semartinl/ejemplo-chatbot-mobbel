import { DeepChat } from 'deep-chat-react'
import React from 'react'

export default function ApiOllamaDocker() {
  return (
    <div className="chat-container">
                  <h1>CHAT CON API CON DOCKER DE OLLAMA</h1>
                  <DeepChat
                    connect={{ url: "http://api-chatbot:8080/ollama-chat" }}
                  />
            </div>
  )
}
