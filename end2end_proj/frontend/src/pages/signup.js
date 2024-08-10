// Filename - pages/signup.js

import React from "react";
import API from "../API"
// import axios from "axios"


// const base_url = "http://127.0.0.1:8000/auth/register";


class SignUp extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            username: "",
            password: "",
            is_logined: false,
        }
    }

    render () {
        return (
            <div>
                <h1>SignUp</h1>
                <form>
                    <p><input placeholder="username" onChange={(el) => this.setState({username: el.target.value})}></input></p>
                    <p><input placeholder="password" onChange={(el) => this.setState({password: el.target.value})}></input></p>
                    <button type="button" onClick={() => this.SubmitForm()}>Submit</button>
                </form>

                {this.state.is_logined && <p>SignUp Successfuly</p>}
            </div>
        );
    }

    SubmitForm() {
        // const kwargs = {
        //     "password": this.state.password,
        //     "username": this.state.username,
        // }
        let config = {
            headers: {
                'Access-Control-Allow-Origin': true,
                'Content-Type': 'application/json',
            },
            params: {
                "username": this.state.username,
                "password": this.state.password,
            }
        }
        API.post("/register", {}, config).then((res) => {console.log(res.data)});
        // .catch((err) => { console.log(err); })
		this.setState({is_logined: true});
    };
};

export default SignUp;
