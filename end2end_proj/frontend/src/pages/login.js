import React from "react";
import API from "../API"


class Login extends React.Component {
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
                <h1>Login</h1>
                <form>
                    <p><input placeholder="username" onChange={(el) => this.setState({username: el.target.value})}></input></p>
                    <p><input placeholder="password" onChange={(el) => this.setState({password: el.target.value})}></input></p>
                    <button type="button" onClick={() => this.SubmitForm()}>Submit</button>
                </form>

                {/* {localStorage.getItem('accessToken') && <p>Logined Successfuly</p>} */}
            </div>
        );
    }

    SubmitForm() {
        console.log("Login submit console!\n");

        const kwargs = {
            "username": this.state.username,
            "password": this.state.password,
        }
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

        console.log(kwargs);
        console.log(config);
        API.post("/login", {}, config).then((res) => {
            console.log(res.data.access_token);
            localStorage.setItem('accessToken', res.data.access_token);
            console.log(localStorage.getItem('accessToken'))
        }).catch((err) => {console.log(err)});




        console.log("Login Ended!\n");
        this.setState({is_logined: true});
    };
};

export default Login;
