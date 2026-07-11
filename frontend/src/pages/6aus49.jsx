import { useState } from "react";
import axios from "axios";
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  flexRender,
} from "@tanstack/react-table";

export default function Lotto6aus49() {
  const [open, setOpen] = useState(false);
  const [mode, setMode] = useState("1");
  const [numbers, setNumbers] = useState([]);
  const [supernum, setSupernum] = useState([]);
  const [history, setHistory] = useState([]);
  const [sorting, setSorting] = useState([]);
  const [threshold, setThreshold] = useState("4");

  // Mode config
  const config = {
    "1": { label: "Normal", count: 6, buttons: 20 },
    "2": { label: "Teilsystem", count: 0, buttons: 6 },
    "3": { label: "Vollsystem", count: 0, buttons: 5 },
  };
  const current = config[mode];
  const [thresholdOpen, setThresholdOpen] = useState(false);
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
        `http://localhost:8000/random_6aus49?button=${btn}&mode=${mode}&threshold=${threshold}`
      );

      setNumbers(res.data.setlist);
      setSupernum(res.data.supernum);
      setHistory(res.data.history ?? []);
    } catch (err) {
      console.error("Error generating numbers:", err);
      setNumbers([]);
      setSupernum([]);
      setHistory([]);
    }
  };

  // table
  const columns = [
    {
      accessorKey: "date_",
      header: ({ column }) => (
        <button
          className="font-bold text-white"
          onClick={column.getToggleSortingHandler()}
        >
          Date{" "}
          {column.getIsSorted() === "asc" && "↑"}
          {column.getIsSorted() === "desc" && "↓"}
        </button>
      ),
      cell: ({ row }) => (
        <span className="text-black font-bold">
          {row.original.date}
        </span>
      ),
    },
    {
      accessorKey: "historical_numbers",
      header: "Nummern",
      cell: ({ row }) => (
        <div className="flex gap-1">
          {row.original.historical_numbers.map((n, i) => (
            <span
              key={i}
              className={`w-12 h-12 rounded-full flex items-center justify-center text font-bold border ${row.original.common.includes(n)
                ? "bg-yellow-500 text-black"
                : "bg-white text-black hover:bg-gray-200"
                }`}
            >
              {n}
            </span>
          ))}
        </div>
      ),
    },
    {
      accessorKey: "historical_supernum",
      header: "Superzahl",
      cell: ({ row }) => (
        <div className="flex justify-center">
          {row.original.historical_supernum.map((n, i) => (
            <span
              className={`w-12 h-12 rounded-full flex items-center justify-center text font-bold shadow-lg border-2 ${row.original.supernum.includes(row.original.historical_supernum[0])
                ? "bg-red-400 text-black border-red-500"
                : "bg-white text-black border-red-500 hover:bg-gray-200"
                }`}
            >
              {n}
            </span>
          ))}
        </div>
      ),
    },
    {
      accessorKey: "num_sum",
      header: ({ column }) => (
        <button
          className="font-bold text-white"
          onClick={column.getToggleSortingHandler()}
        >
          Match{" "}
          {column.getIsSorted() === "asc" && "↑"}
          {column.getIsSorted() === "desc" && "↓"}
        </button>
      ),
      cell: ({ row }) => (
        <span className="font-bold text-black">
          {row.original.num_sum}
        </span>
      ),
    },
    {
      accessorKey: "super_sum",
      header: ({ column }) => (
        <button
          className="font-bold text-white"
          onClick={column.getToggleSortingHandler()}
        >
          SZ Match{" "}
          {column.getIsSorted() === "asc" && "↑"}
          {column.getIsSorted() === "desc" && "↓"}
        </button>
      ),
      cell: ({ row }) => (
        <span className="font-bold text-black">
          {row.original.super_sum}
        </span>
      ),
    },
  ];

  const table = useReactTable({
    data: history,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    enableSortingRemoval: true,
    state: {
      sorting,
    },
    onSortingChange: setSorting,
  });

  return (
    <div className="min-h-screen bg-gray-300 p-8 flex gap-2">
      <div className="w-full mx-auto flex gap-6 items-start">
        {/* Card */}
        <div className="bg-gray-200 shadow-xl rounded-lg p-6 flex-1 flex flex-col items-center gap-8">

          {/* Title */}
          <h1 className="text-black text-3xl font-bold">6 aus 49</h1>

          <div className="flex gap-4 justify-center">
            {/* Dropdown */}
            <div className="relative w-48 mx-auto">
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
            {/* Dropdown Threshold */}
            <div className="relative w-48">
              <button
                onClick={() => setThresholdOpen(!thresholdOpen)}
                className="w-full bg-gray-900 px-4 py-2 rounded hover:bg-red-500 transition text-white"
              >
                Threshold: {threshold}
              </button>

              {thresholdOpen && (
                <div className="absolute mt-2 bg-white text-black shadow-lg rounded-md w-full z-50">
                  {[1, 2, 3, 4, 5, 6].map((value) => (
                    <button
                      key={value}
                      onClick={() => {
                        setThreshold(String(value));
                        setThresholdOpen(false);
                      }}
                      className="block w-full text-left px-4 py-2 hover:bg-gray-100"
                    >
                      {value}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
          <div className="flex gap-4 items-start w-full justify-center">
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

        {/* HISTORY TABLE */}
        <div className="bg-gray-200 shadow-xl rounded-lg p-6 flex-1 items-center gap-8 max-h-[1000px] overflow-y-auto">
          <table className="w-full">
            <thead className="sticky top-0 bg-gray-900 text-white">
              {table.getHeaderGroups().map(headerGroup => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map(header => (
                    <th
                      key={header.id}
                      className="p-2 text-center"
                    >
                      {flexRender(
                        header.column.columnDef.header,
                        header.getContext()
                      )}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>

            <tbody>
              {table.getRowModel().rows.map(row => (
                <tr
                  key={row.id}
                  className="border-b hover:bg-gray-100"
                >
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id} className="p-2">
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>

          </table>
        </div>
      </div>

    </div>
  );
}
