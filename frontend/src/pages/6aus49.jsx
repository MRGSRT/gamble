import { useState } from "react";
import axios from "axios";
import { tableFromIPC } from 'apache-arrow';

export default function Lotto6aus49() {
  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState("1");
  const [numbers, setNumbers] = useState([]);
  const [supernum, setSupernum] = useState([]);

  // Mode config
  const config = {
    "1": { label: "Normal", count: 6, buttons: 20 },
    "2": { label: "Teilsystem", count: 0, buttons: 6 },
    "3": { label: "Vollsystem", count: 0, buttons: 5 },
  };
  const current = config[mode];

  // Buttons array
  let buttons = [];
  if (mode === "1") {
    buttons = Array.from({ length: 20 }, (_, i) => i + 1);
  }
  if (mode === "2") {
    buttons = [22, 30, 66, 77, 130, 132];
  }
  if (mode === "3") {
    buttons = ["6 aus 7", "6 aus 8", "6 aus 9", "6 aus 10", "6 aus 11"];
  }
  // Generate numbers
  const generate = async (btn) => {
    try {
      if (mode === "3") {
        const map = {
          "6 aus 7": 7,
          "6 aus 8": 8,
          "6 aus 9": 9,
          "6 aus 10": 10,
          "6 aus 11": 11,
        };
        btn = map[btn];
      }

      const res = await axios.get(
        `http://localhost:8000/random_6aus49?button=${btn}&mode=${mode}`,
        { responseType: "arraybuffer" }
      );

      const table = tableFromIPC(res.data);
      const rowCount = table.numRows;

      const nums = [];
      const superNums = [];

      for (let i = 0; i < rowCount; i++) {
        nums.push([
          table.getChild("num1").get(i),
          table.getChild("num2").get(i),
          table.getChild("num3").get(i),
          table.getChild("num4").get(i),
          table.getChild("num5").get(i),
          table.getChild("num6").get(i),
        ]);

        // If the backend returns multiple super numbers, wrap in array
        const rowSuper = table.getChild("supernum").get(i);
        superNums.push(Array.isArray(rowSuper) ? rowSuper : [rowSuper]);
      }

      setNumbers(nums);
      setSupernum(superNums);

    } catch (err) {
      console.error("Error generating numbers:", err);
      setNumbers([]);
      setSupernum([]);
    }
  };

  return (
    <div className="min-h-screen bg-gray-300 p-8">
      <div className="max-w-3xl mx-auto">
        {/* Card */}
        <div className="bg-gray-200 shadow-xl rounded-lg p-6 flex flex-col items-center gap-6">

          {/* Title */}
          <h1 className="text-black text-3xl font-bold">6 aus 49</h1>

          {/* Dropdown */}
          <div className="relative w-48">
            <button
              onClick={() => setOpen(!open)}
              className="w-full bg-gray-900 px-4 py-2 rounded hover:bg-red-500 transition text-white"
            >
              {current.label}
            </button>

            {open && (
              <div className="absolute mt-2 bg-white text-black shadow-lg rounded-md w-full z-50">
                <button
                  onClick={() => { setMode("1"); setOpen(false); }}
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100"
                >
                  Normal
                </button>
                <button
                  onClick={() => { setMode("2"); setOpen(false); }}
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100"
                >
                  Teilsystem
                </button>
                <button
                  onClick={() => { setMode("3"); setOpen(false); }}
                  className="block w-full text-left px-4 py-2 hover:bg-gray-100"
                >
                  Vollsystem
                </button>
              </div>
            )}
          </div>

          {/* Number buttons */}
          <div className="flex flex-wrap gap-2 justify-center mb-4">
            {buttons.map((n) => (
              <button
                key={n}
                onClick={() => generate(n)}
                className="bg-gray-900 px-3 py-2 rounded hover:bg-red-500 transition font-bold w-28 text-center text-white"
              >
                {n}
              </button>
            ))}
          </div>

          {/* Generated numbers below the buttons */}
          {numbers.length > 0 && (
            <div className="flex flex-col gap-4 items-center w-full">
              {numbers.map((group, idx) => (
                <div key={idx} className="flex gap-3 justify-center items-center flex-wrap">
                  {/* Regular numbers */}
                  {Array.isArray(group) && group.map((n) => (
                    <div
                      key={n}
                      className="w-14 h-14 rounded-full bg-white text-black flex items-center justify-center text-xl font-bold shadow-lg border-2 border-gray-400"
                    >
                      {n}
                    </div>
                  ))}

                  {/* Super numbers */}
                  {supernum[idx] !== undefined && (
                    <div className="w-14 h-14 rounded-full bg-white text-black flex items-center justify-center text-xl font-bold shadow-lg border-2 border-red-500">
                      {supernum[idx]}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
