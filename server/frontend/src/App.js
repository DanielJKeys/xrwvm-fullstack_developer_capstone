import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register"; 
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      
      {/* 2. Configure the register route */}
      <Route path="/register" element={<Register />} />
    </Routes>
  );
}

export default App;
