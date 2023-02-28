import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { AuthContext } from "../../contexts/AuthContext";
import { Tabs, Tab } from "react-bootstrap";

import axios from "axios";
import ReactionHistory from "./ReactionHistory";
import Reviews from "./Reviews";
import Users from "./Users";

const Profile = (props) => {
  const { authState, authDispatch } = useContext(AuthContext);
  const history = useNavigate();

  const [reactionHistory, setReactionHistory] = useState(null);
  const [reviews, setReviews] = useState(null);
  const [users, setUsers] = useState(null);

  useEffect(() => {
    if (!authState.isUser) {
      history.push("/");
    } else {
      const token = localStorage.getItem("token");
      const config = {
        headers: { Authorization: "Bearer " + token },
      };
      axios
        .get(`api/auth/me`, config)
        .then((res) => {
          setReactionHistory(res.data.history);
          setReviews(res.data.reviews);
          setUsers(res.data.users);
        })
        .catch((err) => console.log(err.response.data));
    }
  }, [authState, history]);

  const handleLogout = () => {
    authDispatch({
      type: "LOGOUT",
    });
  };

  return (
    <div className="profile">
      <div className="content">
        <div className="container">
          <div className="d-flex">
            <div className="">
              <h1>Hello {authState.name}!</h1>
            </div>
            <div className="ml-auto">
              <button
                onClick={handleLogout}
                className="btn btn-danger nav-link"
              >
                Logout
              </button>
            </div>
          </div>
          <Tabs defaultActiveKey="history">
            <Tab eventKey="history" title="History">
              {reactionHistory && (
                <ReactionHistory reactionHistory={reactionHistory} />
              )}
            </Tab>
            {reviews && (
              <Tab eventKey="review" title="Reviews">
                <Reviews reviews={reviews} setReviews={setReviews} />
              </Tab>
            )}
            {users && (
              <Tab eventKey="users" title="Users">
                <Users users={users} setUsers={setUsers} />
              </Tab>
            )}
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default Profile;
