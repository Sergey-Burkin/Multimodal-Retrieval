// Filename - "./components/Navbar/index.js

import React from "react";
import { Nav, NavLink, NavMenu } from "./NavbarElements";

const Navbar = () => {
	return (
		<>
			<Nav>
				<NavMenu>
					{/* <NavLink to="/about" activeStyle>
						About
					</NavLink>
					<NavLink to="/contact" activeStyle>
						Contact Us
					</NavLink> */}
					<NavLink to="/retrival" activeStyle>
						Retrival
					</NavLink>
					<NavLink to="/sign-up" activeStyle>
						Sign Up
					</NavLink>
					<NavLink to="/login" activeStyle>
						Login
					</NavLink>
				</NavMenu>
			</Nav>
		</>
	);
};

export default Navbar;
