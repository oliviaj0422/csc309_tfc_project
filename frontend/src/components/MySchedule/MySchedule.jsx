import React, { Component } from "react";
import { useEffect, useState } from "react";

const MySchedule = () => {
  const [classes, setClasses] = useState([]);

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [classID, setClassID] = useState("");
  const [drop, setDrop] = useState(0);
  const [dropInfo, setDropInfo] = useState("");
  const [drop1, setDrop1] = useState(0);
  const [y, setY] = useState(0);
  const [y1, setY1] = useState(0);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/classes/my_class_schedule/?page=${page}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("access"),
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setClasses(data.results);
        setTotalPages(data.count / 10);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, [page, y, y1]);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/classes/drop_class/${classID}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("access"),
      },
      body: JSON.stringify({}),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setDropInfo(data.detail);
        if (y === 0) setY(1);
        else setY(0);
        
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, [drop]);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/classes/drop_all_future_classes/${classID}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + localStorage.getItem("access"),
      },
      body: JSON.stringify({}),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setDropInfo(data.detail);
        if (y1 === 0) setY1(1);
        else setY1(0);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }, [drop1]);

  const click = () => {
    if (drop === 0) setDrop(1);
    else setDrop(0);
  };
  const click1 = () => {
    if (drop1 === 0) setDrop1(1);
    else setDrop1(0);
  };

  return (
    <React.Fragment>
      <h4>instance id of the class that you want to drop</h4>
      <input
        value={classID}
        onChange={(event) => setClassID(event.target.value)}
      />

      <button className="btn btn-primary btn-sm m-2" onClick={click}>
        Drop
      </button>

      <button className="btn btn-primary btn-sm m-2" onClick={click1}>
        Drop all future occurences of the class
      </button>

      <h4>{dropInfo}</h4>

      <table>
        <thead>
          <tr>
            <th>class name</th>
            <th>instance id</th>
            <th>start time</th>
            <th>end time</th>
          </tr>
        </thead>
        <tbody>
          {classes.map((classs) => (
            <tr key={classs.id}>
              <td>{classs.class_instance_name}</td>
              <td>{classs.class_instance}</td>
              <td>{classs.class_instance_start_time}</td>
              <td>{classs.class_instance_end_time}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {page > 1 ? (
        <button
          className="btn btn-primary btn-sm m-1"
          onClick={() => setPage(page - 1)}
        >
          prev
        </button>
      ) : (
        <></>
      )}
      {page < totalPages ? (
        <button
          className="btn btn-primary btn-sm m-1"
          onClick={() => setPage(page + 1)}
        >
          next
        </button>
      ) : (
        <></>
      )}
    </React.Fragment>
  );
};

export default MySchedule;
