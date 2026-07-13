from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from bigmoney import *
from tools import *
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from typing import cast
from pydantic import BaseModel
from typing import List, Any
import time

load_dotenv(Path(__file__).resolve().parents[1] / ".env")
env = os.getenv("TSV_PATH")

L49file = f"{env}/lotto_6aus49_ab_02.12.2000.txt"
EJfile = f"{env}/eurojackpot.txt"
Kfile = f"{env}/keno.txt"
Super6file = f"{env}/super6.txt"
Spiel77file = f"{env}/spiel77.txt"
Glücksradfile = f"{env}/gs.txt"

TS_NUM_COUNT = f"{os.getenv('BASE_PATH')}/ts_num_count.json"

app = FastAPI()

# allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class MatchRequest(BaseModel):
    type: str
    numbers: Any
    supernum: Any


@app.get("/data_lotto6aus49")
def get_lotto6aus49_data():
    try:
        df = pd.read_csv(L49file, sep="\t")
        df = df.fillna(value="")
        # Sort by date descending (most recent first)
        df['date'] = pd.to_datetime(df[['Jahr', 'Monat', 'Tag']].rename(columns={'Jahr': 'year', 'Monat': 'month', 'Tag': 'day'}))
        df = df.sort_values('date', ascending=False)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/data_eurojackpot")
def get_eurojackpot_data():
    try:
        df = pd.read_csv(EJfile, sep="\t")
        df = df.fillna(value="")
        # Sort by date descending (most recent first)
        df['date'] = pd.to_datetime(df[['Jahr', 'Monat', 'Tag']].rename(columns={'Jahr': 'year', 'Monat': 'month', 'Tag': 'day'}))
        df = df.sort_values('date', ascending=False)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/data_keno")
def get_keno_data():
    try:
        df = pd.read_csv(Kfile, sep="\t")
        df = df.fillna(value="")
        df['date'] = pd.to_datetime(df[['Jahr', 'Monat', 'Tag']].rename(columns={'Jahr': 'year', 'Monat': 'month', 'Tag': 'day'}))
        df = df.sort_values('date', ascending=False)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/data_super6")
def get_super6_data():
    try:
        df = pd.read_csv(Super6file, sep="\t")
        df = df.fillna(value="")
        df['date'] = pd.to_datetime(df[['Jahr', 'Monat', 'Tag']].rename(columns={'Jahr': 'year', 'Monat': 'month', 'Tag': 'day'}))
        df = df.sort_values('date', ascending=False)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/data_spiel77")
def get_spiel77_data():
    try:
        df = pd.read_csv(Spiel77file, sep="\t")
        df = df.fillna(value="")
        df['date'] = pd.to_datetime(df[['Jahr', 'Monat', 'Tag']].rename(columns={'Jahr': 'year', 'Monat': 'month', 'Tag': 'day'}))
        df = df.sort_values('date', ascending=False)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/data_glücksrad")
def get_glücksrad_data():
    try:
        df = pd.read_csv(Glücksradfile, sep="\t")
        df = df.fillna(value="")
        df = df.drop(columns=["VA", "Spieleinsatz(EUR)"], errors="ignore")
        df['date'] = pd.to_datetime(df[['Jahr', 'Monat', 'Tag']].rename(columns={'Jahr': 'year', 'Monat': 'month', 'Tag': 'day'}))
        df = df.sort_values('date', ascending=False)
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/heatmap_eurojackpot")
def heatmap_eurojackpot():
    try:
        df = pd.read_csv(EJfile, sep="\t")
        a_cols = ["ZahlA1", "ZahlA2", "ZahlA3", "ZahlA4", "ZahlA5"]
        all_a_values = df[a_cols].stack()
        freq = all_a_values.value_counts()
        result = freq.reset_index()
        result.columns = ["number", "value"]
        result = result.sort_values("number", ascending=True)
        total_draws = all_a_values.shape[0]
        result["percent"] = (result["value"] / total_draws) * 100
        result = result.to_dict(orient="records")
        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/heatmap_eurojackpot_eurozahl")
def heatmap_eurojackpot_eurozahl():
    try:
        df = pd.read_csv(EJfile, sep="\t")
        a_cols = ["ZahlB1", "ZahlB2"]
        all_a_values = df[a_cols].stack()
        freq = all_a_values.value_counts()
        result = freq.reset_index()
        result.columns = ["number", "value"]
        result = result.sort_values("number", ascending=True)
        total_draws = all_a_values.shape[0]
        result["percent"] = (result["value"] / total_draws) * 100
        result = result.to_dict(orient="records")
        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/heatmap_lotto6aus49")
def heatmap_lotto6aus49():
    try:
        df = pd.read_csv(L49file, sep="\t")
        a_cols = ["Zahl1", "Zahl2", "Zahl3", "Zahl4", "Zahl5", "Zahl6"]
        all_a_values = df[a_cols].stack()
        freq = all_a_values.value_counts()
        result = freq.reset_index()
        result.columns = ["number", "value"]
        result = result.sort_values("number", ascending=True)
        total_draws = all_a_values.shape[0]
        result["percent"] = (result["value"] / total_draws) * 100
        result = result.to_dict(orient="records")
        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/heatmap_lotto6aus49_superzahl")
def heatmap_lotto6aus49_superzahl():
    try:
        df = pd.read_csv(L49file, sep="\t")
        all_a_values = df["Super"]
        freq = all_a_values.value_counts()
        result = freq.reset_index()
        result.columns = ["number", "value"]
        result = result.sort_values("number", ascending=True)
        total_draws = len(all_a_values)
        result["percent"] = (result["value"] / total_draws) * 100
        return result.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}


@app.get("/heatmap_lotto6aus49_not_drawn_since")
def heatmap_lotto6aus49_not_drawn_since():
    try:
        df = pd.read_csv(L49file, sep="\t")
        z_mask = {i: -1 for i in range(1, 50)}
        s_mask = {i: -1 for i in range(0, 10)}
        result = []
        for i, row in enumerate(df.iloc[::-1].itertuples(index=False)):
            z = [row.Zahl1, row.Zahl2, row.Zahl3, row.Zahl4, row.Zahl5, row.Zahl6]
            s = cast(int, row.Super)
            dt = datetime(cast(int,row.Jahr), cast(int,row.Monat), cast(int,row.Tag)).strftime("%d-%m-%Y")
            for j in z:
                j = cast(int, j)
                if z_mask[j] == -1:
                    z_mask[j] = i
                    result.append({
                        "type": "main",
                        "number": j,
                        "draw_date": dt,
                        "last_drawn": z_mask[j]
                    })
            if s_mask[s] == -1:
                s_mask[s] = i
                result.append({
                    "type": "super",
                    "number": s,
                    "draw_date": dt,
                    "last_drawn": s_mask[s]
                })
            if all(value >= 0 for value in z_mask.values()) and all(value >= 0 for value in s_mask.values()):
                return sorted(result, key=lambda x: (0 if x['type'] == 'main' else 1, x['number']))
    except Exception as e:
        return {"error": str(e)}


@app.get("/heatmap_eurojackpot_not_drawn_since")
def heatmap_eurojackpot_not_drawn_since():
    try:
        df = pd.read_csv(EJfile, sep="\t")
        z_mask = {i: -1 for i in range(1, 51)}
        e_mask = {i: -1 for i in range(1, 13)}
        result = []
        for i, row in enumerate(df.iloc[::-1].itertuples(index=False)):
            z = [row.ZahlA1, row.ZahlA2, row.ZahlA3, row.ZahlA4, row.ZahlA5]
            e = [row.ZahlB1, row.ZahlB2]
            dt = datetime(cast(int,row.Jahr), cast(int,row.Monat), cast(int,row.Tag)).strftime("%d-%m-%Y")
            for j in z:
                j = cast(int, j)
                if z_mask[j] == -1:
                    z_mask[j] = i
                    result.append({
                        "type": "main",
                        "number": j,
                        "draw_date": dt,
                        "last_drawn": z_mask[j]
                    })
            for j in e:
                j = cast(int, j)
                if e_mask[j] == -1:
                    e_mask[j] = i
                    result.append({
                        "type": "euro",
                        "number": j,
                        "draw_date": dt,
                        "last_drawn": e_mask[j]
                    })
            if all(value >= 0 for value in z_mask.values()) and all(value >= 0 for value in e_mask.values()):
                return sorted(result, key=lambda x: (0 if x['type'] == 'main' else 1, x['number']))
    except Exception as e:
        return {"error": str(e)}


@app.get("/randomEurojackpot")
def randomEurojackpot(mode: int = 1, qtipps: int = 1, count1: int = 5, count2: int = 2, threshold: int = 3):
    if (count1 == 5 or count1 == 6) and (count2 >= 2 or count2 <= 12):
        pass
    elif count1 == 7 and (count2 >= 2 or count2 <= 7):
        pass
    elif count1 == 8 and (count2 >= 2 or count2 <= 4):
        pass
    elif count1 == 9 and (count2 >= 2 or count2 <= 3):
        pass
    elif (count1 == 10 or count1 == 11) and count2 == 2:
        pass
    else:
        return
    
    euro = Eurojackpot(EJfile)
    setlist = []
    supernum = []
    history = []

    if mode == 1:
        for _ in range(qtipps):
            euro.choose(5, 2)
            setlist.append(euro.set)
            supernum.append(euro.num)
            history.append(euro.check_history(threshold))
    else:
        euro.choose(count1, count2)
        setlist.append(euro.set)
        supernum.append(euro.num)
        history.append(euro.check_history(threshold))

    setlist = [x.tolist() for x in setlist]
    supernum = [x.tolist() for x in supernum]
    history = clean_history(history)

    return {
        "setlist": setlist,
        "supernum": supernum,
        "history": history
    }
    

@app.get("/random_6aus49")
def random_6aus49(button: int = 6, mode: int = 1, threshold: int = 4):
    lotto49 = Lotto49(L49file)
    setlist = []
    supernum = []
    history = []

    match mode:
        case 1:
            for _ in range(button):
                lotto49.choose()
                setlist.append(lotto49.set)
                supernum.append(lotto49.num)
                history.append(lotto49.check_history(threshold))
        case 2:
            with open(TS_NUM_COUNT, "r") as f:
                k = json.load(f)
            lotto49.choose(k.get(f"{button}"))
            setlist = get_sets(lotto49.set, f"{button}")
            supernum.append(lotto49.num)
            history.append(lotto49.check_history(threshold, ts=f"{button}"))
        case 3:
            lotto49.choose(button)
            setlist = get_sets(lotto49.set)
            supernum.append(lotto49.num)
            history.append(lotto49.check_history(threshold))
        case _:
            pass

    setlist = [x.tolist() for x in setlist]
    supernum = [x.tolist() for x in supernum]
    history = clean_history(history)

    return {
        "setlist": setlist,
        "supernum": supernum,
        "history": history
    }


@app.get("/random_keno")
def random_keno(typ: int = 10):
    keno = Keno(typ, Kfile)
    keno.choose()
    # arrow_data = keno_arrow(setlist)
    # return Response(
    #     content=arrow_data,
    #     media_type="application/octet-stream",
    #     headers={"Content-Disposition": "attachment; filename=lotto.arrow"}
    # )
