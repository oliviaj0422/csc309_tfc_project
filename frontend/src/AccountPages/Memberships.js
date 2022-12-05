import { useEffect, useState, useContext } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { baseUrl } from "../base_url";
import "../App.css"

export default function Memberships() {
    const [memberships, setMemberships] = useState();
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
            <h1>The subscription plans are</h1> <br />
            {memberships ? memberships.map((membership)=>{
                if (membership.type == "M") {
                    return <p>The monthly plan is {membership.price}</p>;
                }
                else {
                    return <p>The yearly plan is {membership.price}</p>;
                }
            }) : null}
        </>
    );
}