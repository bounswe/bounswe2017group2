import React from "react";
import { Link } from "react-router-dom";

function DashboardPage() {
  return (
    <div>
      <p>Youre in the DashboardPage!</p>

      <Link to="concert/1">Adamlar Concert</Link>
    </div>
  );
}

export default DashboardPage;
