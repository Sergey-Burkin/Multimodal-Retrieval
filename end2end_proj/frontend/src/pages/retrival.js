// Filename - pages/retrival.js

import React from "react";
import API from "../API"
// import axios from "axios"
import FileForm from "../compoents/Fileform";

// const base_url = "http://127.0.0.1:8000/base_ops/protected-route";


class Retrival extends React.Component {
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
                <h1>Retrival System</h1>
                <FileForm />

                {/* <form>
                    <p><input placeholder="username" onChange={(el) => this.setState({username: el.target.value})}></input></p>
                    <p><input placeholder="password" onChange={(el) => this.setState({password: el.target.value})}></input></p>
                    <p></p>
                    <button
                        type="button" onClick={() => this.SubmitForm()}
                    >
                    Submit
                    </button>
                </form> */}
            </div>
        );
    }


    SubmitForm() {
        console.log("Main Query!");
        // API.get("/base_ops/unprotected-route").then((res) => {console.log(res.data)});
        let config = {
            headers: {
                'Access-Control-Allow-Origin': true,
                'Content-Type': 'application/json',
            },
            params: {
                "token": localStorage.getItem('accessToken'),
            }
        }
        API.get("/protected-route", config).then((res) => {console.log(res.data)});
    };
};

export default Retrival;
