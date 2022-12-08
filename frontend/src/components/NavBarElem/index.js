import React from 'react';
import { Nav, NavLink, NavMenu, NavBtn, NavBtnLink, Logo, NavLogo } from './NavBar';
import logo from '../../tfc_logo.png';
import { LoginContext } from '../../Contexts/LoginContext';
import { useContext } from 'react';

const NavBar = () => {
  const [loggedIn, setLoggedIn] = useContext(LoginContext);
  return (
    <>
      <Nav>
        <NavLogo to="/">
            <Logo src={logo} alt="logo"></Logo>
        </NavLogo>
        <NavMenu>
          <NavLink to="/classes">
            Classes
          </NavLink>
          <NavLink to="/search_classes">
            SearchClasses
          </NavLink>
          <NavLink to="/memberships">
            Membership
          </NavLink>
          <NavLink to="/my_schedule">
            MySchedule
          </NavLink>
          <NavLink to="/my_class_history">
            MyClassHistory
          </NavLink>
          <NavBtn>
            <NavBtnLink to="/register">JOIN US</NavBtnLink>
          </NavBtn>
          {loggedIn ? (
            <NavLink to="/login" onClick={()=>{
              setLoggedIn(false);
              localStorage.clear();
            }}>
            LOG OUT
          </NavLink>  
            ) : (
              <NavLink to="/login">
              LOG IN
            </NavLink>
            )}
        </NavMenu>
      </Nav>
    </>
  )
}

export default NavBar
