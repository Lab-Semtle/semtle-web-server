import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Boardcreate from "./pages/Board/Boardcreate"
import Boardview from "./pages/Board/Boardview";
import Root from "./pages/root/Root";
import Login from "./pages/Login/Login";
import Membership from "./pages/membership/Membership";
import Boardlist from "./pages/Board/Boardlist";
import Boardedit from "./pages/Board/Boardedit";
import MyInfo from "./pages/MyInfo/MyInfo";
import IdFInd from "./pages/IdFind/IdFind";
import PwFInd from "./pages/PwFind/PwFind";
import Agree from "./pages/Agree/Agree";

import Studyboardlist from "./pages/Study_Board/Studyboardlist";
import Studyboardcreate from "./pages/Study_Board/Studyboardcreate";
import Studyboardview from "./pages/Study_Board/Studyboardview";
import Studyboardedit from "./pages/Study_Board/Studyboardedit";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Root />} />
          <Route path="/Main" element={<Root />} />
          <Route path="/Login" element={<Login />} />
          <Route path="/Membership" element={<Membership />} />

          <Route path="/Boardlist" element={<Boardlist />} />
          <Route path="/Boardcreate" element={<Boardcreate />}/>
          <Route path="/Boardview/:idx" element={<Boardview />}/>
          <Route path="/Board/edit/:idx" element={<Boardedit/>}/>

          <Route path="/StudyBoardlist" element={<Studyboardlist/>}/>
          <Route path="/StudyBoardcreate" element={<Studyboardcreate />}/>
          <Route path="/StudyBoardview/:idx" element={<Studyboardview />}/>
          <Route path="/StudyBoard/edit/:idx" element={<Studyboardedit/>}/>
          <Route path="/MyInfo" element = {<MyInfo/>}/>
          <Route path="/IdFind" element={<IdFInd />} />
          <Route path="/PwFind" element={<PwFInd />} />
          <Route path="agree" element={<Agree />} /> 
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
