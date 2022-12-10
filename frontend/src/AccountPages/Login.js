import { baseUrl } from "../base_url";
import { useState, useContext } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { LoginContext } from "../Contexts/LoginContext";
import 'bootstrap/dist/css/bootstrap.min.css';
import "../App.css";

export default function Login() {
    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const location = useLocation();
    const navigate = useNavigate();

    function login(e){
        e.preventDefault();
        const url = baseUrl + "api/token/";
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        })
            .then((response) => {
                if (response.ok) {
                    setError("");
                    navigate(
                        location?.state?.previousUrl
                            ? location.state.previousUrl
                            : '/profile'
                    );
                }
                else if (response.status === 401) {
                    setError("Invalid username and/or password. Please try again.")
                }
                return response.json();
            })
            .then((data) => {
                localStorage.setItem('access', data.access);
                localStorage.setItem('id', data.id);
                if (data.access) {
                    // show success message (popup? a sentence? idk)
                    setLoggedIn(true);
                }
            })

    }
    return (
        
        <form className="m-2 w-full max-w-sm" id="customer" onSubmit={login} style={{"textAlign": "center"}}>
            <div className="md:flex md:items-center mb-6">
                <h3>Log In</h3>
                <br />
                <div className="error-msg">
                <h5 style={{color: "red"}}>{error}</h5>
            </div>
            <br/>
                <div className="md:w-1/4">
                    <label htmlFor="username">Username</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="username"
                        type="username"
                        value={username}
                        onChange={(e) => {
                            setUsername(e.target.value);
                        }}
                        placeholder="Enter your username"
                        style={{"textAlign": "center"}}
                    />
                </div>
            </div>
            <br />
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="password">Password</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="password"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="password"
                        value={password}
                        onChange={(e) => {
                            setPassword(e.target.value);
                        }}
                        placeholder="Enter your password"
                        style={{"textAlign": "center"}}
                    />
                </div>
            </div>
            <br/>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end" style={{"margin-right": "200px", "margin-bottom": "200px"}}>
                <button class="btn btn-primary me-md-2" type="submit">Sign in</button>
            </div>
        </form>
    );
}