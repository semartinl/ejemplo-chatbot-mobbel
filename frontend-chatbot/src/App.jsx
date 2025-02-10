import { Routes, Route, BrowserRouter } from "react-router";
import CustomApi from "./Components/CustomApi";
import Main from "./Components/Main";


export default function App() {
  return (
    <>
    <BrowserRouter>
    
      <Routes >
      
      <Route exact path="/" element={<Main/>}>
      
       
        <Route path="api-custom" element={<CustomApi/>}/>
        
        <Route path="api-openai"></Route>
        <Route path="api-huggingface"></Route>

      </Route>
      </Routes>
    </BrowserRouter>
    </>
  );
}
