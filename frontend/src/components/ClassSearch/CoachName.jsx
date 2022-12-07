import React, { Component } from "react";
import { useEffect, useState } from "react";

const CoachName = () => {
    const [classes, setClasses] = useState([]);

    //const [query, setQuery] = useState({ page: 1, studioName: "" });
    const [studioName, setStudioName] = useState("")
    const [page, setPage] = useState(1)
    const [totalPages, setTotalPages] = useState(1)
    const [coachName, setCoachName] = useState("")

    
    useEffect(() => {
      fetch(
        `http://127.0.0.1:8000/classes/search_or_filter_2/${studioName}/${coachName}/?page=${page}`
      )
        .then((res) => res.json())
        .then((json) => {
          setClasses(json.results)
          setTotalPages(json.count/10)       
        })
        
    }, [studioName, coachName, page]);
  
  
    return (
      <React.Fragment>
        <h3>Search By Coach Name</h3>
        <h4>studio name</h4>
  
        <input
          value={studioName}
          onChange={event => setStudioName(event.target.value)}
        />
  
        <h4>coach name</h4>
        <input
          value={coachName}
          onChange={event => setCoachName(event.target.value)}
        />
        
  
        <table>
          <thead>
            <tr>
              <th>class name</th>
              <th>instance id</th>
              <th>coach name</th>
            </tr>
          </thead>
          <tbody>
            {classes.map((classs) => (
              <tr key={classs.id}>
                
                <td>{classs.class_name}</td>
                <td>{classs.id}</td>
                <td>{classs.coach}</td>
                
              </tr>
            ))}
          </tbody>
        </table>
  
        {page>1 ? <button className="btn btn-primary btn-sm m-1" onClick={()=>setPage(page-1)}>prev</button> : <></>}
        {page < totalPages? <button className="btn btn-primary btn-sm m-1" onClick={()=>setPage(page+1)}>next</button> : <></>}
      </React.Fragment>
    ); 
  
};

export default CoachName;