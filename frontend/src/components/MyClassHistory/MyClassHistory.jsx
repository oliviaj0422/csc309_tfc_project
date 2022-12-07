import React, { Component } from "react";
import { useEffect, useState } from "react";

const MyClassHistory = () => {
  const [classes, setClasses] = useState([]);

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/classes/my_class_history/?page=${page}`, {
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
  }, [page]);

  return (
    <React.Fragment>
      <h2>My Class History</h2>

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
        <button className="btn btn-primary btn-sm m-1" onClick={() => setPage(page - 1)}>prev</button>
      ) : (
        <></>
      )}
      {page < totalPages ? (
        <button className="btn btn-primary btn-sm m-1" onClick={() => setPage(page + 1)}>next</button>
      ) : (
        <></>
      )}
    </React.Fragment>
  );
};

export default MyClassHistory;
