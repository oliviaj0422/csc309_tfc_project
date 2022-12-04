import React from 'react';
import { Nav, NavLink, NavMenu, NavBtn, NavBtnLink, Logo, NavLogo } from './NavBar';
import logo from '../../tfc_logo.png';

const NavBar = () => {
  return (
    <>
      <Nav>
        <NavLogo to="/" activeStyles>
            <Logo src={logo} alt="logo"></Logo>
        </NavLogo>
        <NavMenu>
          <NavLink to="/studios" activeStyles>
            STUDIOS
          </NavLink>
          <NavLink to="/studios" activeStyles>
            CLASSES
          </NavLink>
          <NavLink to="/studios" activeStyles>
            MEMBERSHIP
          </NavLink>
          <NavBtn>
            <NavBtnLink to="/signup">JOIN US</NavBtnLink>
          </NavBtn>
          <NavLink to="/signin" activeStyles>
            LOG IN
          </NavLink>
        </NavMenu>
      </Nav>
    </>
  )
}

export default NavBar
