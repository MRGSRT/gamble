import numpy as np
import pandas as pd
import json
import glob
import os

from tqdm import tqdm
from itertools import combinations
from dotenv import load_dotenv
from pathlib import Path


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
        self.unique = True
        self.set = np.sort(np.random.choice(self.numPool49, k, replace=False), axis=0)
        self.num = np.random.choice(self.superNum, 1)

    def check_history(self, threshold=6, ts=""):
        self.unique = True
        orig = pd.read_csv(self.history, sep="\t").drop(["Zusatz"], axis=1).values
        num = (pd.read_csv(self.history, sep="\t").
               drop(["Tag", "Monat", "Jahr", "Zusatz", "Super"], axis=1).
               values)
        if ts != "":
            with open(TS_PATTERN, "r") as f:
                all_patterns = json.load(f)
            pattern = all_patterns.get(ts, [])
            sets = [[self.set[i - 1] for i in s] for s in pattern]
            sets = np.array([sorted(s) for s in sets])
            for i in range(len(sets)):
                for j in range(num.shape[0]):
                    sum = np.isin(sets[i], num[j]).sum()
                    common = np.intersect1d(sets[i], num[j])
                    if sum >= threshold:
                        print(f"Found: {orig[j][0:3]} {np.sort(orig[j][3:9])} {orig[j][9]} == {sum} | {sets[i]} {common}")
                        self.unique = False
        else:
            for i in range(num.shape[0]):
                sum = np.isin(self.set, num[i]).sum()
                common = np.intersect1d(self.set, num[i])
                if sum >= threshold:
                    print(f"Found: {orig[i][0:3]} {np.sort(orig[i][3:9])} {orig[i][9]} == {sum} | {common}")
                    self.unique = False

    def print(self):
        # print("Lotto49")
        # print(f"Lotto49Pool: {self.numPool49}\nSuperNum: {self.superNum}")
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
        self.unique = True
        self.set = np.sort(np.random.choice(self.numPoolJackpot, k, replace=False), axis=0)
        self.num = np.sort(np.random.choice(self.superNums, s, replace=False), axis=0)

    def check_history(self, threshold=5):
        self.unique = True
        orig = pd.read_csv(self.history, sep="\t").values
        supernum = pd.read_csv(self.history, sep="\t")[["ZahlB1", "ZahlB2"]].values
        num = pd.read_csv(self.history, sep="\t")[["ZahlA1", "ZahlA2", "ZahlA3", "ZahlA4", "ZahlA5"]].values
        for i in range(num.shape[0]):
            sum = np.isin(self.set, num[i]).sum()
            if sum >= threshold:
                print(f"Found: {orig[i][0:3]} {np.sort(orig[i][3:8])} {np.sort(orig[i][8:10])} == {sum}")
                self.unique = False

    def print(self):
        # print("Eurojackpot")
        # print(f"JackpotPool: {self.numPoolJackpot}\nSuperNums: {self.superNums}")
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
        self.unique = True
        self.set = np.sort(np.random.choice(self.numPoolKeno, self.typ, replace=False), axis=0)

    def check_history(self, threshold=10):
        self.unique = True
        orig = pd.read_csv(self.history, sep="\t").values
        num = (pd.read_csv(self.history, sep="\t").
               drop(["Tag", "Monat", "Jahr", "VA"], axis=1).
               values)
        for i in range(num.shape[0]):
            s = np.isin(self.set, num[i]).sum()
            if s >= threshold:
                print(f"Found: {orig[i][0:3]} {np.sort(orig[i][3::])} | {s}")
                self.unique = False

    def print(self):
        # print(f"Keno Typ {self.typ}")
        # print(f"KenoPool: {self.numPoolKeno}")
        print(f"Set: {self.set}\n")

    def write_down(self, file):
        with open(file, "a") as f:
            f.write(",".join(map(str, self.set)) + "\n")
        f.close()


def show_dups(file):
    if "6aus49" in file:
        print("6aus49")
        a1 = pd.read_csv(file, sep="\t")[["Zahl1", "Zahl2", "Zahl3", "Zahl4", "Zahl5", "Zahl6"]].values
        a1.sort()
        temp = pd.read_csv(file, sep="\t")["Super"].to_numpy().reshape(-1, 1)

        a2 = np.hstack((a1, temp))
        _, idx, counts = np.unique(a1, axis=0, return_index=True, return_counts=True)
        duplicates = a1[idx[counts > 1]]
        print(f"Duplicates: {duplicates}")
        _, idx, counts = np.unique(a2, axis=0, return_index=True, return_counts=True)
        duplicates = a2[idx[counts > 1]]
        print(f"Duplicates SuperNum: {duplicates}\n")

    if "eurojackpot" in file:
        print("Eurojackpot")
        a1 = pd.read_csv(file, sep="\t")[["ZahlA1", "ZahlA2", "ZahlA3", "ZahlA4", "ZahlA5"]].values
        temp = pd.read_csv(file, sep="\t")[["ZahlB1", "ZahlB2"]].values
        a1.sort()
        temp.sort()
        a2 = np.hstack((a1, temp))

        _, idx, counts = np.unique(a1, axis=0, return_index=True, return_counts=True)
        duplicates = a1[idx[counts > 1]]
        print(f"Duplicates: {duplicates}")
        _, idx, counts = np.unique(a2, axis=0, return_index=True, return_counts=True)
        duplicates = a2[idx[counts > 1]]
        print(f"Duplicates SuperNum: {duplicates}\n")

    if "keno" in file:
        print("Keno")
        a1 = (pd.read_csv(file, sep="\t").
               drop(["Tag", "Monat", "Jahr", "VA"], axis=1).
               values)
        _, idx, counts = np.unique(a1, axis=0, return_index=True, return_counts=True)
        duplicates = a1[idx[counts > 1]]
        print(f"Duplicates: {duplicates}\n")

    else:
        return


def check_num(file, arr, threshold_49=6, threshold_euro=5, threshold_keno=10):
    if "6aus49" in file:
        print(f"Lotto49: {arr}")
        orig = pd.read_csv(file, sep="\t").drop(["Zusatz"], axis=1).values
        num = (pd.read_csv(file, sep="\t").
               drop(["Tag", "Monat", "Jahr", "Zusatz", "Super"], axis=1).
               values)
        for i in range(num.shape[0]):
            sum = np.isin(arr, num[i]).sum()
            if sum >= threshold_49:
                print(f"Found: {orig[i][0:3]} {np.sort(orig[i][3:9])} {orig[i][9]} == {sum}")
    if "eurojackpot" in file:
        print(f"Eurojackpot: {arr}")
        orig = pd.read_csv(file, sep="\t").values
        supernum = pd.read_csv(file, sep="\t")[["ZahlB1", "ZahlB2"]].values
        num = pd.read_csv(file, sep="\t")[["ZahlA1", "ZahlA2", "ZahlA3", "ZahlA4", "ZahlA5"]].values
        for i in range(num.shape[0]):
            sum = np.isin(arr, num[i]).sum()
            if sum >= threshold_euro:
                print(f"Found: {orig[i][0:3]} {np.sort(orig[i][3:8])} {np.sort(orig[i][8:10])} == {sum}")
    if "keno" in file:
        print(f"Keno: {arr}")
        orig = pd.read_csv(file, sep="\t").values
        num = (pd.read_csv(file, sep="\t").
               drop(["Tag", "Monat", "Jahr", "VA"], axis=1).
               values)
        for i in range(num.shape[0]):
            s = np.isin(arr, num[i]).sum()
            if s >= threshold_keno:
                print(f"Found: {orig[i][0:3]} {np.sort(orig[i][3::])} | {s}")
    

def check_used_num(used_euro, used_49, used_keno, EJ, L49, K, threshold_49=6, threshold_euro=5, threshold_keno=10, date_threshold=0):
    check_num_49(used_49, L49, threshold_49, date_threshold)
    check_num_euro(used_euro, EJ, threshold_euro, date_threshold)
    check_num_keno(used_keno, K, threshold_keno, date_threshold)


def check_num_49(used_df, df, threshold=6, date_threshold=0):
    l1 = pd.read_csv(df, sep="\t").drop(["Zusatz"], axis=1)
    l2 = pd.read_csv(used_df, sep=",").values
    l1 = l1[l1.iloc[:, 2] >= date_threshold].values
    for i in tqdm(l2, desc="Checking Lotto49"):
        for j in l1:
            sum = np.isin(i[0:6], j[3:9]).sum()
            if sum >= threshold and i[6] != j[9]:
                x = np.sort(j[3:9])
                tqdm.write(f"Found match: {j[0:3]} {x} {j[9]} -- {i[0:6]} {i[6]} == {sum}")
            elif sum >= threshold and i[6] == j[9]:
                x = np.sort(j[3:9])
                tqdm.write(f"Found match: {j[0:3]} {x} {j[9]} -- {i[0:6]} {i[6]} == {sum} with SuperNum")


def check_num_49_vs(used_df, df, threshold=6, date_threshold=0):
    l1 = pd.read_csv(df, sep="\t").drop(["Zusatz"], axis=1)
    l2 = pd.read_csv(used_df, sep=",").values
    vs = used_df.split(".")[0].split("aus")[-1]
    l1 = l1[l1.iloc[:, 2] >= date_threshold].values
    for i in tqdm(l2, desc=f"Checking Lotto49 VS 6aus{vs}"):
        for j in l1:
            sum = np.isin(i[:len(i)-1], j[3:9]).sum()
            common = np.intersect1d(i[:len(i)-1], j[3:9])
            if sum >= threshold:
                tqdm.write(f"Found: {j[0:3]} {np.sort(j[3:9])} {j[9]} == {sum} | {i} -- {common}")


def check_num_49_ts(used_df, df, threshold=6, date_threshold=0):
    l1 = pd.read_csv(df, sep="\t").drop(["Zusatz"], axis=1)
    l2 = pd.read_csv(used_df, sep=",").values
    ts = used_df.split("_")[-1].split(".")[0]
    l1 = l1[l1.iloc[:, 2] >= date_threshold].values
    with open(TS_PATTERN, "r") as f:
        all_patterns = json.load(f)
    pattern = all_patterns.get(ts, [])
    for x in tqdm(l2, desc=f"Checking Lotto49 TS {ts}"):
        sets = [[x[i - 1] for i in s] for s in pattern]
        sets = np.array([sorted(s) for s in sets])
        for s in tqdm(sets, leave=False):
            for j in l1:
                sum = np.isin(s[:len(s)-1], j[3:9]).sum()
                common = np.intersect1d(s[:len(s)-1], j[3:9])
                if sum >= threshold:
                    tqdm.write(f"Found: {j[0:3]} {np.sort(j[3:9])} {j[9]} == {sum} | {s} -- {common}")


def check_num_all_ts(df, file_pattern, threshold=6, date_threshold=0):
    f = glob.glob(f"{CSV_PATH}/{file_pattern}*.csv")
    for i in f:
        check_num_49_ts(i, df, threshold, date_threshold)


def check_num_all_vs(df, file_pattern, threshold=6, date_threshold=0):
    f = glob.glob(f"{CSV_PATH}/{file_pattern}*.csv")
    for i in f:
        check_num_49_vs(i, df, threshold, date_threshold)


def check_num_all_49(df, fp_ts, fp_vs, threshold=6, date_threshold=0):
    check_num_all_ts(df, fp_ts, threshold, date_threshold)
    check_num_all_vs(df, fp_vs, threshold, date_threshold)


def check_num_euro(used_df, df, threshold=5, date_threshold=0):
    e1 = pd.read_csv(df, sep="\t")
    e2 = pd.read_csv(used_df, sep=",").values
    e1 = e1[e1.iloc[:, 2] >= date_threshold].values
    for i in tqdm(e2, desc="Checking Eurojackpot"):
        for j in e1:
            sum = np.isin(i[0:5], j[3:8]).sum()
            if sum >= threshold and np.isin(i[5:7], j[8:10]).sum() >= 2:
                x = np.sort(j[3:8])
                y = np.sort(j[8:10])
                tqdm.write(f"Found match: {j[0:3]} {x} {y} -- {i[0:5]} {i[5:7]} == {sum} with SuperNums")
            elif sum >= threshold:
                x = np.sort(j[3:8])
                y = np.sort(j[8:10])
                tqdm.write(f"Found match: {j[0:3]} {x} {y} -- {i[0:5]} {i[5:7]} == {sum}")


def check_num_keno(used_df, df, threshold=10, date_threshold=0):
    k1 = pd.read_csv(df, sep="\t").drop(["VA"], axis=1)
    k2 = pd.read_csv(used_df, sep=",").values
    k1 = k1[k1.iloc[:, 2] >= date_threshold].values
    for i in tqdm(k2, desc="Checking Keno"):
        for j in k1:
            s = np.isin(i, j[3::]).sum()
            if s >= threshold:
                x = np.sort(j[3::])
                tqdm.write(f"Found match: {j[0:3]} {x} {i} | {s}")


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
            if (sum > 1 and supernum >=1) or sum >= 3:
                gewinnklassen_output.append(f"{i} -- {winning_set} -- {common} - Gewinnklasse {gewinnklassen_49[(sum, supernum)]}")
    elif type == "euro":
        for i in all_combs:
            common = np.intersect1d(i, winning_set)
            sum = len(common)
            if (sum > 0 and supernum > 1) or (sum >= 2 and supernum >= 1):
                gewinnklassen_output.append(f"{i} - Gewinnklasse {gewinnklassen_euro[(sum, supernum)]}")
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
