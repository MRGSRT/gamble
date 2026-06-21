import { useState } from "react";

export default function LotteryGrid() {
    const [game, setGame] = useState("6aus49"); // selected game
    const [menuOpen, setMenuOpen] = useState(false); // dropdown toggle
    const [selected, setSelected] = useState([]);

    const toggleNumber = (num) => {
        setSelected((prev) => {
            const updated = prev.includes(num)
                ? prev.filter((n) => n !== num)
                : [...prev, num];

            return updated.sort((a, b) => a - b);
        });
    };

    // Configure grid based on game
    const maxNumber = game === "6aus49" ? 49 : 50;
    const numbers = Array.from({ length: maxNumber }, (_, i) => i + 1);

    const handleGameSelect = (selectedGame) => {
        setGame(selectedGame);
        setSelected([]); // reset selection on game change
        setMenuOpen(false); // close dropdown
    };

    return (
        <div className="min-h-screen bg-gray-300 p-8 flex flex-col items-center">

            <h1 className="text-black text-3xl mb-6">Select Numbers</h1>

            {/* DROPDOWN */}
            <div className="relative w-48 mb-6">
                <button
                    onClick={() => setMenuOpen(!menuOpen)}
                    className="w-full bg-gray-900 px-4 py-2 rounded hover:bg-red-500 transition text-white"
                >
                    {game === "6aus49" ? "6 aus 49" : "EuroJackpot"}
                </button>

                {menuOpen && (
                    <div className="absolute mt-2 bg-white text-black shadow-lg rounded-md w-full z-50">
                        <button
                            onClick={() => handleGameSelect("6aus49")}
                            className="block w-full text-left px-4 py-2 hover:bg-gray-100"
                        >
                            6 aus 49
                        </button>
                        <button
                            onClick={() => handleGameSelect("eurojackpot")}
                            className="block w-full text-left px-4 py-2 hover:bg-gray-100"
                        >
                            EuroJackpot
                        </button>
                    </div>
                )}
            </div>

            {/* GRID */}
            <div className={`grid gap-2 ${game === "6aus49" ? "grid-cols-7" : "grid-cols-10"}`}>
                {numbers.map((num) => (
                    <button
                        key={num}
                        onClick={() => toggleNumber(num)}
                        className={`
                                    w-12 h-12 rounded-full font-bold shadow-md
                                    flex items-center justify-center
                                    transition
                                    ${selected.includes(num)
                                ? "bg-yellow-500 text-black"
                                : "bg-white text-black hover:bg-gray-200"
                            }
                        `}
                    >
                        {num}
                    </button>
                ))}
            </div>
            {/* SELECTED NUMBERS */}
            <div className="mt-6 flex flex-wrap gap-2 justify-center">
                {selected.map((n) => (
                    <div
                        key={n}
                        className="w-14 h-14 rounded-full bg-white text-black flex items-center justify-center text-xl font-bold shadow-lg border-2 border-gray-400"
                    >
                        {n}
                    </div>
                ))}
            </div>

        </div>
    );
}