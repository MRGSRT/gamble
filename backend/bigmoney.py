import numpy as np
import pandas as pd
import json
import glob
import os

from tqdm import tqdm
from itertools import combinations
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime


load_dotenv(Path(__file__).resolve().parents[1] / ".env")
TS_PATTERN = f"{os.getenv('BASE_PATH')}/ts_patterns.json"
CSV_PATH = os.getenv("CSV_PATH")


class Lotto:

    def __init__(self, file):
        self.set = []
        self.num = []
        self.history = file
        self.unique = False


class Lotto49(Lotto):

    def __init__(self, file):
        super().__init__(file)
        self.numPool49 = [i for i in range(1, 50)]
        self.superNum = [i for i in range(10)]

    def shuffle(self):
        np.random.default_rng()
        np.random.shuffle(self.numPool49)
        np.random.shuffle(self.superNum)

    def choose(self, k=6):
        np.random.default_rng()
        self.unique = False
        self.set = np.sort(np.random.choice(
            self.numPool49, k, replace=False), axis=0)
        self.num = np.random.choice(self.superNum, 1)

    def check_history(self, threshold=6, ts=""):
        self.unique = True
        orig = pd.read_csv(self.history, sep="\t").drop(
            ["Zusatz"], axis=1).values
        num = (pd.read_csv(self.history, sep="\t").
               drop(["Tag", "Monat", "Jahr", "Zusatz", "Super"], axis=1).
               values)
        supernum = (pd.read_csv(self.history, sep="\t", usecols=["Super"]).
                    values)
        matches = []
        if ts != "":
            with open(TS_PATTERN, "r") as f:
                all_patterns = json.load(f)
            pattern = all_patterns.get(ts, [])
            sets = [[self.set[i - 1] for i in s] for s in pattern]
            sets = np.array([sorted(s) for s in sets])
            for i in range(len(sets) - 1):
                for j in range(num.shape[0]):
                    new_matches = add_matches(matches, orig[i][0], orig[i][1], orig[i][2],
                                              sets[i], num[j], threshold, self.num, supernum[j])
                    if matches != new_matches:
                        self.unique = False
        else:
            for i in range(num.shape[0]):
                new_matches = add_matches(matches, orig[i][0], orig[i][1], orig[i][2],
                                          self.set, num[i], threshold, self.num, supernum[i])
                if matches != new_matches:
                    self.unique = False

        matches.sort(key=lambda x: x["date_"])
        return matches

    def check_history_and_print(self, threshold=5, ts=""):
        matches = self.check_history(threshold, ts)
        print_matches(matches)
        self.print()

    def print(self):
        print(f"Set: {self.set}\nSuper: {self.num}\n")

    def write_down(self, file):
        with open(file, "a") as f:
            set_size = len(self.set)
            for i in range(set_size):
                if i < set_size:
                    f.write(f"{self.set[i]},")
            f.write(f"{self.num[0]}\n")
        f.close()

    def get_sets(self, ts="", set_len=6):
        return get_sets(self.set, ts, set_len)


class Eurojackpot(Lotto):

    def __init__(self, file):
        super().__init__(file)
        self.numPoolJackpot = [i for i in range(1, 51)]
        self.superNums = [i for i in range(1, 13)]

    def shuffle(self):
        np.random.default_rng()
        # np.random.shuffle(self.numPoolJackpot)
        np.random.shuffle(self.superNums)

    def choose(self, k=5, s=2):
        np.random.default_rng()
        self.unique = False
        self.set = np.sort(np.random.choice(
            self.numPoolJackpot, k, replace=False), axis=0)
        self.num = np.sort(np.random.choice(
            self.superNums, s, replace=False), axis=0)

    def check_history(self, threshold=5):
        self.unique = True
        orig = pd.read_csv(self.history, sep="\t").values
        supernum = pd.read_csv(self.history, sep="\t")[
            ["ZahlB1", "ZahlB2"]].values
        num = pd.read_csv(self.history, sep="\t")[
            ["ZahlA1", "ZahlA2", "ZahlA3", "ZahlA4", "ZahlA5"]].values
        matches = []

        for i in range(num.shape[0]):
            new_matches = add_matches(matches, orig[i][0], orig[i][1], orig[i][2],
                                      self.set, num[i], threshold, self.num, supernum[i])
            if matches != new_matches:
                self.unique = False
        matches.sort(key=lambda x: x["date_"])
        return matches

    def check_history_and_print(self, threshold=5):
        matches = self.check_history(threshold)
        print_matches(matches)
        self.print()

    def print(self):
        print(f"Set: {self.set}\nSuper: {self.num}\n")

    def write_down(self, file):
        with open(file, "a") as f:
            set_size = len(self.set)
            for i in range(set_size):
                if i < set_size:
                    f.write(f"{self.set[i]},")
            for i in range(len(self.num)-1):
                f.write(f"{self.num[i]},")
            f.write(f"{self.num[-1]}\n")
        f.close()


class Keno(Lotto):

    def __init__(self, typ, file):
        super().__init__(file)
        self.numPoolKeno = [i for i in range(1, 71)]
        self.typ = typ

    def shuffle(self):
        np.random.default_rng()
        np.random.shuffle(self.numPoolKeno)

    def choose(self):
        np.random.default_rng()
        self.unique = False
        self.set = np.sort(np.random.choice(
            self.numPoolKeno, self.typ, replace=False), axis=0)

    def check_history(self, threshold=10):
        self.unique = True
        orig = pd.read_csv(self.history, sep="\t").values
        num = (pd.read_csv(self.history, sep="\t").
               drop(["Tag", "Monat", "Jahr", "VA"], axis=1).
               values)
        matches = []
        for i in range(num.shape[0]):
            matches = add_matches(matches, orig[i][0], orig[i][1], orig[i][2],
                                  self.set, num[i], threshold, None, None)
        matches.sort(key=lambda x: x["date_"])
        return matches

    def check_history_and_print(self, threshold=5):
        matches = self.check_history(threshold)
        print_matches(matches)
        self.print()

    def print(self):
        print(f"Set: {self.set}\n")

    def write_down(self, file):
        with open(file, "a") as f:
            f.write(",".join(map(str, self.set)) + "\n")
        f.close()


def show_dups(file):
    if "6aus49" in file:
        print("6aus49")
        a1 = pd.read_csv(file, sep="\t")[
            ["Zahl1", "Zahl2", "Zahl3", "Zahl4", "Zahl5", "Zahl6"]].values
        a1.sort()
        temp = pd.read_csv(file, sep="\t")["Super"].to_numpy().reshape(-1, 1)

        a2 = np.hstack((a1, temp))
        _, idx, counts = np.unique(
            a1, axis=0, return_index=True, return_counts=True)
        duplicates = a1[idx[counts > 1]]
        print(f"Duplicates: {duplicates}")
        _, idx, counts = np.unique(
            a2, axis=0, return_index=True, return_counts=True)
        duplicates = a2[idx[counts > 1]]
        print(f"Duplicates SuperNum: {duplicates}\n")

    if "eurojackpot" in file:
        print("Eurojackpot")
        a1 = pd.read_csv(file, sep="\t")[
            ["ZahlA1", "ZahlA2", "ZahlA3", "ZahlA4", "ZahlA5"]].values
        temp = pd.read_csv(file, sep="\t")[["ZahlB1", "ZahlB2"]].values
        a1.sort()
        temp.sort()
        a2 = np.hstack((a1, temp))

        _, idx, counts = np.unique(
            a1, axis=0, return_index=True, return_counts=True)
        duplicates = a1[idx[counts > 1]]
        print(f"Duplicates: {duplicates}")
        _, idx, counts = np.unique(
            a2, axis=0, return_index=True, return_counts=True)
        duplicates = a2[idx[counts > 1]]
        print(f"Duplicates SuperNum: {duplicates}\n")

    if "keno" in file:
        print("Keno")
        a1 = (pd.read_csv(file, sep="\t").
              drop(["Tag", "Monat", "Jahr", "VA"], axis=1).
              values)
        _, idx, counts = np.unique(
            a1, axis=0, return_index=True, return_counts=True)
        duplicates = a1[idx[counts > 1]]
        print(f"Duplicates: {duplicates}\n")

    else:
        return


def check_num(file, arr, sz=None, threshold_49=6, threshold_euro=5, threshold_keno=10):
    matches = []
    if "6aus49" in file:
        print(f"Lotto49: {arr}")
        orig = pd.read_csv(file, sep="\t").drop(["Zusatz"], axis=1).values
        num = (pd.read_csv(file, sep="\t").
               drop(["Tag", "Monat", "Jahr", "Zusatz", "Super"], axis=1).
               values)
        supernum = (pd.read_csv(file, sep="\t", usecols=["Super"]).
                    values)
        for i in range(num.shape[0]):
            matches = add_matches(matches, orig[i][0], orig[i][1], orig[i][2],
                                  arr, num[i], threshold_49, sz, supernum[i])
    if "eurojackpot" in file:
        print(f"Eurojackpot: {arr}")
        orig = pd.read_csv(file, sep="\t").values
        supernum = pd.read_csv(file, sep="\t")[["ZahlB1", "ZahlB2"]].values
        num = pd.read_csv(file, sep="\t")[
            ["ZahlA1", "ZahlA2", "ZahlA3", "ZahlA4", "ZahlA5"]].values
        for i in range(num.shape[0]):
            matches = add_matches(matches, orig[i][0], orig[i][1], orig[i][2],
                                  arr, num[i], threshold_euro, sz, supernum[i])
    if "keno" in file:
        print(f"Keno: {arr}")
        orig = pd.read_csv(file, sep="\t").values
        num = (pd.read_csv(file, sep="\t").
               drop(["Tag", "Monat", "Jahr", "VA"], axis=1).
               values)
        for i in range(num.shape[0]):
            matches = add_matches(matches, orig[i][0], orig[i][1], orig[i][2],
                                  arr, num[i], threshold_keno)
    matches.sort(key=lambda x: x["date_"])
    return matches


def check_used_num(used_euro, used_49, used_keno, EJ, L49, K, threshold_49=6, threshold_euro=5, threshold_keno=10, date_threshold=0):
    return (check_num_49(used_49, L49, threshold_49, date_threshold),
            check_num_euro(used_euro, EJ, threshold_euro, date_threshold),
            check_num_keno(used_keno, K, threshold_keno, date_threshold))


def check_num_49(used_df, df, threshold=6, date_threshold=0):
    l1 = pd.read_csv(df, sep="\t").drop(["Zusatz"], axis=1)
    l2 = pd.read_csv(used_df, sep=",").values
    l1 = l1[l1.iloc[:, 2] >= date_threshold].values
    matches = []
    for i in tqdm(l2, desc="Checking Lotto49"):
        sz = i[-1]
        for j in l1:
            matches = add_matches(matches, j[0], j[1], j[2],
                                  i[0:6], j[3:9], threshold, sz, j[9])
    matches.sort(key=lambda x: x["date_"])
    return matches


def check_num_49_vs(used_df, df, threshold=6, date_threshold=0):
    l1 = pd.read_csv(df, sep="\t").drop(["Zusatz"], axis=1)
    l2 = pd.read_csv(used_df, sep=",").values
    vs = used_df.split("6aus")[-1].split(".")[0]
    l1 = l1[l1.iloc[:, 2] >= date_threshold].values
    matches = []
    for i in tqdm(l2, desc=f"Checking Lotto49 VS 6aus{vs}"):
        sz = i[-1]
        for j in l1:
            matches = add_matches(matches, j[0], j[1], j[2],
                                  i[:len(i)-1], j[3:9], threshold, sz, j[9])
    matches.sort(key=lambda x: x["date_"])
    return matches


def check_num_49_ts(used_df, df, threshold=6, date_threshold=0):
    l1 = pd.read_csv(df, sep="\t").drop(["Zusatz"], axis=1)
    l2 = pd.read_csv(used_df, sep=",").values
    ts = used_df.split("_")[-1].split(".")[0]
    l1 = l1[l1.iloc[:, 2] >= date_threshold].values
    with open(TS_PATTERN, "r") as f:
        all_patterns = json.load(f)
    pattern = all_patterns.get(ts, [])
    matches = []
    for x in tqdm(l2, desc=f"Checking Lotto49 TS {ts}"):
        sets = [[x[i - 1] for i in s] for s in pattern]
        sets = np.array([sorted(s) for s in sets])
        sz = x[-1]
        for s in tqdm(sets, leave=False):
            for j in l1:
                matches = add_matches(matches, j[0], j[1], j[2],
                                      s, j[3:9], threshold, sz, j[9])
    matches.sort(key=lambda x: x["date_"])
    return matches


def check_num_all_ts(df, file_pattern, threshold=6, date_threshold=0):
    f = glob.glob(f"{CSV_PATH}/{file_pattern}*.csv")
    l = []
    for i in f:
        a = check_num_49_ts(i, df, threshold, date_threshold)
        l.append(a)
        print_matches(a)
    return [i for sublist in l for i in sublist]


def check_num_all_vs(df, file_pattern, threshold=6, date_threshold=0):
    f = glob.glob(f"{CSV_PATH}/{file_pattern}*.csv")
    l = []
    for i in f:
        a = check_num_49_vs(i, df, threshold, date_threshold)
        l.append(a)
        print_matches(a)
    return [i for sublist in l for i in sublist]


def check_num_all_49(df, fp_ts, fp_vs, threshold=6, date_threshold=0):
    return check_num_all_ts(df, fp_ts, threshold, date_threshold) + check_num_all_vs(df, fp_vs, threshold, date_threshold)


def check_num_euro(used_df, df, threshold=5, date_threshold=0):
    e1 = pd.read_csv(df, sep="\t")
    e2 = pd.read_csv(used_df, sep=",").values
    e1 = e1[e1.iloc[:, 2] >= date_threshold].values
    matches = []
    for i in tqdm(e2, desc="Checking Eurojackpot"):
        for j in e1:
            matches = add_matches(matches, j[0], j[1], j[2],
                                  i[0:5], j[3:8], threshold, i[5:7], j[8:10])
    matches.sort(key=lambda x: x["date_"])
    return matches


def check_num_keno(used_df, df, threshold=10, date_threshold=0):
    k1 = pd.read_csv(df, sep="\t").drop(["VA"], axis=1)
    k2 = pd.read_csv(used_df, sep=",").values
    k1 = k1[k1.iloc[:, 2] >= date_threshold].values
    matches = []
    for i in tqdm(k2, desc="Checking Keno"):
        for j in k1:
            matches = add_matches(matches, j[0], j[1], j[2],
                                  i, j[3:], threshold)
    matches.sort(key=lambda x: x["date_"])
    return matches


def add_matches(matches, day, month, year, current_numbers, historical_set, threshold=3, current_supernum=None, historical_supernum=None):
    """
    Compare two lottery number sets and append matching draw information if they
    meet the required similarity threshold.

    The function counts how many lottery numbers in ``current_numbers`` are also present in
    ``historical_set``. If the number of matching values is greater than or equal to
    ``threshold``, a dictionary containing the draw date, matching statistics,
    and common numbers is appended to ``matches``.

    Parameters
    ----------
    matches : list
        List of dictionaries describing matching lottery draws.
    day : int or str
        Day of the draw.
    month : int or str
        Month of the draw.
    year : int or str
        Year of the draw.
    current_numbers : array-like
        Lottery numbers being compared.
    historical_set : array-like
        Already drawn sorted lottery numbers.
    current_supernum : array-like or scalar
        Super number(s) associated with ``current_numbers``.
    historical_supernum : array-like or scalar
        Sorted Super number(s) associated with the drawn numbers (``historical_set``).
    threshold : int
        Minimum number of matching lottery numbers required before a match is
        recorded.

    Returns
    -------
    list
        The updated ``matches`` list.

    Notes
    -----
    Each appended dictionary contains the following keys:

    - ``date_`` : ``datetime`` object representing the draw date.
    - ``date`` : Draw date formatted as ``DD.MM.YYYY``.
    - ``numbers`` : The candidate lottery numbers (``current_numbers``).
    - ``supernum`` : Super number(s) associated with ``current_numbers``.
    - ``historical_numbers`` : The already drawn lottery numbers (``historical_set``).
    - ``historical_supernum`` : Super number(s) associated with ``historical_set``.
    - ``num_sum`` : Number of matching lottery numbers.
    - ``super_sum`` : Number of matching super numbers.
    - ``common`` : NumPy array containing the lottery numbers common to both sets.
    """

    num_sum = int(np.isin(current_numbers, historical_set).sum())
    if num_sum >= threshold:
        if isinstance(historical_supernum, np.ndarray):
            historical_supernum = np.sort(historical_supernum)
        super_sum = 0 if current_supernum is None or historical_supernum is None else int(
            np.isin(current_supernum, historical_supernum).sum())
        common = np.intersect1d(current_numbers, historical_set)
        date = datetime(int(year), int(month), int(day))
        matches.append({
            "date_": date,
            "date": date.strftime("%d.%m.%Y"),
            "numbers": current_numbers,
            "supernum": current_supernum,
            "historical_numbers": np.sort(historical_set),
            "historical_supernum": historical_supernum,
            "num_sum": num_sum,
            "super_sum": super_sum,
            "common": common
        })

    return matches


def print_matches(matches: list):
    if not matches:
        return

    for match in matches:
        try:
            num_sum = match["num_sum"]
            super_sum = match["super_sum"]
            historical_len = len((match["historical_numbers"]))
            keno = match["supernum"] is None and match["historical_supernum"] is None
            if (
                (super_sum == 1 and num_sum == 6 and historical_len == 6)
                or (super_sum == 2 and num_sum == 5 and historical_len == 5)
                or num_sum == 10
            ):
                emoji = "🔔🔔 💯 🔔🔔"

            elif (
                (super_sum == 0 and num_sum == 6 and historical_len == 6)
                or (super_sum == 1 and num_sum == 5 and historical_len == 5)
                or num_sum == 9
            ):
                emoji = "🔥"

            elif super_sum == 0 and num_sum == 5 and not keno:
                emoji = "⭕️"

            elif super_sum >= 2:
                emoji = "🟡 🟡"

            elif super_sum == 1:
                emoji = "🟡"

            else:
                emoji = ""

            if keno:
                print(
                    f'Found: {match["date"]:>12} {str(match["historical_numbers"]):<20}'
                    f' {str(match["numbers"]):<26} {str(match["common"]):>12} {emoji:<8}'
                )

            elif match["supernum"] is None:
                print(
                    f'Found: {match["date"]:>12} {str(match["historical_numbers"]):<6} '
                    f'{str(match["historical_supernum"]):<8}'
                    f' {str(match["numbers"]):<11} {str(match["common"]):>12} {emoji:<8}'
                )

            else:
                print(
                    f'Found: {match["date"]:>12} {str(match["historical_numbers"]):<6} '
                    f'{str(match["historical_supernum"]):<8}'
                    f' {str(match["numbers"]):<11} {str(str(match["supernum"])):<8}'
                    f' == {str(match["common"]):>12} {emoji:<8}'
                )
        except:
            pass


def clean_history(history: list):
    clean_history = []
    for item in history:
        rows = item if isinstance(item, list) else [item]

        for row in rows:
            clean_history.append({
                "date_": row["date_"].isoformat() if hasattr(row["date_"], "isoformat") else row["date_"],
                "date": row["date"],
                "numbers": row["numbers"].tolist(),
                "supernum": row["supernum"].tolist(),
                "historical_numbers": row["historical_numbers"].tolist(),
                "historical_supernum": row["historical_supernum"].tolist(),
                "num_sum": int(row["num_sum"]),
                "super_sum": int(row["super_sum"]),
                "common": row["common"].tolist(),
            })
    return clean_history


def get_sets(arr, ts="", set_len=6):
    if ts != "":
        with open(TS_PATTERN, "r") as f:
            all_patterns = json.load(f)
        pattern = all_patterns.get(ts, [])
        sets = [[arr[i - 1] for i in s] for s in pattern]
        sets = np.array([sorted(s) for s in sets])
        return sets
    return np.array(list(combinations(arr[:(len(arr))], set_len)))


def get_gewinnklassen(arr, winning_set, ts="", set_len=6, supernum=0, type="49"):
    all_combs = get_sets(arr, ts, set_len)
    gewinnklassen_euro = {
        (5, 2): "1 🔔🔔 💯 🔔🔔", (5, 1): "2 🔥", (5, 0): "3 ⭕️", (4, 2): "4 ♨️", (4, 1): "5 💤", (3, 2): "6",
        (4, 0): "7", (2, 2): "8", (3, 1): "9", (3, 0): "10", (1, 2): "11", (2, 1): "12"
    }
    gewinnklassen_49 = {
        (6, 1): "1 💯", (6, 0): "2 🔥", (5, 1): "3 ⭕️", (5, 0): "4 ♨️",
        (4, 1): "5 💤", (4, 0): "6", (3, 1): "7", (3, 0): "8", (2, 1): "9"
    }
    gewinnklassen_output = []
    if type == "49":
        for i in all_combs:
            common = np.intersect1d(i, winning_set)
            sum = len(common)
            if (sum > 1 and supernum >= 1) or sum >= 3:
                gewinnklassen_output.append(
                    f"{i} -- {winning_set} -- {common} - Gewinnklasse {gewinnklassen_49[(sum, supernum)]}")
    elif type == "euro":
        for i in all_combs:
            common = np.intersect1d(i, winning_set)
            sum = len(common)
            if (sum > 0 and supernum > 1) or (sum >= 2 and supernum >= 1):
                gewinnklassen_output.append(
                    f"{i} - Gewinnklasse {gewinnklassen_euro[(sum, supernum)]}")
    for i in gewinnklassen_output:
        print(f"{i}")
    return gewinnklassen_output


def get_gewinnklassen_from_csv(df, winning_set, ts="", set_len=6, supernum=0):
    df = pd.read_csv(df, sep=",").values
    for i in df:
        get_gewinnklassen(i, winning_set, ts, set_len, supernum)


def is_in(set, subset):
    return all(x in set.tolist() for x in subset)


if __name__ == "__main__":
    pass
