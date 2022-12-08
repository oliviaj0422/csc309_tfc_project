import "./App.css";
import NavBar from "./components/NavBarElem";

import SearchClasses from "./components/SearchClasses/SearchClasses";
import MyClassHistory from "./components/MyClassHistory/MyClassHistory";
import GetClasses from "./components/GetClasses/GetClasses";
import MySchedule from "./components/MySchedule/MySchedule";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState, useEffect, createContext } from "react";
import { LoginContext } from "./Contexts/LoginContext";
import Login from "./AccountPages/Login";
import Memberships from "./AccountPages/Memberships";

import Studios from "./components/Studios/studios";

function App() {
  const [loggedIn, setLoggedIn] = useState(localStorage.access ? true : false);
  function changeLoggedIn(value) {
    setLoggedIn(value);
    if (value === false) {
      localStorage.clear();
    }
  }

  return (
    <LoginContext.Provider value={[loggedIn, changeLoggedIn]}>
      <BrowserRouter>
        <NavBar /> <br />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/memberships" element={<Memberships />} />
          <Route path="/classes" element={<GetClasses />} />
          <Route path="/my_schedule" element={<MySchedule />} />
          <Route path="/my_class_history" element={<MyClassHistory />} />
          <Route path="/search_classes" element={<SearchClasses />} />
          <Route path="/my_studios" element={<Studios />} />
          <Route path="/" element={<Studios />} exact/>
        </Routes>
      </BrowserRouter>
    </LoginContext.Provider>
  );
}

export default App;
