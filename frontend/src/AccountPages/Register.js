import { baseUrl } from "../base_url";
import { useState, useEffect, useContext } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { LoginContext } from "../Contexts/LoginContext";
import axios from 'axios';
import { Form } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import "../App.css";

export default function Register() {
    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [password2, setPassword2] = useState("");
    const [email, setEmail] = useState("");
    const [first, setFirst] = useState("");
    const [last, setLast] = useState("");
    const [phone, setPhone] = useState("");
    const [pmt, setPmt] = useState("");
    const [avatar, setAvatar] = useState(null);
    const [memberships, setMemberships] = useState(null);

    const [show, setShow] = useState(false);
    const [usernameError, setUsernameError] = useState("");
    const [pwd1Error, setPwd1Error] = useState("");
    const [pwd2Error, setPwd2Error] = useState("");
    const [emailError, setEmailError] = useState("");


    const location = useLocation();
    const navigate = useNavigate();


    const url2 = baseUrl + "memberships/";
    useEffect(() => {

        fetch(url2, {
            method: 'GET',
        })
        .then((response) => response.json())
        .then((data) => {
            setMemberships(data.results);
        });

    }, []);

    function register(e){
        e.preventDefault();
        const url = baseUrl + "account/signup/";

        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('password2', password2);
        formData.append('email', email);
        formData.append('first_name', first);
        formData.append('last_name', last);
        formData.append('phone_num', phone);
        formData.append('pmt_option', pmt);
        formData.append('avatar', avatar);

        axios.post(url, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
        }).then((res) => {
            console.log(res);
            if (res.status === 200)
                navigate(
                    location?.state?.previousUrl
                        ? location.state.previousUrl
                        : '/login'
                );
            return res;
        })
        .catch((e) => {
            console.log(e.response.data);
            if (e.response.data.username) {
                setUsernameError(e.response.data.username);
            }
            else {setUsernameError("");}
            if (e.response.data.password) {
                setPwd1Error(e.response.data.password);
            }
            else {setPwd1Error("");}
            if (e.response.data.non_field_errors) {
                setPwd2Error(e.response.data.non_field_errors);
            }
            else {setPwd2Error("");}
            if (e.response.data.email) {
                setEmailError(e.response.data.email);
            }
            else {setEmailError("");}
        })
    }
    return (
        
        <form className="form-container" id="cform" onSubmit={register}>
            <h3>Register Your Account</h3>
            <br/>
            <h6 style={{"color": "red"}}>*: required field</h6><br/>

            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="username">Username</label>
                    <label className="require-symbol" style={{"color": "red"}}>*</label>
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
                        required
                        placeholder="Enter your username"
                        style={{"textAlign": "center"}}
                    />
                </div>
                <p className="error-msg" style={{"color": "red", "marginTop": "10px"}}>{usernameError}</p>
            </div>
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="password">Password</label>
                    <label className="require-symbol" style={{"color": "red"}}>*</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="password"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="password"
                        value={password}
                        required
                        onChange={(e) => {
                            setPassword(e.target.value);
                        }}
                        placeholder="Enter your password"
                        style={{"textAlign": "center"}}
                    />
                </div>
                <p className="error-msg" style={{"color": "red", "marginTop": "10px"}}>{pwd1Error}</p>
            </div>

            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="password2">Password (again)</label>
                    <label className="require-symbol" style={{"color": "red"}}>*</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="password2"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="password"
                        value={password2}
                        required
                        onChange={(e) => {
                            setPassword2(e.target.value);
                        }}
                        placeholder="Re-enter your password"
                        style={{"textAlign": "center"}}
                    />
                </div>
                <p className="error-msg" style={{"color": "red", "marginTop": "10px"}}>{pwd2Error}</p>
            </div>

            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="email">Email</label>
                    <label className="require-symbol" style={{"color": "red"}}>*</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="email"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="email"
                        value={email}
                        required
                        onChange={(e) => {
                            setEmail(e.target.value);
                        }}
                        placeholder="Enter your email"
                        style={{"textAlign": "center"}}
                    />
                </div>
                <p className="error-msg" style={{"color": "red", "marginTop": "10px"}}>{emailError}</p>
            </div>

            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="first_name">First name</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="first_name"
                        type="text"
                        value={first}
                        onChange={(e) => {
                            setFirst(e.target.value);
                        }}
                        placeholder="Enter your first name"
                        style={{"textAlign": "center"}}
                    />
                </div>
            </div>
            <br/>
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="last_name">Last name</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="last_name"
                        type="text"
                        value={last}
                        onChange={(e) => {
                            setLast(e.target.value);
                        }}
                        placeholder="Enter your last name"
                        style={{"textAlign": "center"}}
                    />
                </div>
            </div>
            <br/>
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="phone_num">Phone number</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="phone_num"
                        type="text"
                        value={phone}
                        onChange={(e) => {
                            setPhone(e.target.value);
                        }}
                        placeholder="Enter your phone number"
                        style={{"textAlign": "center"}}
                    />
                </div>
            </div>
            <br/>
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="pmt_option">Membership Plan</label>
                </div>

                <div className="md:w-3/4">
                    <Form.Select className="choose_plan" id="pmt_option"
                    onChange={(e) => {
                        setPmt(e.target.value);
                    }}

                    style={{"width": "20%", "margin": "0 auto", "textAlign": "center"}}
                    >
                        <option>Choose a plan</option>
                    {memberships ? memberships.map((membership)=>{
                        if (membership.type === "M") {
                            return <option value="M">Monthly Plan ${membership.price}/mo</option>;
                        }
                        else {
                            return <option value="Y">Yearly Plan ${membership.price}/yr</option>;
                        }
                        }) : null
                    }
                    </Form.Select>                    
                </div>
                <br/>
                <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="avatar">Avatar</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="avatar"
                        accept="image/png, image/jpeg"
                        type="file"
                        // value={phone}
                        onChange={(e) => {
                            console.log(e.target.files[0]);
                            setAvatar(e.target.files[0]);
                        }}
                    />
                </div>
            </div>
            </div>
            <br/>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end" style={{"marginRight": "200px", "marginBottom": "200px"}}>
                <button class="btn btn-success me-md-2" type="submit">Register</button>
            </div>
            {/* <div className="error-msg">
                <p style={{color: "red"}}>{error}</p>
            </div> */}
        </form>
        
    );
}