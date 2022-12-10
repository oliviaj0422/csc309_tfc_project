import React from 'react';
import { Nav, NavLink, NavMenu, NavBtn, NavBtnLink, Logo, NavLogo } from './NavBar';
import logo from '../../images/tfc_logo.png';
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
            CLASSES
          </NavLink>
          <NavLink to="/search_classes">
            SEARCH CLASSES
          </NavLink>
          {/* <NavLink to="/my_schedule">
            MySchedule
          </NavLink>
          <NavLink to="/my_class_history">
            MyClassHistory
          </NavLink> */}
          <NavLink to="/memberships">
            MEMBERSHIP
          </NavLink>
          <NavBtn>
            <NavBtnLink to="/register">JOIN US</NavBtnLink>
          </NavBtn>
          {loggedIn ? (
            <>
            <NavLink to="/login" onClick={()=>{
              setLoggedIn(false);
              localStorage.clear();
            }}>
              LOG OUT
            </NavLink> 
            <NavLink to="/profile">
              ACCOUNT
            </NavLink> 
        </>
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
