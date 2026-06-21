import { useEffect, useState } from "react";

export default function Analytics() {
    const API = "/api";

    const endpoints = {
        lotto6aus49: `${API}/heatmap_lotto6aus49`,
        eurojackpot: `${API}/heatmap_eurojackpot`,
        lotto6aus49_superzahl: `${API}/heatmap_lotto6aus49_superzahl`,
        eurojackpot_eurozahl: `${API}/heatmap_eurojackpot_eurozahl`,
        lotto6aus49_not_drawn: `${API}/heatmap_lotto6aus49_not_drawn`,
        eurojackpot_not_drawn: `${API}/heatmap_eurojackpot_not_drawn`,
    };

    const initialState = Object.keys(endpoints).reduce((acc, key) => {
        acc[key] = [];
        return acc;
    }, {});
    const [state, setState] = useState(initialState);

    useEffect(() => {
        const load = async (url, key) => {
            try {
                const res = await fetch(url);
                const data = await res.json();

                setState(prev => ({
                    ...prev,
                    [key]: data,
                }));
            } catch (err) {
                console.error(`Failed loading ${key}:`, err);
            }
        };

        Object.entries(endpoints).forEach(([key, url]) => {
            load(url, key);
        });
    }, []);

    const getPastelColor = (pct, min, max) => {
        // Normalisieren auf 0–1
        const n = (pct - min) / (max - min);

        // HSL-Farbskala: grün → gelb → rot
        let hue;
        if (n <= 0.5) {
            // grün → gelb
            hue = 120 - (n / 0.5) * 60;
        } else {
            // gelb → rot
            hue = 60 - ((n - 0.5) / 0.5) * 60;
        }

        const saturation = 70;
        const lightness = 65 + (1 - n) * 10;

        return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
    };
    const minPct3 = Math.min(...state.eurojackpot.map(d => d.percent));
    const maxPct3 = Math.max(...state.eurojackpot.map(d => d.percent));
    const minPct2 = Math.min(...state.lotto6aus49.map(d => d.percent));
    const maxPct2 = Math.max(...state.lotto6aus49.map(d => d.percent));

    const minPct5 = Math.min(...state.eurojackpot_eurozahl.map(d => d.percent));
    const maxPct5 = Math.max(...state.eurojackpot_eurozahl.map(d => d.percent));
    const minPct4 = Math.min(...state.lotto6aus49_superzahl.map(d => d.percent));
    const maxPct4 = Math.max(...state.lotto6aus49_superzahl.map(d => d.percent));

    const minPct6 = state.lotto6aus49_not_drawn.length > 0 ? Math.min(...state.lotto6aus49_not_drawn.map(d => d.days_since).filter(d => d >= 0)) : 0;
    const maxPct6 = state.lotto6aus49_not_drawn.length > 0 ? Math.max(...state.lotto6aus49_not_drawn.map(d => d.days_since).filter(d => d >= 0)) : 100;
    const minPct7 = state.eurojackpot_not_drawn.length > 0 ? Math.min(...state.eurojackpot_not_drawn.map(d => d.days_since).filter(d => d >= 0)) : 0;
    const maxPct7 = state.eurojackpot_not_drawn.length > 0 ? Math.max(...state.eurojackpot_not_drawn.map(d => d.days_since).filter(d => d >= 0)) : 100;

    return (
        <div className="min-h-screen bg-gray-300 p-8 flex flex-col items-center">
            <div className="bg-gray-200 shadow-xl rounded-lg p-6 ">
                <div className="flex gap-10 items-start justify-center flex-wrap">
                    <h2 className="text-2xl font-bold mb-4 text-black">Häufigkeit</h2>
                </div>


                <div className="bg-gray-100 shadow-xl rounded-lg p-6">
                    <div className="flex gap-10 items-start justify-center flex-wrap">

                        {/* LOTTO 6aus49 */}
                        <div className="flex flex-col gap-4 items-center">
                            <h3 className="text-xl font-bold text-black">Lotto 6aus49</h3>

                            {/* Main Numbers */}
                            <div className="grid grid-cols-7 gap-2">
                                {Array.from({ length: state.lotto6aus49.length }, (_, i) => {
                                    const number = i + 1;

                                    const item = state.lotto6aus49.find(
                                        d => d.number === number
                                    );

                                    const value = item?.value || 0;
                                    const percent = item?.percent ?? 0;

                                    const bg = item
                                        ? getPastelColor(percent, minPct2, maxPct2)
                                        : "#eee";

                                    return (
                                        <div
                                            key={`lotto-main-${number}`}
                                            title={`Number: ${number} | Value: ${value} | ${percent.toFixed(2)}%`}
                                            className="w-14 h-14 flex flex-col items-center justify-center rounded-lg text-gray-800 font-bold shadow hover:scale-105 transition"
                                            style={{ backgroundColor: bg }}
                                        >
                                            <span>{number}</span>
                                            <span className="text-xs text-gray-600">{value}</span>
                                            <span className="text-xs text-blue-800">
                                                {percent.toFixed(1)}%
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>

                            {/* Superzahl */}
                            <div className="grid grid-cols-5 gap-2">
                                {Array.from({ length: state.lotto6aus49_superzahl.length }, (_, i) => {
                                    const number = i;

                                    const item = state.lotto6aus49_superzahl.find(
                                        d => d.number === number
                                    );

                                    const value = item?.value || 0;
                                    const percent = item?.percent ?? 0;

                                    const bg = item
                                        ? getPastelColor(percent, minPct4, maxPct4)
                                        : "#eee";

                                    return (
                                        <div
                                            key={`lotto-super-${number}`}
                                            title={`Superzahl: ${number} | Value: ${value} | ${percent.toFixed(2)}%`}
                                            className="w-14 h-14 flex flex-col items-center justify-center rounded-lg text-gray-800 font-bold shadow hover:scale-105 transition"
                                            style={{ backgroundColor: bg }}
                                        >
                                            <span>{number}</span>
                                            <span className="text-xs text-gray-600">{value}</span>
                                            <span className="text-xs text-blue-800">
                                                {percent.toFixed(1)}%
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        {/* EUROJACKPOT */}
                        <div className="flex flex-col gap-4 items-center">
                            <h3 className="text-xl font-bold text-black">Eurojackpot</h3>

                            {/* Main Numbers */}
                            <div className="grid grid-cols-10 gap-2">
                                {Array.from({ length: state.eurojackpot.length }, (_, i) => {
                                    const number = i + 1;

                                    const item = state.eurojackpot.find(
                                        d => d.number === number
                                    );

                                    const value = item?.value || 0;
                                    const percent = item?.percent ?? 0;

                                    const bg = item
                                        ? getPastelColor(percent, minPct3, maxPct3)
                                        : "#eee";

                                    return (
                                        <div
                                            key={`euro-main-${number}`}
                                            title={`Number: ${number} | Value: ${value} | ${percent.toFixed(2)}%`}
                                            className="w-14 h-14 flex flex-col items-center justify-center rounded-lg text-gray-800 font-bold shadow hover:scale-105 transition"
                                            style={{ backgroundColor: bg }}
                                        >
                                            <span>{number}</span>
                                            <span className="text-xs text-gray-600">{value}</span>
                                            <span className="text-xs text-blue-800">
                                                {percent.toFixed(1)}%
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>

                            {/* Eurozahlen */}
                            <div className="grid grid-cols-6 gap-2">
                                {Array.from({ length: state.eurojackpot_eurozahl.length }, (_, i) => {
                                    const number = i + 1;

                                    const item = state.eurojackpot_eurozahl.find(
                                        d => d.number === number
                                    );

                                    const value = item?.value || 0;
                                    const percent = item?.percent ?? 0;

                                    const bg = item
                                        ? getPastelColor(percent, minPct5, maxPct5)
                                        : "#eee";

                                    return (
                                        <div
                                            key={`euro-special-${number}`}
                                            title={`Eurozahl: ${number} | Value: ${value} | ${percent.toFixed(2)}%`}
                                            className="w-14 h-14 flex flex-col items-center justify-center rounded-lg text-gray-800 font-bold shadow hover:scale-105 transition"
                                            style={{ backgroundColor: bg }}
                                        >
                                            <span>{number}</span>
                                            <span className="text-xs text-gray-600">{value}</span>
                                            <span className="text-xs text-blue-800">
                                                {percent.toFixed(1)}%
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                    </div>
                </div>
                <div className="flex gap-10 items-start justify-center flex-wrap">
                    <h2 className="text-2xl font-bold mb-4 text-black mt-8">Letztes Mal Gezogen in Tagen</h2>
                </div>

                <div className="bg-gray-100 shadow-xl rounded-lg p-6">
                    <div className="flex gap-10 items-start justify-center flex-wrap">

                        {/* LOTTO 6aus49 */}
                        <div className="flex flex-col gap-4 items-center">
                            <h3 className="text-xl font-bold text-black">Lotto 6aus49</h3>

                            {/* Main Numbers */}
                            <div className="grid grid-cols-7 gap-1">
                                {Array.from({ length: 49 }, (_, i) => {
                                    const number = i + 1;

                                    const item = state.lotto6aus49_not_drawn.find(
                                        d => d.type === "main" && d.number === number
                                    );

                                    const last_drawn = item?.last_drawn || "Never";
                                    const days_since = item?.days_since ?? -1;

                                    const bg = days_since >= 0
                                        ? getPastelColor(days_since, minPct6, maxPct6)
                                        : "#ddd";

                                    return (
                                        <div
                                            key={`lotto-main-${number}`}
                                            title={`Number: ${number} | Last drawn: ${last_drawn} | Days since: ${days_since}`}
                                            className="w-14 h-14 flex flex-col items-center justify-center rounded-lg text-gray-800 font-bold shadow hover:scale-105 transition"
                                            style={{ backgroundColor: bg }}
                                        >
                                            <span className="text-s">{number}</span>
                                            <span className="text-s text-gray-600">
                                                {days_since >= 0 ? days_since : "∞"}
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>

                            {/* Superzahl */}
                            <div className="grid grid-cols-5 gap-1">
                                {Array.from({ length: 10 }, (_, i) => {
                                    const number = i;

                                    const item = state.lotto6aus49_not_drawn.find(
                                        d => d.type === "super" && d.number === number
                                    );

                                    const last_drawn = item?.last_drawn || "Never";
                                    const days_since = item?.days_since ?? -1;

                                    const bg = days_since >= 0
                                        ? getPastelColor(days_since, minPct6, maxPct6)
                                        : "#ddd";

                                    return (
                                        <div
                                            key={`lotto-super-${number}`}
                                            title={`Superzahl: ${number} | Last drawn: ${last_drawn} | Days since: ${days_since}`}
                                            className="w-14 h-14 flex flex-col items-center justify-center rounded-lg text-gray-800 font-bold shadow hover:scale-105 transition"
                                            style={{ backgroundColor: bg }}
                                        >
                                            <span className="text-s">{number}</span>
                                            <span className="text-s text-gray-600">
                                                {days_since >= 0 ? days_since : "∞"}
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                        {/* EUROJACKPOT */}
                        <div className="flex flex-col gap-4 items-center">
                            <h3 className="text-xl font-bold text-black">Eurojackpot</h3>

                            {/* Main Numbers */}
                            <div className="grid grid-cols-10 gap-1">
                                {Array.from({ length: 50 }, (_, i) => {
                                    const number = i + 1;

                                    const item = state.eurojackpot_not_drawn.find(
                                        d => d.type === "main" && d.number === number
                                    );

                                    const last_drawn = item?.last_drawn || "Never";
                                    const days_since = item?.days_since ?? -1;

                                    const bg = days_since >= 0
                                        ? getPastelColor(days_since, minPct7, maxPct7)
                                        : "#ddd";

                                    return (
                                        <div
                                            key={`euro-main-${number}`}
                                            title={`Number: ${number} | Last drawn: ${last_drawn} | Days since: ${days_since}`}
                                            className="w-14 h-14 flex flex-col items-center justify-center rounded-lg text-gray-800 text-sm font-bold shadow hover:scale-105 transition"
                                            style={{ backgroundColor: bg }}
                                        >
                                            <span className="text-s">{number}</span>
                                            <span className="text-s text-gray-600">
                                                {days_since >= 0 ? days_since : "∞"}
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>

                            {/* Eurozahlen */}
                            <div className="grid grid-cols-6 gap-1">
                                {Array.from({ length: 12 }, (_, i) => {
                                    const number = i + 1;

                                    const item = state.eurojackpot_not_drawn.find(
                                        d => d.type === "euro" && d.number === number
                                    );

                                    const last_drawn = item?.last_drawn || "Never";
                                    const days_since = item?.days_since ?? -1;

                                    const bg = days_since >= 0
                                        ? getPastelColor(days_since, minPct7, maxPct7)
                                        : "#ddd";

                                    return (
                                        <div
                                            key={`euro-special-${number}`}
                                            title={`Eurozahl: ${number} | Last drawn: ${last_drawn} | Days since: ${days_since}`}
                                            className="w-14 h-14 flex flex-col items-center justify-center rounded-lg text-gray-800 text-sm font-bold shadow hover:scale-105 transition"
                                            style={{ backgroundColor: bg }}
                                        >
                                            <span className="text-s">{number}</span>
                                            <span className="text-s text-gray-600">
                                                {days_since >= 0 ? days_since : "∞"}
                                            </span>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
    );
}