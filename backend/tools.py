import os
import zipfile
import shutil
import pyarrow as pa
import pyarrow.ipc as ipc
import glob
import requests

from dotenv import load_dotenv
from fastapi.responses import Response
from io import BytesIO
from bs4 import BeautifulSoup
from urllib.parse import urljoin


EXTRACT_FILES = [
    "eurojackpot.txt",
    "keno.txt",
    "lotto_6aus49_ab_02.12.2000.txt",
    "gs.txt",
    "spiel77.txt",
    "super6.txt",
    "plus5.txt"
]


def safe_urljoin(base: str, url: object) -> str | None:
    if isinstance(url, str):
        return urljoin(base, url)
    return None


def get_download_folder():
    # cross-platform Downloads folder (macOS, Linux, Windows)
    download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.isdir(download_folder):
        # fallback to home dir then current working dir
        download_folder = os.path.expanduser("~")
        if not os.path.isdir(download_folder):
            download_folder = os.getcwd()
    return str(download_folder)


def download_archives(url_list: list):
    file_types = (".zip",)
    for URL in url_list:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for a_tag in soup.find_all("a", href=True):
            full_url = safe_urljoin(URL, a_tag["href"])
            links.append(full_url)
        for link in links:
            if link.lower().endswith(file_types):
                download_file(link)


def download_file(url):
    download_folder = get_download_folder()
    filename = os.path.join(download_folder, url.split("/")[-1])

    print(f"Downloading: {url}")
    r = requests.get(url, stream=True)

    if r.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        print(f"Saved to {filename}")
    else:
        print(f"Failed: {url}")


def get_lotto(destination):
    download_folder = get_download_folder()
    files = [
        "archiv_keno.zip",
        "archiv_eurojackpot.zip",
        "archiv_lotto.zip",
        "archiv_s77.zip",
        "archiv_s6.zip",
        "archiv_gs.zip",
        "archiv_p5.zip"
    ]
    for file in files:
        file_path = os.path.join(download_folder, file)
        if os.path.exists(file_path):
            print(f"Found {file} in {download_folder}")
        else:
            print(f"{file} not found in {download_folder}")
    for file in files:
        file_path = os.path.join(download_folder, file)
        if os.path.exists(file_path):
            dest_path = os.path.join(destination, file)
            if os.path.exists(dest_path):
                os.remove(dest_path)
            shutil.copy2(file_path, dest_path)
            os.remove(file_path)
    for file in files:
        dest_path = os.path.join(destination, file)
        if os.path.exists(dest_path):
            with zipfile.ZipFile(dest_path, 'r') as zip_ref:
                for member in zip_ref.namelist():
                    if member in EXTRACT_FILES:
                        zip_ref.extract(member, destination)
            os.remove(dest_path)


def lotto_arrow(setlist, supernum):
    num_columns = len(setlist[0])
    table_dict = {f"num{i+1}": [r[i] for r in setlist] for i in range(num_columns)}
    if len(supernum) == 1:
        table_dict["supernum"] = [supernum] * len(setlist)
    else:
        table_dict["supernum"] = [[x] for x in supernum]
    table = pa.Table.from_pydict(table_dict)
    
    buf = pa.BufferOutputStream()
    writer = ipc.RecordBatchStreamWriter(buf, table.schema)
    writer.write_table(table)
    writer.close()
    arrow_bytes = buf.getvalue().to_pybytes()
    return arrow_bytes


def eurojackpot_arrow(setlist, supernum):
    num_columns = len(setlist[0])
    table_dict = {f"num{i+1}": [r[i] for r in setlist] for i in range(num_columns)}
    super_width = len(supernum[0]) if supernum else 0

    for i in range(super_width):
        table_dict[f"supernum{i+1}"] = [
            s[i] if i < len(s) else None
            for s in supernum
        ]
    table = pa.Table.from_pydict(table_dict)

    buf = pa.BufferOutputStream()
    writer = ipc.RecordBatchStreamWriter(buf, table.schema)
    writer.write_table(table)
    writer.close()
    arrow_bytes = buf.getvalue().to_pybytes()
    return arrow_bytes


def merge_rows_inplace(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        filtered_lines = [line for line in lines if not 
                          (line.strip().startswith('Tipp') or 
                            line.strip().startswith('5 aus 50') or 
                            line.strip().startswith('2 aus 12') or
                            line.strip().startswith('Vollsystem') or
                            line.strip().startswith('Teilsystem'))]
    with open(file, 'w') as f:
        f.writelines(line.replace(' ', ',') for line in filtered_lines)

    with open(file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    merged_lines = []
    buffer = []

    for line in lines:
        numbers = line.split(",")
        buffer.extend(numbers)

        if len(buffer) >= 6:
            merged_lines.append(",".join(buffer))
            buffer = []

    if buffer:
        merged_lines.append(",".join(buffer))
    with open(file, "w", encoding="utf-8") as f:
        for line in merged_lines:
            f.write(line + "\n")


def format_CSVs(dir):
    files = glob.glob(f"{dir}/*",)
    for file in files:
        merge_rows_inplace(file)


def is_in(set, subset):
    return all(x in set.tolist() for x in subset)


if __name__ == "__main__":
    load_dotenv()
    download_archives([os.getenv("LOTTO_49_URL"), os.getenv("EUROJACKPOT_URL"), os.getenv("KENO_URL"), os.getenv("GS_S77_S6_URL")])
    get_lotto(os.getenv("TSV_PATH"))
    format_CSVs(os.getenv("CSV_PATH"))
