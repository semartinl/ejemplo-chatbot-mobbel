import React from 'react'
import { NavLink, Outlet } from 'react-router'
import PopOverChat from './PopOverChat'
export default function Main() {
  return (
    <>
        <header className='header-chatbots'>
            <NavLink to="/api-custom">Api personalizada</NavLink>
            <NavLink to="/api-ollama">Api de Ollama</NavLink>
            <NavLink to="/api-docker"> Api de Docker</NavLink>
            
        </header>
        <Outlet/>
        <PopOverChat/>
    </>
  )
}
