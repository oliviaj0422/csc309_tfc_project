import React, { Component } from "react";
import { useEffect, useState } from "react";
import ClassName from "../ClassSearch/ClassName";
import CoachName from "../ClassSearch/CoachName";
import Date from "../ClassSearch/Date";
import TimeRange from "../ClassSearch/TimeRange";
const SearchClasses = () => {

    return(
        <React.Fragment>
            <ClassName />
            <CoachName />
            <Date />
            <TimeRange />
        </React.Fragment>
    )


};

export default SearchClasses;
