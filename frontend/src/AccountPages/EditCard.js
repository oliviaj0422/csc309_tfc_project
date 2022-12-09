import { baseUrl } from "../base_url";
import { useState, useContext } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { LoginContext } from "../Contexts/LoginContext";
import DatePicker from "react-datepicker";
import 'bootstrap/dist/css/bootstrap.min.css';
import "../App.css";

export default function UpdateCard() {

    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    
    const [billAddr, setBillAddr] = useState(localStorage.getItem("billing_addr"));
    const [expDate, setExpDate] = useState("");

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

    function editCard(e) {

        e.preventDefault();
        const url = baseUrl + `account/${localStorage.getItem("card_id")}/profile/update_card_info/`;
    
        fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                Authorization: "Bearer " + localStorage.getItem("access"),
            },
            body: JSON.stringify({
                billing_addr: billAddr,
                expires_at: expDate.toISOString().substring(0, 10),
            }),
        })
        .then((res) => {
            if (res.status === 401) {
                setError("Please login first!")
            }
            else if (res.status === 200) {
                navigate(
                    location?.state?.previousUrl
                        ? location.state.previousUrl
                        : '/profile'
                  );
            }
            return res.json();           
        })
    
      }
    
    return (
        <>
        <form className="form-container" id="cform" onSubmit={editCard}>
            <h3>Update Card Info</h3><br/>
            <h6 style={{"color": "green"}}>If you want to change your card number or cvv code, please add a new payment method.</h6>
            <br />
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="bill-addr">Billing Address</label><br/>
                </div>

                <div className="md:w-3/4">
                    <input
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="bill-addr"
                        type="text"
                        value={billAddr}
                        onChange={(e) => {
                            setBillAddr(e.target.value);
                        }}
                        placeholder="Enter your new billing address"
                        style = {{"textAlign": "center"}}
                    />
                </div>
            </div>
            <br />
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="exp-date">Expiry Date</label>
                </div>

                <div className="md:w-3/4">
                    <DatePicker
                        id="exp-date"
                        className="pick-date"
                        selected = {expDate}
                        required
                        dateFormat="yyyy-MM-dd"
                        placeholderText = "Click to select a date"
                        onChange={(date) => {
                            console.log(date.toISOString().substring(0, 10));
                            setExpDate(date);
                        }}
                        style = {{"textAlign": "center"}}
                    />
                </div>
            </div>
            <br />
            <br />
            <div class="d-grid gap-2 d-md-flex justify-content-md-end" style={{"margin-right": "34%", "margin-bottom": "200px"}}>
                <button class="btn btn-secondary" type="button" onClick={redirect}>Cancel</button>
                <button class="btn btn-primary" type="button">Add New Payment Method</button>
                <button class="btn btn-success" type="submit">Submit</button>
            </div>
            <div className="error-msg">
                <p style={{color: "red"}}>{error}</p>
            </div>
        </form>
        </>
    );
}