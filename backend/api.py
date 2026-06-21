from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from bigmoney import *
from tools import *
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(Path(__file__).resolve().parents[1] / ".env")
env = os.getenv("TSV_PATH")

L49file = f"{env}/lotto_6aus49_ab_02.12.2000.txt"
EJfile = f"{env}/eurojackpot.txt"
Kfile = f"{env}/keno.txt"
Super6file = f"{env}/super6.txt"
Spiel77file = f"{env}/spiel77.txt"
Glücksradfile = f"{env}/gs.txt"


ts_num_count = "ts_num_count.json"

app = FastAPI()

# allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/heatmap_lotto6aus49_not_drawn")
def heatmap_lotto6aus49_not_drawn():
    try:
        df = pd.read_csv(L49file, sep="\t")

        df['date'] = pd.to_datetime(
            df[['Jahr', 'Monat', 'Tag']].rename(
                columns={
                    'Jahr': 'year',
                    'Monat': 'month',
                    'Tag': 'day'
                }
            )
        )

        df = df.sort_values('date', ascending=False)

        main_cols = [
            "Zahl1", "Zahl2", "Zahl3",
            "Zahl4", "Zahl5", "Zahl6"
        ]

        result = []

        for number in range(1, 50):
            mask = df[main_cols].isin([number]).any(axis=1)
            matching_rows = df[mask]

            if len(matching_rows) > 0:
                last_drawn_date = matching_rows.iloc[0]['date']
                days_since = (pd.Timestamp.now() - last_drawn_date).days
            else:
                last_drawn_date = None
                days_since = -1

            result.append({
                "type": "main",
                "number": number,
                "last_drawn": last_drawn_date.strftime("%Y-%m-%d") if last_drawn_date else None,
                "days_since": int(days_since) if days_since >= 0 else -1
            })

        for number in range(0, 10):
            mask = df["Super"] == number
            matching_rows = df[mask]

            if len(matching_rows) > 0:
                last_drawn_date = matching_rows.iloc[0]['date']
                days_since = (pd.Timestamp.now() - last_drawn_date).days
            else:
                last_drawn_date = None
                days_since = -1

            result.append({
                "type": "super",
                "number": number,
                "last_drawn": last_drawn_date.strftime("%Y-%m-%d") if last_drawn_date else None,
                "days_since": int(days_since) if days_since >= 0 else -1
            })

        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/heatmap_eurojackpot_not_drawn")
def heatmap_eurojackpot_not_drawn():
    try:
        df = pd.read_csv(EJfile, sep="\t")

        df['date'] = pd.to_datetime(
            df[['Jahr', 'Monat', 'Tag']].rename(
                columns={
                    'Jahr': 'year',
                    'Monat': 'month',
                    'Tag': 'day'
                }
            )
        )

        df = df.sort_values('date', ascending=False)

        main_cols = [
            "ZahlA1", "ZahlA2", "ZahlA3",
            "ZahlA4", "ZahlA5"
        ]

        euro_cols = [
            "ZahlB1", "ZahlB2"
        ]

        result = []

        for number in range(1, 51):
            mask = df[main_cols].isin([number]).any(axis=1)
            matching_rows = df[mask]

            if len(matching_rows) > 0:
                last_drawn_date = matching_rows.iloc[0]['date']
                days_since = (pd.Timestamp.now() - last_drawn_date).days
            else:
                last_drawn_date = None
                days_since = -1

            result.append({
                "type": "main",
                "number": number,
                "last_drawn": last_drawn_date.strftime("%Y-%m-%d") if last_drawn_date else None,
                "days_since": int(days_since) if days_since >= 0 else -1
            })

        # Euro numbers 1-12
        for number in range(1, 13):
            mask = df[euro_cols].isin([number]).any(axis=1)
            matching_rows = df[mask]

            if len(matching_rows) > 0:
                last_drawn_date = matching_rows.iloc[0]['date']
                days_since = (pd.Timestamp.now() - last_drawn_date).days
            else:
                last_drawn_date = None
                days_since = -1

            result.append({
                "type": "euro",
                "number": number,
                "last_drawn": last_drawn_date.strftime("%Y-%m-%d") if last_drawn_date else None,
                "days_since": int(days_since) if days_since >= 0 else -1
            })

        return result
    except Exception as e:
        return {"error": str(e)}


@app.get("/randomEurojackpot")
def randomEurojackpot(mode: int = 1, qtipps: int = 1, count1: int = 5, count2: int = 2):
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

    if mode == 1:
        for _ in range(qtipps):
            euro.choose(5, 2)
            setlist.append(euro.set)
            supernum.append(euro.num)
    else:
        euro.choose(count1, count2)
        setlist.append(euro.set)
        supernum.append(euro.num)
    
    arrow_data = eurojackpot_arrow(setlist, supernum)
    return Response(
        content=arrow_data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=lotto.arrow"}
    )


@app.get("/random_6aus49")
def random_6aus49(button: int = 6, mode: int = 1):
    lotto49 = Lotto49(L49file)
    setlist = []
    supernum = []
    match mode:
        case 1:
            for _ in range(button):
                lotto49.choose()
                setlist.append(lotto49.set)
                supernum.append(lotto49.num)
        case 2:
            with open(ts_num_count, "r") as f:
                count = json.load(f)
            lotto49.choose(count.get(f"{button}"))
            setlist = get_sets(lotto49.set, f"{button}")
            supernum.append(lotto49.num)
        case 3:
            lotto49.choose(button)
            setlist = get_sets(lotto49.set)
            supernum.append(lotto49.num)
        case _:
            pass
    arrow_data = lotto_arrow(setlist, supernum)
    return Response(
        content=arrow_data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": "attachment; filename=lotto.arrow"}
    )


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
