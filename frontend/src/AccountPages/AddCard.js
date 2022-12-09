import { baseUrl } from "../base_url";
import { useState, useContext } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { LoginContext } from "../Contexts/LoginContext";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function AddCard() {
    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    const [cardNum, setCardNum] = useState("");
    const [billAddr, setBillAddr] = useState("");
    const [expDate, setExpDate] = useState("");
    const [cvv, setCvv] = useState("");

    const [cardNumError, setCardNumError] = useState([]);
    const [cvvError, setCvvError] = useState("");
    const [expDateError, setExpDateError] = useState("")


    const location = useLocation();
    const navigate = useNavigate();

    function redirect() {
        navigate(
            location?.state?.previousUrl
                ? location.state.previousUrl
                : '/profile'
          );
    }


    function addCard(e){
        e.preventDefault();
        const url = baseUrl + "account/add_payment_method/";

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: "Bearer " + localStorage.getItem("access"),
            },
            body: JSON.stringify({
                card_num: cardNum,
                billing_addr: billAddr,
                expires_at: expDate.toISOString().substring(0, 10),
                cvv: cvv,
            }),
        })
        .then((res) => {
            if (res.status === 401) {
                alert("Please login!")
            }
            else if (res.status === 201) {
                navigate(
                    location?.state?.previousUrl
                        ? location.state.previousUrl
                        : '/profile'
                  );
            }
            return res.json();           
        })
        .then((data)=>{
            console.log(data.card_num);
            localStorage.setItem("card_id", data.id);
            localStorage.setItem("billing_addr", data.billing_addr);
            localStorage.setItem("expires_at", data.expires_at);
            localStorage.setItem("card_num", data.card_num);

            if (data.card_num) {
                setCardNumError(data.card_num);
            }
            else {setCardNumError("");}
            if (data.cvv) {
                setCvvError(data.cvv);
            }
            else {setCvvError("");}
            if (data.non_field_errors) {
                setExpDateError(data.non_field_errors);
            }
            else {setExpDateError("");}
        })
        .catch((e)=>{
            console.log(e);
        })

        

    }
    return (
        <form className="m-2 w-full max-w-sm" id="customer" onSubmit={addCard}>
            <h3>Add Payment Method</h3>
            <br/>
            <h6 style={{"color": "red"}}>*: required field</h6><br/>
            
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="card-num">Card number</label>
                    <label className="require-symbol" style={{"color": "red"}}>*</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="card-num"
                        type="text"
                        value={cardNum}
                        onChange={(e) => {
                            setCardNum(e.target.value);
                        }}
                        required
                        placeholder="Enter your card number"
                    />
                </div>
                <p className="error-msg" style={{"color": "red", "marginTop": "10px"}}>{cardNumError}</p>
            </div>

            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="bill-addr">Billing address</label>
                    <label className="require-symbol" style={{"color": "red"}}>*</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="bill-addr"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="text"
                        value={billAddr}
                        required
                        onChange={(e) => {
                            setBillAddr(e.target.value);
                        }}
                        placeholder="Enter your billing address"
                    />
                </div>
            </div>
            <br/>
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="exp-date">Expiry date</label>
                    <label className="require-symbol" style={{"color": "red"}}>*</label>
                </div>

                <div className="md:w-3/4">
                    <DatePicker
                        id="exp-date"
                        className="pick-date"
                        selected = {expDate}
                        required
                        placeholderText = "Click to select a date"
                        onChange={(date) => {
                            console.log(date.toISOString().substring(0, 10));
                            setExpDate(date);
                        }}

                        
                    />
                </div>
                <p className="error-msg" style={{"color": "red", "marginTop": "10px"}}>{expDateError}</p>
            </div>
           
            <div className="md:flex md:items-center mb-6">
                <div className="md:w-1/4">
                    <label htmlFor="cvv">cvv</label>
                    <label className="require-symbol" style={{"color": "red"}}>*</label>
                </div>

                <div className="md:w-3/4">
                    <input
                        id="cvv"
                        className="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        type="text"
                        value={cvv}
                        required
                        onChange={(e) => {
                            setCvv(e.target.value);
                        }}
                        placeholder="Enter your 3-digit cvv"
                    />
                </div>
                <p className="error-msg" style={{"color": "red", "marginTop": "10px"}}>{cvvError}</p>
            </div>
            <br />
            <div className="d-grid gap-2 d-md-flex justify-content-md-end" style={{"marginRight": "200px", "marginBottom": "200px"}}>
            <button className="btn btn-secondary" type="button" onClick={redirect}>Cancel</button>
                <button className="btn btn-success me-md-2" type="submit">Add</button>
            </div>
        </form>
    );
}