import styled from "styled-components";
import { NavLink as Link } from "react-router-dom";

export const Nav = styled.nav`
  background: #fd6114;
  height: 110px;
  display: flex;
  justify-content: space-between;
  padding: 0.5rem calc((100vw - 1000px)/2);
  z-index: 10;
`

export const NavLogo = styled(Link)`
  display: flex;
  align-items: center;
  cursor: pointer;
`

export const Logo = styled.img`
  max-width: 180px;
  height: 90px;
`


export const NavLink = styled(Link)`
  color: white;
  display: flex;
  align-items: center;
  text-decoration: none;
  margin-left: 5px;
  margin-right: 20px;
  padding: 0 1rem;
  height: 100%;
  cursor: pointer;

  &:active {
    color: #15cdfc;
  }

  &:hover {
    text-decoration: underline;
  }
`

export const NavMenu = styled.div`
  display: flex;
  align-items: center;
  margin-right: -10px;
`

export const NavBtn = styled.nav`
  display: flex;
  align-items: center;
  margin-left: 20px;
  margin-right: 24px;
`

export const NavBtnLink = styled(Link)`
  border-radius: 4px;
  background: white;
  padding: 10px 22px;
  color: #fd6114;
  border: none;
  outline: none;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-decoration: none;

  &:hover {
    transition: all 0.2s ease-in-out;
    background: #fd6114;
    color: white;
  }

`
