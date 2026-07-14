import { Routes, Route, Link } from "react-router-dom";

import Home from "./pages/home";
import Grid from "./pages/grid"
import Lotto6aus49 from "./pages/6aus49";
import Eurojackpot from "./pages/eurojackpot";
import Analytics from "./pages/analytics";
import DrawHistory from "./pages/draw-history";

function App() {
  return (
    <div>

      {/* NAVBAR */}
      <div className="navbar bg-yellow-500 shadow-sm">

        <div className="flex-1">
          <Link to="/" className="btn btn-ghost text-xl hover:bg-red-500 text-white">
            Gamble
          </Link>
        </div>

        <div className="flex-none gap-2">

          <Link to="/Numbers-Drawn" className="btn btn-ghost hover:bg-red-500 text-white">
            Gewinnzahlen
          </Link>

          <Link to="/Analytics" className="btn btn-ghost hover:bg-red-500 text-white">
            Analytics
          </Link>

          <Link to="/Lotto6aus49" className="btn btn-ghost hover:bg-red-500 text-white">
            6 aus 49
          </Link>

          <Link to="/Eurojackpot" className="btn btn-ghost hover:bg-red-500 text-white">
            Eurojackpot
          </Link>

          <Link to="/grid" className="btn btn-ghost hover:bg-red-500 text-white">
            Grid
          </Link>

        </div>
      </div>

      {/* ROUTES */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/Analytics" element={<Analytics />} />
        <Route path="/Lotto6aus49" element={<Lotto6aus49 />} />
        <Route path="/Eurojackpot" element={<Eurojackpot />} />
        <Route path="/grid" element={<Grid />} />
        <Route path="/Numbers-Drawn" element={<DrawHistory />} />
      </Routes>

    </div>
  );
}

export default App;