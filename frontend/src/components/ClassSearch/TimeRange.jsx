import React, { Component } from "react";
import { useEffect, useState } from "react";

const TimeRange = () => {
    const [classes, setClasses] = useState([]);

    //const [query, setQuery] = useState({ page: 1, studioName: "" });
    const [studioName, setStudioName] = useState("")
    const [hour1, setHour1] = useState(0)
    const [minute1, setMinute1] = useState(0)
    const [hour2, setHour2] = useState(0)
    const [minute2, setMinute2] = useState(0)

    
    useEffect(() => {
      fetch(
        `http://127.0.0.1:8000/classes/search_or_filter_4/${studioName}/${hour1}/${minute1}/${hour2}/${minute2}/`
      )
        .then((res) => res.json())
        .then((json) => {
          setClasses(json.detail)      
        })
        
    }, [studioName,hour1,minute1,hour2,minute2]);
  
  
    return (
      <React.Fragment>
        <h3>Search By Time Range</h3>
        <h4>studio name</h4>
  
        <input
          value={studioName}
          onChange={event => setStudioName(event.target.value)}
        />

        <h4>hour1</h4>
        <input
          value={hour1}
          onChange={event => setHour1(event.target.value)}
        />

        <h4>minute1</h4>
        <input
          value={minute1}
          onChange={event => setMinute1(event.target.value)}
        />

        <h4>hour2</h4>
        <input
          value={hour2}
          onChange={event => setHour2(event.target.value)}
        />

        <h4>minute2</h4>
        <input
          value={minute2}
          onChange={event => setMinute2(event.target.value)}
        />
        
        <h4>The class instances that are in the time range (i.e. hour1:minute1 - hour2:minute2):</h4>

        <ul>
        {classes.map((classs) => (
          <li key={classs}>{classs}</li>
        ))}
        </ul>
      </React.Fragment>
    ); 
  
};

export default TimeRange;