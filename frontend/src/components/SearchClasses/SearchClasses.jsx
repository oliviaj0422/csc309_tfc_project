import React, { Component } from "react";
import { useEffect, useState } from "react";
import ClassName from "../ClassSearch/ClassName";
import CoachName from "../ClassSearch/CoachName";
import Date from "../ClassSearch/Date";
import TimeRange from "../ClassSearch/TimeRange";
const SearchClasses = () => {

    return(
        <React.Fragment>
            <center>
                <ClassName />
                <br></br>
                <CoachName />
                <br></br>
                <Date />
                <br></br>
                <TimeRange />
            </center>
        </React.Fragment>
    )


};

export default SearchClasses;
