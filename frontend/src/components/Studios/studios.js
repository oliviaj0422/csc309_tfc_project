// import logo from "./mylogo.svg"
import { useState, useEffect } from "react";
import { GoogleMap, LoadScript, Marker } from "@react-google-maps/api";
import { getArticleList, getQueryList, getDistance } from "../../utils/api";
import { NavLink } from "../NavBarElem/NavBar";
import "./studios.css";

const containerStyle = {
  width: "100%",
  height: "100%",
};

function getPosition() {
  var pos = {
    lat: 51.502745,
    lon: -0.103739,
  };
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function (position) {
        pos = {
          lat: position.coords.latitude || 51.502745,
          lon: position.coords.longitude || -0.103739,
        };
      },
      function () {
      }
    );
  }
  return pos;
}

function App() {
  let posNum = getPosition();

  const [inputValue, setInputValue] = useState("");


  const [pageNum, setPageNum] = useState(1);


  const [position, setPosition] = useState({
    lat: posNum.lat,
    lng: posNum.lon,
  });


  const [toSearch, setToSearch] = useState(false);


  const [showMask, setShowMask] = useState(true);

  const [showMaskInfo, setShowMaskInfo] = useState({});


  const [isShowFilter, setIsShowFilter] = useState(false);
  const filterLabel = ["Hot yoga", "Pool", "Yoga", "Squash", "Turf Zone",
    "Tanning", "Massage Chairs", "Steam Room", "MindDen", "NinjaFit", "Group Cycling",
  "Recovery Room", "Peak", "REGYMEN", "CRAFTBOXING"];

  const [clubList, setClubList] = useState([]);
  function getClubList() {
    let data = {
      page: pageNum,
      lon: posNum.lon,
      lat: posNum.lat,
    };
    getArticleList(data).then((res) => {
      const re = res.data;
      re.map((item) => {
        getDistance({
          x1: posNum.lon,
          y1: posNum.lat,
          x2: item.geolocation.split(",")[1],
          y2: item.geolocation.split(",")[0],
        }).then((res) => {
          item.distance = res.details.toFixed(2) + "km";
          setClubList(re);
        });
        return item;
      });
      console.log(re);
    });
  }
  useEffect(() => {
    getClubList();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pageNum]);
  useEffect(() => {
    getClubList();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  const [markesList, setMarkesList] = useState([]);

  useEffect(() => {
    let data = {
      page: pageNum,
      lon: posNum.lon,
      lat: posNum.lat,
    };
    getArticleList(data).then((res) => {
      let mkList = [];
      res.data.forEach((item) => {
        mkList.push({
          lat: Number(item.geolocation.split(",")[0]),
          lng: Number(item.geolocation.split(",")[1]),
        });
      });
      setMarkesList(mkList);
    });
  }, []);

  useEffect(() => {
    let data = {
      key: inputValue,
      page: pageNum,
      lon: posNum.lon,
      lat: posNum.lat,
    };
    getQueryList(data).then((res) => {
      setClubList(res.Result);
    });
  }, [toSearch]);

  function handleSearch(item) {
    setInputValue(item);
    setToSearch(!toSearch);
  }

  function goPosition(data) {
    let geolocation = {
      lat: Number(data.split(",")[0]),
      lng: Number(data.split(",")[1]),
    };
    setPosition(geolocation);
  }

  function handlePage(type) {
    let mewPageNum = pageNum;
    switch (type) {
      case "up":
        if (mewPageNum > 1) {
          setPageNum(mewPageNum - 1);
        }
        break;
      case "down":
        setPageNum(mewPageNum + 1);
        break;
      // no default
    }
  }

  let checkedItem = [];

  let filterData = [];

  function handleFilter(e, txt) {
    if (e.target.checked) {

      checkedItem.push(txt);
      clubList.forEach((item) => {
        let amenitiestype = item.amenitiestype.split(",");

        if (amenitiestype.indexOf(txt) !== -1) {
          filterData.push(item);
        }
      });
      setClubList(filterData);
    } else {

      clubList.forEach((item) => {
        let amenitiestype = item.amenitiestype.split(",");
        if (amenitiestype.indexOf(txt) !== -1) {
          filterData.push(item);
        }
      });
      let newClubList = clubList.filter((item) => {
        return filterData.indexOf(item) === -1;
      });
      if (newClubList.length === 0) {
        getClubList();
      } else {
        setClubList(newClubList);
      }
    }
  }

  function handleGoModal(item) {
    let scrollLock = document.body;
    if (item.address) {
      setShowMask(false);
      scrollLock.style.overflow = "hidden";
    } else {
      setShowMask(true);
      scrollLock.style.overflow = "auto";
    }
    setShowMaskInfo(item);
  }

  return (
    <>
      <div className="page2" style={{ display: showMask ? "none" : "block" }}>
        {/* <div className="mask"></div> */}
        <div className="page-content">
          <div
            className="page-back"
            onClick={() => {
              handleGoModal({});
            }}
          ></div>
          <div className="title">Studios Info</div>
          <div className="page-info">
            <div className="page-left">
              {/* <img src='https://img.homejournal.com/202004/5ea6766c2f244.jpg' /> */}
              <img src={showMaskInfo.imagelist} />
            </div>
            <div className="page-right">
              <div className="page-info-item">
                Address: {showMaskInfo.address}
              </div>
              <div className="page-info-item">
                phoneNumber: {showMaskInfo.phonenumber}
              </div>
              <div className="page-info-item">
                postalCode: {showMaskInfo.postalcode}
              </div>
              <div className="page-info-item">
                distance: {showMaskInfo.distance}
              </div>
              <div className="page-info-item">
                amenitiesType: {showMaskInfo.amenitiestype}
              </div>
              <div className="page-info-item">
                amenitiesQuantity: {showMaskInfo.amenitiesquantity}
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="main">
        <div
          className="filter"
          style={{ display: isShowFilter ? "block" : "none" }}
        >
          <div className="filter-title">
            <div className="filter-name">FILTERS</div>
            <div
              className="filter-btn"
              onClick={() => {
                setIsShowFilter(false);
              }}
            >
              ×
            </div>
          </div>
          <div className="filter-subtitle">Amenities</div>
          <div>
            {filterLabel.map((item, index) => (

              <div className="filter-item" key={index}>
                <div className="filter-item">
                  <input
                    type="checkbox"
                    onClick={(e) => {
                      handleFilter(e, item);
                    }}
                  />
                  {item}
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="title">Find a Studio</div>

        <div className="search">
          <div className="search-main">
            <input
              type="text"
              className="search-input"
              placeholder="Search by address, postal code, etc."
              value={inputValue}
              onChange={(e) => {
                setInputValue(e.target.value);
              }}
            />
            <div
              className="search-btn"
              onClick={() => {
                setToSearch(!toSearch);
              }}
            >
              SEARCH
            </div>
          </div>
          <div
            className="filters-btn"
            onClick={() => {
              setIsShowFilter(true);
            }}
          >
            FILTERS
          </div>
        </div>
        <div className="page-options">
          <div
            className="page-btn"
            onClick={() => {
              handlePage("up");
            }}
          >
            &lt;
          </div>
          <div className="page-num">{pageNum}</div>
          <div
            className="page-btn"
            onClick={() => {
              handlePage("down");
            }}
          >
            &gt;
          </div>
        </div>
        <div className="club-map">
          <div className="club-list">
            {clubList.map((item, index) => (
              
              <div className="club-item" key={index + "club"}>
                <div className="club-title">
                  <div
                    className="club-name"
                    onClick={() => {
                      handleGoModal(item);
                    }}
                  >
                    Studio Name: {item.name}
                  </div>
                  <div
                    className="club-icon"
                    onClick={() => {
                      goPosition(item.geolocation);
                    }}
                  >
                    !
                  </div>
                </div>
                <div className="small-text">Address: {item.address}</div>
                <div className="small-text">
                  Phone Number: {item.phonenumber}
                </div>
                <div className="small-text">Postal Code: {item.postalcode}</div>
                <div className="small-text">Distance: {item.distance}</div>
                <div className="small-text">
                  Amenities Type: {item.amenitiestype}
                </div>
                <div className="small-text">
                  Amenities Quantity: {item.amenitiesquantity}
                </div>
                <div className="club-btn-list">
                  <div className="btn-left">
                    <a
                      href={
                        "https://www.google.com/maps/dir/?api=1&destination=" +
                        position.lat +
                        "," +
                        position.lng
                      }
                      target="_blank"
                      class="c-btn-outlined c-btn-outlined--gray"
                    >
                      <span class="c-btn__label">DIRECTIONS</span>
                    </a>
                  </div>
                  <div className="btn-right">
                    <NavLink to={"/classes/?name=" + item.name}>
                      CLASS SCHEDULE
                    </NavLink>
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="map-main">
            <LoadScript googleMapsApiKey="AIzaSyDXZEaujucVUNx7EaD4Prxx1VBQPvhe4ow">
              <GoogleMap
                mapContainerStyle={containerStyle}
                center={position}
                zoom={18}
              >
                {markesList.map((item, index) => (
                  <Marker key={index + "marker"} position={item} />
                ))}
                <Marker position={position} />
              </GoogleMap>
            </LoadScript>
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
