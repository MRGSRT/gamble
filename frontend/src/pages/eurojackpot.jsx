import { useState } from "react";
import axios from "axios";
import { tableFromIPC } from "apache-arrow";

export default function Eurojackpot() {
  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState("1");
  const [numbers, setNumbers] = useState([]);
  const [supernum, setSupernum] = useState([]);

  const config = {
    "1": { label: "Normal" },
    "2": { label: "System" },
  };
  const current = config[mode];

  const buttons = mode === "1"
    ? Array.from({ length: 20 }, (_, i) => i + 1)
    : [
      "5 / 3", "5 / 4", "5 / 5", "5 / 6", "5 / 7",
      "5 / 8", "5 / 9", "5 / 10", "5 / 11", "5 / 12",
      "6 / 2", "6 / 3", "6 / 4", "6 / 5", "6 / 6",
      "6 / 7", "6 / 8", "6 / 9", "6 / 10", "6 / 11",
      "6 / 12", "7 / 2", "7 / 3", "7 / 4", "7 / 5",
      "7 / 6", "7 / 7", "8 / 2", "8 / 3", "8 / 4",
      "9 / 2", "9 / 3", "10 / 2", "11 / 2"
    ];
  const generate = async (btn) => {
    try {
      const params = { mode };

      if (mode === "2") {
        const [a, b] = btn.split(" / ").map(Number);
        params.count1 = a;
        params.count2 = b;
      } else {
        params.qtipps = Number(btn);
      }

      const res = await axios.get(
        "http://localhost:8000/randomEurojackpot",
        { params, responseType: "arraybuffer" }
      );

      const table = tableFromIPC(new Uint8Array(res.data));

      const columnNames = table.schema.fields.map(f => f.name);

      const numberColumns = columnNames.filter(n => n.startsWith("num"));
      const superColumns = columnNames.filter(n => n.startsWith("supernum"));

      const nums = [];
      const superNums = [];

      for (let row = 0; row < table.numRows; row++) {

        // 🔥 FIX: unwrap [[14]] → 14
        const numRow = numberColumns.map(col => {
          const v = table.getChild(col).get(row);
          return Array.isArray(v) ? v[0] : v;
        });

        nums.push(numRow);

        // same fix for supernums
        const superRow = superColumns.map(col => {
          const v = table.getChild(col).get(row);
          return Array.isArray(v) ? v[0] : v;
        });

        superNums.push(superRow);
      }

      console.log("NUMS:", nums);
      console.log("SUPERNUMS:", superNums);

      setNumbers(nums);
      setSupernum(superNums);

    } catch (err) {
      console.error(err);
      setNumbers([]);
      setSupernum([]);
    }
  };


  return (
    <div className="min-h-screen bg-gray-300 p-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-gray-200 shadow-xl rounded-lg p-6 flex flex-col items-center gap-6">
          <h1 className="text-black text-3xl font-bold">Eurojackpot</h1>

          <div className="relative w-48">
            <button
              onClick={() => setOpen(!open)}
              className="w-full bg-gray-900 px-4 py-2 rounded hover:bg-red-500 transition text-white"
            >
              {current.label}
            </button>
            {open && (
              <div className="absolute mt-2 bg-white text-black shadow-lg rounded-md w-full z-50">
                <button onClick={() => { setMode("1"); setOpen(false); }} className="block w-full text-left px-4 py-2 hover:bg-gray-100">Normal</button>
                <button onClick={() => { setMode("2"); setOpen(false); }} className="block w-full text-left px-4 py-2 hover:bg-gray-100">System</button>
              </div>
            )}
          </div>

          <div className="flex flex-wrap gap-2 justify-center mb-4">
            {buttons.map((n) => (
              <button key={n} onClick={() => generate(n)} className="bg-gray-900 px-3 py-2 rounded hover:bg-red-500 transition font-bold w-28 text-center text-white">
                {n}
              </button>
            ))}
          </div>

          {numbers.length > 0 && (
            <div className="flex flex-col gap-4 items-center w-full">
              {numbers.map((group, idx) => (
                <div key={idx} className="flex gap-3 justify-center items-center flex-wrap">
                  {group.map((n, i) => (
                    <div key={`num-${idx}-${i}`} className="w-14 h-14 rounded-full bg-white text-black flex items-center justify-center text-xl font-bold shadow-lg border-2 border-gray-400">
                      {n}
                    </div>
                  ))}
                  {supernum[idx]?.map((n, i) => (
                    <div key={`super-${idx}-${i}`} className="w-14 h-14 rounded-full bg-white text-black flex items-center justify-center text-xl font-bold shadow-lg border-2 border-red-500">
                      {n}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}