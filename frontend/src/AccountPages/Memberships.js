import { useEffect, useState } from 'react';
import { baseUrl } from "../base_url";
import "../App.css"
import "./PaymentTable/style.css"
import 'bootstrap/dist/css/bootstrap.min.css';
import image1 from "../images/web-hero-crop.jpeg"
import image2 from "../images/web-latpulldown.jpeg"

export default function Memberships() {

    const [memberships, setMemberships] = useState([]);

    useEffect(() => {
        const url = baseUrl + "memberships/";
        console.log("Fetching...");
        fetch(url)
        .then((response) => response.json())
        .then((data) => {
            console.log(data);
            setMemberships(data.results);
        })
    }, []);

    return (
        <>
            <div className="title-name" style={{"textAlign": "center"}}>
            <h3>Choose Your Membership</h3> 
            </div>

            <div className="plan-container">
            {memberships.length > 0 ? memberships.map((membership)=>{
                if (membership.type == "M") {
                    return <div className="card" style={{"width": "25rem", "margin": "50px auto"}}>
                        <img src={image2} class="card-img-top" alt="..."></img>
                    <div className="card-body">
                        <h4 className="card-title">Monthly Plan</h4>
                        <h5 className="card-subtitle mb-2 text-muted">${membership.price}/month</h5>
                        <p className="card-text">With more than 200 clubs across Canada, we've got what you need, where and when you need it.</p>
                        <a href="/register" class="btn btn-danger">JOIN US</a>
        
                    </div>
                    <br/>
                </div>;
                }
                else if (membership.type == "Y"){
                    return <div className="card" style={{"width": "25rem", "margin": "50px auto"}}>
                    <img src={image1} class="card-img-top" alt="..."></img>

                    <div className="card-body">
                        <h4 className="card-title">Yearly Plan</h4>
                        <h5 className="card-subtitle mb-2 text-muted">${membership.price}/year</h5>
                        <p className="card-text">With more than 200 clubs across Canada, we've got what you need, where and when you need it.</p>
                        <a href="/register" class="btn btn-danger">JOIN US</a>
    
                    </div>
                </div>;
                }
            }) : null}
            </div>
        </>
    );
}