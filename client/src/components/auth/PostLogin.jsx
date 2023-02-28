import { useEffect, useContext } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { AuthContext } from "../../contexts/AuthContext";

import qs from "qs";
import jwt_decode from "jwt-decode";

const PostLogin = (props) => {
  const { authDispatch } = useContext(AuthContext);
  const location = useLocation();
  const history = useNavigate();

  useEffect(() => {
    if (location.search) {
      const query = qs.parse(location.search, { ignoreQueryPrefix: true });
      const { jwt } = query;

      if (jwt) {
        const decoded_jwt = jwt_decode(jwt);

        authDispatch({
          type: "LOGIN",
          payload: { ...decoded_jwt.sub, token: jwt },
        });
      }
    }
    history.push("/me");
  }, [location, authDispatch, history]);

  return null;
};

export default PostLogin;
