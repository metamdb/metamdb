import React, { useContext } from "react";
import { Link } from "react-router-dom";

import { MetaboliteContext } from "../../contexts/MetaboliteContext";

const Reactions = () => {
  const { metabolite } = useContext(MetaboliteContext);

  return (
    <div className="mt-3">
      <Link
        target="_blank"
        to={`/database-query?metabolite_id=${metabolite.id}`}
      >
        See the reactions here!
      </Link>
    </div>
  );
};

export default Reactions;
