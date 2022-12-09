import { useEffect, useState, useContext } from 'react';
import { baseUrl } from "../base_url";
import { LoginContext } from "../Contexts/LoginContext";
import { useNavigate, useLocation } from 'react-router-dom';
import "../App.css"
import "./PaymentTable/style.css"
import { Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

export default function PaymentHistory() {
    const [loggedIn, setLoggedIn] = useContext(LoginContext);
    const [history, setHistory] = useState([]);
    const [page, setPage] = useState(1);
    const [msg, setMsg] = useState("");
    const [totalPages, setTotalPages] = useState(1);
    const [error, setError] = useState("");

    const navigate = useNavigate();
    const location = useLocation();

    function redirect() {
        navigate(
            location?.state?.previousUrl
                ? location.state.previousUrl
                : '/profile'
          );
    }

    useEffect(() => {
        const url = baseUrl + `/account/payment_history/?page=${page}`;
        console.log("Fetching...");
        fetch(url, {
            headers: {
            Authorization: "Bearer " + localStorage.getItem("access"),
            },
        })
        .then((response) => {
            if (response.status === 401) {
                setError("Please login first!");
            }
            return response.json()
        }
        )
        .then((data) => {
            console.log(data.results);
            setHistory(data.results);
            setTotalPages(data.count / 10);
            
        })
    }, [page]);
    

    return (
        <>
            <h3>Payment History</h3> <br />


            <table>
                <thead>
                <tr>
                    <th>Refrence #</th>
                    <th>Amount</th>
                    <th>Card number</th>
                    <th>Payment date</th>
                    <th>Recurrence</th>
                    <th>End date</th>
                    <th>Payment status</th>
                </tr>
                </thead>
                
                <tbody>
                {history.length>0 ? history.map((h) => {
                    return <tr key={h.id}>
                    <td>{h.id}</td>    
                    <td>{h.amount}</td>
                    <td>{h.pmt_method}</td>
                    <td>{h.pmt_date}</td>
                    <td>{h.recur}</td>
                    <td>{h.edate}</td>
                    <td>{h.pmt_status}</td>
                    </tr>
                }) : <div>You have no payments.</div>}
                </tbody>
            </table>
            <br/>

            <div style={{"marginBottom": "200px"}}>
            <button
                className="btn btn-outline-primary btn-sm m-1"
                onClick={redirect}
                >
                Back To Profile
                </button>

            {page > 1 ? (
                <button
                className="btn btn-primary btn-sm m-1"
                onClick={() => setPage(page - 1)
                }
                >
                Prev
                </button>
            ) : (
                <></>
            )}
            {page < totalPages ? (
                <button
                className="btn btn-primary btn-sm m-1"
                onClick={() => setPage(page + 1)}
                >
                Next
                </button>
            ) : (
                <></>
            )}
            </div>

            <p>{msg}</p>

            <div className="error-msg">
                <p style={{color: "red"}}>{error}</p>
            </div>
            
        </>
    );
}