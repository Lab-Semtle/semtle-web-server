import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Stackboot from "./pages/Board/Stackboot";
import Main from "./pages/Main/Main";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Main />} />
          <Route path="/Board" element={<Stackboot />} />
          <Route path="/Main" element={<Main />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
