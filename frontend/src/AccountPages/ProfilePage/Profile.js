import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { baseUrl } from "../../base_url";
import { Modal, Nav, Image, Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import "./style.css";

export default function PersonalProfile() {

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [first, setFirst] = useState("");
  const [last, setLast] = useState("");
  const [phone, setPhone] = useState("");
  const [pmt, setPmt] = useState("");
  const [avatar, setAvatar] = useState(null);
  const [show, setShow] = useState(false);
  const [toDelete, setToDelete] = useState(false);
  const [cardNum, setCardNum] = useState(localStorage.getItem("card_num"));

  const [error, setError] = useState("");

  const navigate = useNavigate();
  const location = useLocation();

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const redirectProfile = () => {
    navigate(
      location?.state?.previousUrl
          ? location.state.previousUrl
          : '/profile/edit'
    );
  }

  const redirectAddCard = () => {
    navigate(
      location?.state?.previousUrl
          ? location.state.previousUrl
          : '/add-card'
    );
  }

  const redirectUpdateCard = () => {
    navigate(
      location?.state?.previousUrl
          ? location.state.previousUrl
          : '/update-card'
    );
  }

  const redirectViewPayments = () => {
    navigate(
      location?.state?.previousUrl
          ? location.state.previousUrl
          : '/payment-history'
    );
  }

  const redirectClassHistory = () => {
    navigate(
      location?.state?.previousUrl
          ? location.state.previousUrl
          : '/my_class_history'
    );
  }

  const redirectClassSched = () => {
    navigate(
      location?.state?.previousUrl
          ? location.state.previousUrl
          : '/my_schedule'
    );
  }

  useEffect(() => {
    const url3 = baseUrl + `account/${localStorage.getItem("card_id")}/profile/delete_card/`
    if (toDelete) {
    fetch(url3, {
      method: "DELETE",
      headers: {
        Authorization: "Bearer " + localStorage.getItem("access"),
      }
    })
    .then(res=>res.json())
    .catch(error => console.log("Error: " + error))
  }
  }, [toDelete])


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
          setEmail(data.email);
          setFirst(data.first_name);
          setLast(data.last_name);
          setAvatar(data.avatar);
          setPhone(data.phone_num);
          setPmt(data.pmt_option);
        })
      
  }, [])


  return (
    // template: bootstrap
    <>
      <h3 style={{"textAlign": "center"}}>Profile</h3><br/>

      <div className="d-grid gap-2 d-md-flex justify-content-md-end" style={{"margin-right": "150px"}}>
        <Button variant="outline-primary" type="button" onClick={redirectProfile} style={{"marginRight": "20px"}}>Edit Profile</Button>
        <Button variant="outline-primary" type="button" onClick={redirectAddCard} style={{"marginRight": "20px"}}>Change Card</Button>
        <Button variant="outline-primary" type="button" onClick={redirectViewPayments} style={{"marginRight": "20px"}}>View Payment History</Button>
        <Button variant="outline-primary" type="button" onClick={redirectClassSched} style={{"marginRight": "20px"}}>My Class Schedule</Button>
        <Button variant="outline-primary" type="button" onClick={redirectClassHistory} style={{"marginRight": "20px"}}>My Class History</Button>
      </div>
      <br/>

    <br/>
    <div className="container">
    <Image src={avatar} img="rounded"></Image>
    <br/>
    <br/>
    <div className="mb-3 row">
      <label htmlFor="staticUsername" className="col-sm-2 col-form-label">Username</label>
    <div className="col-sm-10">
      <input type="text" readOnly className="form-control-plaintext" id="staticUsername" value={username} />
    </div>
    </div>
    <div className="mb-3 row">
      <label htmlFor="staticEmail" className="col-sm-2 col-form-label">Email</label>
    <div className="col-sm-10">
      <input type="text" readOnly className="form-control-plaintext" id="staticEmail" value={email} />
    </div>
    </div>
    <div className="mb-3 row">
      <label htmlFor="staticFirst" className="col-sm-2 col-form-label">First name</label>
    <div className="col-sm-10">
      <input type="text" readOnly className="form-control-plaintext" id="staticFirst" value={first} />
    </div>
    </div>
    <div className="mb-3 row">
      <label htmlFor="staticLast" className="col-sm-2 col-form-label">Last name</label>
    <div className="col-sm-10">
      <input type="text" readOnly className="form-control-plaintext" id="staticLast" value={last} />
    </div>
    </div>
    <div className="mb-3 row">
      <label htmlFor="staticPhone" className="col-sm-2 col-form-label">Phone</label>
    <div className="col-sm-10">
      <input type="text" readOnly className="form-control-plaintext" id="staticPhone" value={phone} />
    </div>
    </div>
    <div className="mb-3 row">
      <label htmlFor="staticPlan" className="col-sm-2 col-form-label">Subscription</label>
    <div className="col-sm-10">
      <input type="text" readOnly className="form-control-plaintext" id="staticPlan" value={pmt} />
    </div>
    </div>

      <div className="mb-3 row">
        <label htmlFor="staticPmt" className="col-sm-2 col-form-label">Payment method</label>
          <div className="col-sm-10">
            <input type="text" readOnly className="form-control-plaintext" id="staticPmt" value={cardNum} />
          </div>
          <br/>
      </div>

      <div className="d-grid gap-2 d-md-flex justify-content-md-end" style={{"marginBottom": "200px"}}>
        <button className="btn btn-primary me-md-2" type="button" onClick={redirectUpdateCard}>Edit Payment Method</button>
        <button className="btn btn-primary me-md-2" data-bs-toggle="modal" data-bs-target="#exampleModal" type="button" onClick={handleShow}>Delete Payment Method</button>
        
      </div>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Delete Confirmation</Modal.Title>
        </Modal.Header>
        <Modal.Body>Are you sure you want to delete the current payment method?</Modal.Body>
        <Modal.Footer>
          <button className="btn btn-secondary"  onClick={handleClose}>
            Cancel
          </button>
          <button className="btn btn-danger" variant="primary" onClick={()=>{
            setToDelete(true);
            setShow(false);
            setCardNum("No payment method")
            }}>
            Delete
          </button>
        </Modal.Footer>
      </Modal>
    </div>

    </>

  );
    
  
}