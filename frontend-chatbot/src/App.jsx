import { Routes, Route, BrowserRouter } from "react-router";
import CustomApi from "./Components/CustomApi";
import Main from "./Components/Main";
import ApiColab from "./Components/ApiColab";
import ApiHF from "./Components/ApiHF";
import ApiOllama from "./Components/ApiOllama";
import ApiOllamaDocker from "./Components/ApiOllama-Docker";


export default function App() {
  return (
    <>
    <BrowserRouter>
    
      <Routes >
      
      <Route exact path="/" element={<Main/>}>
      
       
        <Route path="api-custom" element={<CustomApi/>}/>
        
        <Route path="api-colab" element={<ApiColab/>}/>
        <Route path="api-openai"></Route>
        <Route path="api-huggingface" element={<ApiHF/>}/>
        <Route path="api-ollama" element={<ApiOllama/>}/>
        <Route path="api-docker" element={<ApiOllamaDocker/>}/>

      </Route>
      </Routes>
    </BrowserRouter>
    </>
  );
}
