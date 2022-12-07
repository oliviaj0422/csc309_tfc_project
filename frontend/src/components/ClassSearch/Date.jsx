import React, { Component } from "react";
import { useEffect, useState } from "react";

const Date = () => {
    const [classes, setClasses] = useState([]);

    //const [query, setQuery] = useState({ page: 1, studioName: "" });
    const [studioName, setStudioName] = useState("")
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)
    const [year, setYear] = useState("")
    const [month, setMonth] = useState("")
    const [day, setDay] = useState("")

    
    useEffect(() => {
      fetch(
        `http://127.0.0.1:8000/classes/search_or_filter_3/${studioName}/${year}/${month}/${day}/?page=${page}`
      )
        .then((res) => res.json())
        .then((json) => {
          setClasses(json.results)
          setTotalPages(json.count/10)       
        })
        
    }, [studioName, year, month, day, page]);
  
  
    return (
      <React.Fragment>
        <h3>Search By Date</h3>
        <h4>studio name</h4>
  
        <input
          value={studioName}
          onChange={event => setStudioName(event.target.value)}
        />
  
        <h4>year</h4>
        <input
          value={year}
          onChange={event => setYear(event.target.value)}
        />

        <h4>month</h4>
        <input
          value={month}
          onChange={event => setMonth(event.target.value)}
        />

        <h4>day</h4>
        <input
          value={day}
          onChange={event => setDay(event.target.value)}
        />
        
  
        <table>
          <thead>
            <tr>
              <th>class name</th>
              <th>instance id</th>
              <th>start time</th>
            </tr>
          </thead>
          <tbody>
            {classes.map((classs) => (
              <tr key={classs.id}>
                
                <td>{classs.class_name}</td>
                <td>{classs.id}</td>
                <td>{classs.start_time}</td>

                
              </tr>
            ))}
          </tbody>
        </table>
  
        {page>1 ? <button className="btn btn-primary btn-sm m-1" onClick={()=>setPage(page-1)}>prev</button> : <></>}
        {page < totalPages? <button className="btn btn-primary btn-sm m-1" onClick={()=>setPage(page+1)}>next</button> : <></>}
      </React.Fragment>
    ); 
  
};

export default Date;