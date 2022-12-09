import { baseUrl } from "../base_url";
import { useState, useEffect, useContext } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { LoginContext } from "../Contexts/LoginContext";
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import "../App.css";
import { Form } from 'react-bootstrap';

export default function EditProfile() {

    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [first, setFirst] = useState("");
    const [last, setLast] = useState("");
    const [phone, setPhone] = useState("");
    const [pmt, setPmt] = useState("");
    const [avatar, setAvatar] = useState(null);
    const [memberships, setMemberships] = useState(null);

    const [error, setError] = useState("");

    const location = useLocation();
    const navigate = useNavigate();

    function redirect() {
        navigate(
            location?.state?.previousUrl
                ? location.state.previousUrl
                : '/profile'
          );
    }

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

    useEffect(() => {
        const url2 = baseUrl + `account/${localStorage.getItem("id")}/profile/`;
        fetch(url2, {
          headers: {
            Authorization: "Bearer " + localStorage.getItem("access"),
          }
        })
        .then((res) => {
          return res.json()
        })
        .then((data) => {
          console.log(data);
          setUsername(data.username);
          setPassword(data.password);
          setEmail(data.email);
          setFirst(data.first_name);
          setLast(data.last_name);
          setAvatar(data.avatar);
          setPhone(data.phone_num);
          setPmt(data.pmt_option);
        })
    }, [])


    function edit(e) {

        e.preventDefault();
        const url = baseUrl + `account/${localStorage.getItem("id")}/profile/edit/`;
    
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('email', email);
        formData.append('first_name', first);
        formData.append('last_name', last);
        formData.append('phone_num', phone);
        formData.append('pmt_option', pmt);
        formData.append('avatar', avatar);
    
        axios.patch(url, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
                Authorization: "Bearer " + localStorage.getItem("access"),
            }
            }).then((res) => {
            console.log(res);
            if (res.status === 200)
                navigate(
                    location?.state?.previousUrl
                        ? location.state.previousUrl
                        : '/profile'
                );
            })
            .catch((e)=>{
                console.log(e);
            })
    
      }
    
    return (
        <>
        <form className="form-container" id="cform" onSubmit={edit}>
            <h3>Edit Profile</h3><br/>
            <div className="md:flex md:items-center mb-6">
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
                    />
                </div>
            </div>
            <br/>
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
                    />
                </div>
            </div>
            <br/>
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="email">Email</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="email"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="email"
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value);
                        }}
                        placeholder="Enter your email"
                    />
                </div>
            </div>
            <br/>
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
                        <option>Choose an option</option>
                    {memberships ? memberships.map((membership)=>{
                        if (membership.type === "M") {
                            return <option value="M">Monthly Plan {membership.price}</option>;
                        }
                        else {
                            return <option value="Y">Yearly Plan {membership.price}</option>;
                        }
                        }) : null
                    }
                        <option value="N">Cancel subscription</option>
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

            <div class="d-grid gap-2 d-md-flex justify-content-md-end" style={{"margin-right": "200px", "margin-bottom": "200px"}}>
                <button class="btn btn-secondary" type="button" onClick={redirect}>Cancel</button>
                <button class="btn btn-success" type="submit">Submit</button>
            </div>
            <div className="error-msg">
                <p style={{color: "red"}}>{error}</p>
            </div>
        </form>
        </>
    );
}