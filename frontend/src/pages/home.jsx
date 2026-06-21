import { useState, useEffect, useMemo, useCallback } from "react";
import "../App.css";

export default function Home() {
  const [lotto49Data, setLotto49Data] = useState([]);
  const [eurojackpotData, setEurojackpotData] = useState([]);
  const [kenoData, setKenoData] = useState([]);
  const [super6Data, setSuper6Data] = useState([]);
  const [spiel77Data, setSpiel77Data] = useState([]);
  const [glücksradData, setGlücksradData] = useState([]);
  const [sortOrder, setSortOrder] = useState("asc");
  const [displayMode, setDisplayMode] = useState("separate"); // "separate" or "sorted"
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("lotto49"); // "lotto49", "eurojackpot", "keno", "super6", "spiel77", "glücksrad"
  const [displayLimit, setDisplayLimit] = useState(50); // Limit renders to first 50 entries

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // Fetch each game independently so one failure doesn't block others
        const fetchGame = async (url, setState) => {
          try {
            const res = await fetch(url);
            if (res.ok) {
              const data = await res.json();
              setState(Array.isArray(data) ? data.slice(0, 5000) : []);
            }
          } catch (err) {
            console.error(`Error fetching from ${url}:`, err);
            setState([]);
          }
        };

        await Promise.all([
          fetchGame("http://localhost:8000/data_lotto6aus49", setLotto49Data),
          fetchGame("http://localhost:8000/data_eurojackpot", setEurojackpotData),
          fetchGame("http://localhost:8000/data_keno", setKenoData),
          fetchGame("http://localhost:8000/data_super6", setSuper6Data),
          fetchGame("http://localhost:8000/data_spiel77", setSpiel77Data),
          fetchGame("http://localhost:8000/data_glücksrad", setGlücksradData),
        ]);
      } catch (err) {
        console.error("Error in fetch process:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Sort numbers for display - memoized
  const getSortedNumbers = useCallback((zahlen) => {
    if (!Array.isArray(zahlen)) return [];
    const sorted = [...zahlen];
    if (sortOrder === "asc") {
      sorted.sort((a, b) => a - b);
    } else {
      sorted.sort((a, b) => b - a);
    }
    return sorted;
  }, [sortOrder]);

  const renderNumberCircle = (num, color = "blue") => {
    const colorClasses = {
      white: "from-white-400 to-white-600 border-gray-400",
      blue: "from-blue-400 to-blue-600 border-blue-800",
      purple: "from-white-400 to-white-600 border-purple-800",
      red: "from-white-400 to-white-600 border-red-500",
      green: "from-white-400 to-white-600 border-green-800",
      yellow: "from-white-400 to-white-600 border-yellow-500",
      super6: "from-white-400 to-white-600 border-purple-500",
      spiel77: "from-white-400 to-white-600 border-blue-300"
    };

    return (
      <div
        key={num}
        className={`w-16 h-16 rounded-full bg-gradient-to-br ${colorClasses[color]} text-black flex items-center justify-center text-xl font-bold shadow-lg border-2 hover:scale-110 transition`}
      >
        {num}
      </div>
    );
  };

  const renderLotto49Entry = (entry, idx) => {
    const zahlen = [entry.Zahl1, entry.Zahl2, entry.Zahl3, entry.Zahl4, entry.Zahl5, entry.Zahl6];
    const displayNumbers =
      displayMode === "separate" ? zahlen : getSortedNumbers(zahlen);

    return (
      <div key={idx} className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-black text-lg font-bold mb-4">
          {entry.Tag}.{String(entry.Monat).padStart(2, "0")}.{entry.Jahr}
        </h2>

        <div className="space-y-4">
          <div className={`grid gap-3 mb-4 ${displayMode === "separate" ? "grid-cols-3 md:grid-cols-6" : "grid-cols-3 md:grid-cols-6"}`}>
            {displayNumbers.map((num) =>
              displayMode === "separate"
                ? renderNumberCircle(num, "white")
                : renderNumberCircle(num, "white")
            )}
          </div>

          <div className="flex items-center gap-4 pt-4 border-t-2 border-gray-300">
            <span className="text-black font-bold text-lg">Superzahl:</span>
            {renderNumberCircle(entry.Super, "red")}
          </div>
        </div>
      </div>
    );
  };

  const renderEurojackpotEntry = (entry, idx) => {
    const zahlA = [entry.ZahlA1, entry.ZahlA2, entry.ZahlA3, entry.ZahlA4, entry.ZahlA5];
    const zahlB = [entry.ZahlB1, entry.ZahlB2];

    const displayZahlA = displayMode === "separate" ? zahlA : getSortedNumbers(zahlA);
    const displayZahlB = displayMode === "separate" ? zahlB : getSortedNumbers(zahlB);

    return (
      <div key={idx} className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-black text-lg font-bold mb-4">
          {entry.Tag}.{String(entry.Monat).padStart(2, "0")}.{entry.Jahr}
        </h2>

        <div className="space-y-4">
          {/* Main numbers (1-50) */}
          <div>
            <h3 className="text-black font-bold text-sm mb-2">Zahlen (1-50):</h3>
            <div className="grid grid-cols-3 md:grid-cols-5 gap-3 mb-4">
              {displayZahlA.map((num) =>
                displayMode === "separate"
                  ? renderNumberCircle(num, "white")
                  : renderNumberCircle(num, "white")
              )}
            </div>
          </div>

          {/* Euro numbers (1-12) */}
          <div className="pt-4 border-t-2 border-gray-300">
            <h3 className="text-black font-bold text-sm mb-2">Eurozahlen (1-12):</h3>
            <div className="flex gap-3">
              {displayZahlB.map((num) =>
                displayMode === "separate"
                  ? renderNumberCircle(num, "yellow")
                  : renderNumberCircle(num, "yellow")
              )}
            </div>
          </div>
        </div>
      </div>
    );
  };

  const renderKenoEntry = (entry, idx) => {
    const zahlen = Array.from({ length: 20 }, (_, i) => entry[`Zahl${i + 1}`]);
    const displayNumbers = displayMode === "separate" ? zahlen : getSortedNumbers(zahlen);

    return (
      <div key={idx} className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-black text-lg font-bold mb-4">
          {entry.Tag}.{String(entry.Monat).padStart(2, "0")}.{entry.Jahr}
        </h2>
        <div className="grid grid-cols-5 md:grid-cols-10 gap-3">
          {displayNumbers.map((num) => renderNumberCircle(num, "purple"))}
        </div>
      </div>
    );
  };

  const renderSimpleEntry = (entry, idx, fieldName) => {
    return (
      <div key={idx} className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-black text-lg font-bold mb-4">
          {entry.Tag}.{String(entry.Monat).padStart(2, "0")}.{entry.Jahr}
        </h2>
        <div className="flex gap-3 justify-center">
          <div className="bg-gray-100 border-2 border-gray-400 rounded-lg px-6 py-4">
            <span className="text-black text-3xl font-bold">{entry[fieldName]}</span>
          </div>
        </div>
      </div>
    );
  };

  const renderSuper6Entry = (entry, idx, fieldName) => {
    return (
      <div key={idx} className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-black text-lg font-bold mb-4">
          {entry.Tag}.{String(entry.Monat).padStart(2, "0")}.{entry.Jahr}
        </h2>
        <div className="flex gap-3 justify-center">
          <div className="bg-pink-200 border-2 border-pink-700 rounded-lg px-6 py-4">
            <span className="text-black text-3xl font-bold">{entry[fieldName]}</span>
          </div>
        </div>
      </div>
    );
  };

  const renderSpiel77Entry = (entry, idx, fieldName) => {
    return (
      <div key={idx} className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-black text-lg font-bold mb-4">
          {entry.Tag}.{String(entry.Monat).padStart(2, "0")}.{entry.Jahr}
        </h2>
        <div className="flex gap-3 justify-center">
          <div className="bg-blue-100 border-2 border-blue-400 rounded-lg px-6 py-4">
            <span className="text-black text-3xl font-bold">{entry[fieldName]}</span>
          </div>
        </div>
      </div>
    );
  };

  const renderGlücksradEntry = (entry, idx) => {
    const winningClasses = [
      { label: "GK1", value: entry.GK1 },
      { label: "GK2", value: entry.GK2 },
      { label: "GK3", value: entry.GK3 },
      { label: "GK4", value: entry.GK4 },
      { label: "GK5", value: entry.GK5 },
      { label: "GK6 (1)", value: entry.GK6_1 },
      { label: "GK6 (2)", value: entry.GK6_2 },
      { label: "GK7 (1)", value: entry.GK7_1 },
      { label: "GK7 (2)", value: entry.GK7_2 },
    ];

    // Rainbow colors for border + background
    const colorPairs = [
      { border: "border-red-500", bg: "bg-red-100" },
      { border: "border-orange-500", bg: "bg-orange-100" },
      { border: "border-yellow-500", bg: "bg-yellow-100" },
      { border: "border-green-500", bg: "bg-green-100" },
      { border: "border-blue-500", bg: "bg-blue-100" },
      { border: "border-indigo-500", bg: "bg-indigo-100" },
      { border: "border-purple-500", bg: "bg-purple-100" },
      { border: "border-pink-500", bg: "bg-pink-100" },
      { border: "border-cyan-500", bg: "bg-cyan-100" },
    ];

    return (
      <div key={idx} className="bg-white rounded-lg p-6 shadow-md">
        <h2 className="text-black text-lg font-bold mb-4">
          {entry.Tag}.{String(entry.Monat).padStart(2, "0")}.{entry.Jahr}
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
          {winningClasses.map((gk, i) => {
            const colors = colorPairs[i % colorPairs.length];
            return (
              <div
                key={i}
                className={`border-2 rounded-lg p-3 text-center ${colors.border} ${colors.bg}`}
              >
                <p className="text-black font-bold text-sm">{gk.label}</p>
                <p className="text-black text-lg font-bold">{gk.value || "-"}</p>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-300 p-8 flex items-center justify-center">
        <div className="text-black text-2xl font-bold">Loading lottery data...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-300 p-8">
      <div className="max-w-5xl mx-auto">
        {/* Card */}
        <div className="bg-gray-200 shadow-xl rounded-lg p-6">
          {/* Title */}
          <h1 className="text-black text-3xl font-bold mb-6 text-center">
            Gezogene Nummern
          </h1>

          {/* Tab Navigation */}
          <div className="flex gap-4 justify-center mb-6 flex-wrap">
            <button
              onClick={() => setActiveTab("lotto49")}
              className={`px-4 py-2 rounded font-bold transition ${activeTab === "lotto49"
                ? "bg-yellow-500 text-white"
                : "bg-gray-900 text-white hover:bg-red-500"
                }`}
            >
              Lotto 6aus49
            </button>
            <button
              onClick={() => setActiveTab("eurojackpot")}
              className={`px-4 py-2 rounded font-bold transition ${activeTab === "eurojackpot"
                ? "bg-yellow-500 text-white"
                : "bg-gray-900 text-white hover:bg-red-500"
                }`}
            >
              Eurojackpot
            </button>
            <button
              onClick={() => setActiveTab("keno")}
              className={`px-4 py-2 rounded font-bold transition ${activeTab === "keno"
                ? "bg-purple-800 text-white"
                : "bg-gray-900 text-white hover:bg-purple-800"
                }`}
            >
              Keno
            </button>
            <button
              onClick={() => setActiveTab("super6")}
              className={`px-4 py-2 rounded font-bold transition ${activeTab === "super6"
                ? "bg-pink-700 text-white"
                : "bg-gray-900 text-white hover:bg-pink-700"
                }`}
            >
              Super6
            </button>
            <button
              onClick={() => setActiveTab("spiel77")}
              className={`px-4 py-2 rounded font-bold transition ${activeTab === "spiel77"
                ? "bg-blue-400 text-white"
                : "bg-gray-900 text-white hover:bg-blue-400"
                }`}
            >
              Spiel77
            </button>
            <button
              onClick={() => setActiveTab("glücksrad")}
              className={`px-4 py-2 rounded font-bold transition ${activeTab === "glücksrad"
                  ? "rainbow-active"
                  : "rainbow-hover"
                }`}
            >
              Glücksrad
            </button>
          </div>

          {/* Controls */}
          <div className="flex flex-wrap gap-4 justify-center mb-8">
            {/* Sort Order Toggle */}
            <div className="flex gap-2">
              <button
                onClick={() => setSortOrder("asc")}
                className={`px-4 py-2 rounded font-bold transition ${sortOrder === "asc"
                  ? "bg-green-500 text-white"
                  : "bg-gray-900 text-white hover:bg-red-500"
                  }`}
              >
                ↑ Ascending
              </button>
              <button
                onClick={() => setSortOrder("desc")}
                className={`px-4 py-2 rounded font-bold transition ${sortOrder === "desc"
                  ? "bg-green-500 text-white"
                  : "bg-gray-900 text-white hover:bg-red-500"
                  }`}
              >
                ↓ Descending
              </button>
            </div>

            {/* Display Mode Toggle */}
            <div className="flex gap-2">
              <button
                onClick={() => setDisplayMode("separate")}
                className={`px-4 py-2 rounded font-bold transition ${displayMode === "separate"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-900 text-white hover:bg-red-500"
                  }`}
              >
                Original Order
              </button>
              <button
                onClick={() => setDisplayMode("sorted")}
                className={`px-4 py-2 rounded font-bold transition ${displayMode === "sorted"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-900 text-white hover:bg-red-500"
                  }`}
              >
                Sorted Order
              </button>
            </div>
          </div>

          {/* Data Display */}
          <div className="space-y-6">
            {activeTab === "lotto49" && lotto49Data.length > 0 ? (
              lotto49Data.slice(0, displayLimit).map((entry, idx) => renderLotto49Entry(entry, idx))
            ) : activeTab === "lotto49" ? (
              <div className="text-black text-center text-lg">No Lotto 6 aus 49 data available</div>
            ) : null}

            {activeTab === "eurojackpot" && eurojackpotData.length > 0 ? (
              eurojackpotData.slice(0, displayLimit).map((entry, idx) => renderEurojackpotEntry(entry, idx))
            ) : activeTab === "eurojackpot" ? (
              <div className="text-black text-center text-lg">No Eurojackpot data available</div>
            ) : null}

            {activeTab === "keno" && kenoData.length > 0 ? (
              kenoData.slice(0, displayLimit).map((entry, idx) => renderKenoEntry(entry, idx))
            ) : activeTab === "keno" ? (
              <div className="text-black text-center text-lg">No Keno data available</div>
            ) : null}

            {activeTab === "super6" && super6Data.length > 0 ? (
              super6Data.slice(0, displayLimit).map((entry, idx) => renderSuper6Entry(entry, idx, "Gewinnzahl"))
            ) : activeTab === "super6" ? (
              <div className="text-black text-center text-lg">No Super6 data available</div>
            ) : null}

            {activeTab === "spiel77" && spiel77Data.length > 0 ? (
              spiel77Data.slice(0, displayLimit).map((entry, idx) => renderSpiel77Entry(entry, idx, "Gewinnzahl"))
            ) : activeTab === "spiel77" ? (
              <div className="text-black text-center text-lg">No Spiel77 data available</div>
            ) : null}

            {activeTab === "glücksrad" && glücksradData.length > 0 ? (
              glücksradData.slice(0, displayLimit).map((entry, idx) => renderGlücksradEntry(entry, idx))
            ) : activeTab === "glücksrad" ? (
              <div className="text-black text-center text-lg">No Glücksrad data available</div>
            ) : null}
          </div>

          {/* Load More Button */}
          {(displayLimit < lotto49Data.length || displayLimit < eurojackpotData.length || displayLimit < kenoData.length ||
            displayLimit < super6Data.length || displayLimit < spiel77Data.length || displayLimit < glücksradData.length) && (
              <div className="mt-6 text-center">
                <button
                  onClick={() => setDisplayLimit(prev => prev + 100)}
                  className="px-6 py-2 bg-yellow-500 text-white font-bold rounded hover:bg-yellow-600 transition"
                >
                  Load More
                </button>
              </div>
            )}

          {/* Legend */}
          <div className="mt-8 p-4 bg-gray-100 rounded-lg text-black text-sm">
            <p className="font-bold mb-2">Legend:</p>
            <ul className="space-y-1">
              <li>
                <span className="inline-block w-4 h-4 rounded-full bg-red-500 mr-2"></span>
                Superzahl (Lotto 6aus49)
              </li>
              <li>
                <span className="inline-block w-4 h-4 rounded-full bg-yellow-500 mr-2"></span>
                Eurozahlen (Eurojackpot)
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
