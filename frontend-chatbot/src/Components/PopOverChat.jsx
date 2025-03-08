import { DeepChat } from 'deep-chat-react'
import React, { useEffect, useState } from 'react'

export default function PopOverChat() {
    const [isOpen, setIsOpen] = useState(false)
  const[texto, setTexto] = useState("Abrir chat")

  useEffect(()=> {
    if(isOpen){
      setTexto("Cerrar Texto")
    }
    else{
      setTexto("Abrir texto")
    }
  }, [isOpen])

  return (
    <section className='popover-chat'>
    {isOpen? <DeepChat
                connect={{ url: "http://localhost:8080/ollama-chat" }}
              /> : null}
    <button onClick={()=> setIsOpen(!isOpen)}>{texto}</button>
    </section>

  )
}
