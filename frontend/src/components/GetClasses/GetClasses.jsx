import React, { Component } from "react";
import { useEffect, useState } from "react";
import "./style.css";
import Input from "../Input";

const GetClasses = () => {
  const [classes, setClasses] = useState([]);

  //const [query, setQuery] = useState({ page: 1, studioName: "" });
  const [studioName, setStudioName] = useState("")
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [classID, setClassID] = useState(null)

  useEffect(() => {
    fetch(
      `http://127.0.0.1:8000/classes/${studioName}/get_classes/?page=${page}`
    )
      .then((res) => res.json())
      .then((json) => {
        setClasses(json.results)
        setTotalPages(json.count/3)       
      })
      
  }, [studioName, page]);

  return (
    <React.Fragment>
      <h3>Studio Name</h3>

      <input
        value={studioName}
        onChange={event => setStudioName(event.target.value)}
      />

      <h4>ClassID of the class that you want to enrol</h4>
      <input
        value={classID}
        onChange={event => setClassID(event.target.value)}
      />
      <button className="btn btn-primary btn-sm m-2">Enrol</button>

      <table>
        <thead>
          <tr>
            <th>id</th>
            <th>class name</th>
            <th>description</th>
            <th>coach</th>
            <th>keywords</th>
            <th>space availability</th>
            <th>start time</th>
            <th>end time</th>
          </tr>
        </thead>
        <tbody>
          {classes.map((classs) => (
            <tr key={classs.id}>
              <td>{classs.id}</td>
              <td>{classs.class_name}</td>
              <td>{classs.description}</td>
              <td>{classs.coach}</td>
              <td>{classs.keywords}</td>
              <td>{classs.space_availability}</td>
              <td>{classs.start_time}</td>
              <td>{classs.end_time}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {page>1 ? <button onClick={()=>setPage(page-1)}>prev</button> : <></>}
      {console.log("page is" + page)}
      {console.log("total pages is" + totalPages)}
      {page < totalPages? <button onClick={()=>setPage(page+1)}>next</button> : <></>}
    </React.Fragment>
  );
};

export default GetClasses;


