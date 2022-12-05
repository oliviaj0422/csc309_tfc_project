import './App.css';
import NavBar from './components/NavBarElem';

import {BrowserRouter, Routes, Route} from 'react-router-dom';
import { useState, useEffect, createContext } from 'react';
import { LoginContext } from './Contexts/LoginContext';
import Login from './pages/Login';
import Memberships from './pages/Memberships';

import GetClasses from './components/GetClasses/GetClasses';


function App() {
  const [loggedIn, setLoggedIn] = useState(
    localStorage.access ? true : false
  );
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
        </Routes>
      </BrowserRouter>
    </LoginContext.Provider>

    <GetClasses />

  );
}

export default App;
