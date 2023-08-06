"""Module for accuiring statistical data
"""
import platform
import subprocess
import psutil
from datetime import datetime
import uptime
import random
import time
import csv
import pandas as pd
from pathlib import Path
from typing import Tuple, Union


class Hardware():
    """Class about hardware information.
    """

    def get_model(self) -> str:
        """Gets a model of the hardware

        Note:
            This method is valid for only raspberry pi OS.

        Returns:
            String showing the model.
        """
        try:
            ret = subprocess.check_output(["cat", "/proc/device-tree/model"])
            ret = ret.decode("utf-8")
            return ret
        except subprocess.CalledProcessError:
            return ""

    def get_os(self) -> str:
        """Gets OS

        Returns:
            str: OS
        """
        return platform.system()

    def get_kernel(self) -> str:
        """Gets kernel information.

        Returns:
            str: kernel
        """
        return platform.platform()

    def get_memory(self) -> float:
        """Gets memory size in unit of GB

        Returns:
            float: Memory size
        """
        return round(psutil.virtual_memory().total / 2**30, 1)

    def get_disk(self) -> float:
        """Gets free space under the root direcotory '/' in unit of GB.

        Returns:
            float: Disk space
        """
        return round(psutil.disk_usage("/").total / 2**30, 1)

    def get_boot_time(self) -> str:
        """Gets the time when the system booted.

        Returns:
            str: The time system bboted in the format of %Y-%m-%d %H:%M:%S
        """
        return datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    def get_operating_time(self) -> float:
        """Gets the operating time in unit of hour.

        Returns:
            float: The operating time.
        """
        return round(uptime.uptime() / 60.0 / 60.0, 2)

    def get_hard_info(self) -> dict:
        """Gets the list of the hardware information.

        Returns:
            dict: The hardware information.
        """
        info = {
            "model": self.get_model(),
            "os": self.get_os(),
            "kernel": self.get_kernel(),
            "memory": self.get_memory(),
            "disk": self.get_disk(),
            "boot_time": self.get_boot_time(),
            "operating_time": self.get_operating_time()
        }
        return info


class StatData():

    def __init__(self, debug: bool = False):
        self.root_dir = Path(__file__).resolve().parent / "data/stat_data"
        self.debug = debug

    def get_cpu_temperature(self) -> str:
        """Gets the CPU temperature.

        Returns:
            str: The CPU temperature
        """
        cmd = "vcgencmd measure_temp"
        ret = subprocess.check_output(cmd.split()).decode("utf-8")
        r = ret.split("=")
        return r[1][:4]

    def get_cpu_freq(self) -> str:
        """Gets the CPU frequency of the clock.

        Returns:
            str: The CPU frequency
        """
        cmd = "vcgencmd measure_clock arm"
        ret = subprocess.check_output(cmd.split()).decode("utf-8")
        r = ret.split("=")
        freq = int(r[1][:-1]) / 10**6
        return freq

    def get_core_freq(self) -> str:
        """Gets the VC4 scaler cores frequency of the clock.

        Returns:
            str: The VC4 scaler cores frequency
        """
        cmd = "vcgencmd measure_clock core"
        ret = subprocess.check_output(cmd.split()).decode("utf-8")
        r = ret.split("=")
        freq = int(r[1][:-1]) / 10**6
        return freq

    def get_cpu_memory(self) -> str:
        """Gets the size of the memory currently allocated to the cpu.

        Returns:
            str: The memory size
        """
        cmd = "vcgencmd get_mem arm"
        ret = subprocess.check_output(cmd.split()).decode("utf-8")
        r = ret.split("=")
        return r[1][:-2]

    def get_gpu_memory(self) -> str:
        """Gets the size of the memory currently allocated to the gpu.

        Returns:
            str: The memory size
        """
        cmd = "vcgencmd get_mem gpu"
        ret = subprocess.check_output(cmd.split()).decode("utf-8")
        r = ret.split("=")
        return r[1][:-2]

    def get_cpu_usage(self) -> dict:
        """Gets the current cpu usage.

        Returns:
            dict: The usage of each cpu.
        """
        cpu_usage = {
            "usage_total": psutil.cpu_percent()
            }
        for i, item in enumerate(psutil.cpu_percent(percpu=True)):
            cpu_usage["usage_cpu{}".format(i + 1)] = item
        return cpu_usage

    def get_loadavg(self) -> dict:
        """Gets load average.

        Returns:
            dict: The load averages of 1, 5, 15 minutes.
        """
        loads = psutil.getloadavg()
        keys = ["loadavg_1", "loadavg_5", "loadavg_15"]
        return dict(zip(keys, loads))

    def get_alldata(self) -> dict:
        json_data = {
            "current_time": datetime.now().strftime("%y%m%d-%H:%M:%S"),
            "temperature": self.get_cpu_temperature(),
            "memory_cpu": self.get_cpu_memory(),
            "memory_gpu": self.get_gpu_memory(),
            "frequency_cpu": self.get_cpu_freq(),
            "frequency_core": self.get_core_freq()}
        cpu_usage = self.get_cpu_usage()
        load_avg = self.get_loadavg()

        json_data.update(cpu_usage)
        json_data.update(load_avg)
        return json_data

    def get_dummydata(self) -> dict:
        json_data = {
            "current_time": datetime.now().strftime("%y%m%d-%H:%M:%S"),
            "temperature": random.random() * 70,
            "usage_cpu1": random.random() * 100,
            "usage_cpu2": random.random() * 100,
            "usage_cpu3": random.random() * 100,
            "usage_cpu4": random.random() * 100,
            "memory_cpu": random.random() * 1000,
            "memory_gpu": random.random() * 1000,
            "frequency_cpu": random.random() * 1000,
            "frequency_core": random.random() * 1000,
            "loadavg_1": random.random() * 2,
            "loadavg_5": random.random() * 2,
            "loadavg_15": random.random() * 2,
            }
        return json_data

    def data_with_log(self, dst: Path):
        if self.debug:
            self.func = self.get_dummydata
        else:
            self.func = self.get_alldata
        json_data = self.func()
        values = list(json_data.values())
        values = self.digit_format(values)
        with open(str(dst), "a") as f:
            w = csv.writer(f)
            w.writerow(values)

    def digit_format(self, lst: list) -> list:
        dst = []
        for val in lst:
            try:
                dst.append(f"{val:.2f}")
            except:
                dst.append(val)
        return dst

    def get_csv(self) -> Path:
        data_root = Path(__file__).resolve().parent / "data/stat_data"
        today = datetime.now().strftime("%Y%m")
        data_dir = data_root / today

        data_dir.mkdir(parents=True, exist_ok=True)
        data_file = "{}.csv".format(datetime.now().strftime("%Y%m%d"))
        dst = data_dir / data_file

        if not dst.exists():
            if self.debug:
                json_data = self.get_dummydata()
            else:
                json_data = self.get_alldata()
            header = list(json_data.keys())
            with open(str(dst), "w") as f:
                w = csv.writer(f)
                w.writerow(header)
        return dst

    def check_input_params(self, data: dict, graph: str) -> Tuple[bool, str]:
        value = []
        for i in data.values():
            value.append(i)
        try:
            min_ = int(value[0])
            max_ = int(value[1])
            step = float(value[2])
            duration = int(value[3])
        except (ValueError, TypeError):
            return False, "There are empty or invalid fields."

        for i in min_, max_, step:
            if not self.check_yaxes(i, graph):
                return False, "Input values are invalid."

        if not self.check_duration(duration):
            return False, "Input values are invalid."

        return True, "ok"

    def check_yaxes(self, value: Union[int, float], graph: str) -> bool:
        if graph == "temperature":
            if 0 <= value < 1000:
                return True
            else:
                return False
        elif graph == "usage":
            if 0 <= value < 1000:
                return True
            else:
                return False
        elif graph == "memory":
            if 0 <= value < 10000:
                return True
            else:
                return False
        elif graph == "frequency":
            if 0 <= value < 10000:
                return True
            else:
                return False
        elif graph == "loadavg":
            if 0 <= value < 100:
                return True
            else:
                return False
        else:
            if 0 <= value < 10:
                return True
            else:
                return False

    def check_duration(self, value: int) -> bool:
        if 1000 <= value <= 600000:
            return True
        else:
            return False

    def exist_logs(self) -> list:
        lst = []
        for f in self.root_dir.glob("**/*"):
            if f.is_file():
                filename = f.stem
                lst.append(str(filename))
        return lst

    def get_date(self, path: str, ret_date: bool = False) -> str:
        """Converts string showing the specified date into abs path if exists.

        The path should be in the format of yyyymmdd.

        Args:
            path (str): [description]

        Returns:
            str: [description]
        """
        if "/" in path:
            month = path[0:2]
            day = path[3:5]
            year = path[6:]
            path = f"{year}{month}{day}"
            if ret_date:
                return year, month, day
        date = self.root_dir / path[:-2]
        if date.exists():
            date2 = date / f"{path}.csv"
            if date2.exists():
                return date2.resolve()
        return None

    def read_log(self, path: str, rate: str) -> dict:
        df = pd.read_csv(path)
        t = pd.to_datetime(df.iloc[:, 0], format="%y%m%d-%H:%M:%S")
        df = df.set_index(t)
        df.drop("current_time", axis=1, inplace=True)
        # Resamples data by the specified rate.
        df = df.resample(rate).mean()
        dct = {}
        # add timestamp
        dct[df.index.name] = [str(i) for i in df.index]
        # add the rest data
        for i, col in enumerate(df):
            dct[col] = list(df.iloc[:, i])
        return dct

    def get_sampling_rate(self, num: str, unit: str) -> str:
        """Parses the string for data resampling.

        The input string showing the time rate is parsed to get the string specified
        with the resample method in pandas. The parsed string is splited into num
        and str, showing the time and unit respectively. Finally,

        Args:
            rate (str): [description]

        Returns:
            str: [description]

        Examples:
            >> parser_sample_rate("1hour")
            >> "1h"
        """
        ret = str(num)
        if unit == "min":
            ret += "min"
        elif unit == "hour":
            ret += "h"
        elif unit == "second":
            ret += "s"
        return ret

    def time_validate(self, start: str, end: str) -> bool:
        """Check if the input string is valid.

        Returns true if the time is HH::MM, otherwise false.

        Args:
            t (str): [description]

        Returns:
            bool: [description]
        """
        t_list = [start, end]
        for t in t_list:
            tmp_list = t.split(":")
            if len(tmp_list) != 2:
                return False
            try:
                hour = int(tmp_list[0])
                minute = int(tmp_list[1])
                if 0 <= hour <= 24 and 0 <= minute < 60:
                    pass
                else:
                    return False
            except (ValueError, IndexError):
                return False
        return True

    def time_relation(self, t1: str, t2: str) -> bool:
        t1_h, t1_m = t1.split(":")
        t2_h, t2_m = t2.split(":")
        date1 = datetime(2021, 1, 1, int(t1_h), int(t1_m))
        date2 = datetime(2021, 1, 1, int(t2_h), int(t2_m))
        if date1 < date2:
            return True
        else:
            return False


def routine(debug: bool = False):
    s = StatData(debug)
    while True:
        dst = s.get_csv()
        s.data_with_log(dst)
        time.sleep(1)
