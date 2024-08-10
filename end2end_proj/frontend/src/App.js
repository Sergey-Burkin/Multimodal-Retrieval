// Filename - App.js

import React from "react";
import {
	BrowserRouter as Router,
	Routes,
	Route,
} from "react-router-dom";

import Navbar from "./compoents/index";

import Home from "./pages/index";
import Retrival from "./pages/retrival";
import SignUp from "./pages/signup";
import Login from "./pages/login";


function App() {
	return (
		<Router>
			<Navbar />
			<Routes>
				<Route exact path="/" element={<Home />} />
				<Route
					path="/retrival"
					element={<Retrival />}
				/>
				<Route
					path="/sign-up"
					element={<SignUp />}
				/>
				<Route
					path="/login"
					element={<Login />}
				/>
			</Routes>
		</Router>
	);
}

export default App;
