from salt import get_student_params
import platform
import sys
import json
import os
import subprocess
import psutil
import cpuinfo
import argparse


def get_windows_cache_info():
    cache_info = {
        "L1_data_KB": None,
        "L2_KB": None,
        "L3_shared_KB": None,
        "cache_line_bytes": 64
    }

    try:
        command = (
            "Get-CimInstance Win32_CacheMemory | "
            "Select-Object Level, InstalledSize, CacheType | "
            "ConvertTo-Json -Compress"
        )

        result = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", command],
            text=True
        )

        data = json.loads(result)

        if isinstance(data, dict):
            data = [data]

        l1_data = []
        l2 = []
        l3 = []

        for item in data:
            level = item.get("Level")
            size = item.get("InstalledSize")
            cache_type = item.get("CacheType")

            if size is None:
                continue

            if level == 3 and cache_type == 4:
                l1_data.append(size)

            elif level == 4:
                l2.append(size)

            elif level == 5:
                l3.append(size)

        if l1_data:
            cache_info["L1_data_KB"] = sum(l1_data)

        if l2:
            cache_info["L2_KB"] = sum(l2)

        if l3:
            cache_info["L3_shared_KB"] = max(l3)

    except Exception as error:
        print("Could not detect cache information:", error)

    return cache_info


def get_cpu_microarchitecture(cpu_name):
    name = cpu_name.lower()

    if "i7-12650h" in name:
        return "Alder Lake"

    if "12th gen" in name:
        return "Alder Lake"

    return "Unknown"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--student-id", required=True)
    args = parser.parse_args()

    cpu_info = cpuinfo.get_cpu_info()

    cpu_name = cpu_info.get("brand_raw", platform.processor())

    physical_cores = psutil.cpu_count(logical=False)
    logical_cores = psutil.cpu_count(logical=True)

    base_frequency_mhz = None

    try:
        command = (
            "Get-CimInstance Win32_Processor | "
            "Select-Object -First 1 -ExpandProperty MaxClockSpeed"
        )

        result = subprocess.check_output(
            ["powershell", "-NoProfile", "-Command", command],
            text=True
        )

        base_frequency_mhz = int(result.strip())

    except Exception:
        pass

    cache_info = get_windows_cache_info()

    profile = {
        "cpu_model": cpu_name,
        "microarchitecture": get_cpu_microarchitecture(cpu_name),
        "base_frequency_MHz": base_frequency_mhz,
        "physical_cores": physical_cores,
        "logical_threads": logical_cores,
        "SMT_enabled": logical_cores > physical_cores,
        "cache": cache_info,
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "kernel_version": platform.release(),
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "python_architecture": platform.architecture()[0]
    }

    os.makedirs("results", exist_ok=True)

    with open("results/host_profile.json", "w") as file:
        json.dump(profile, file, indent=4)

    salted_params = get_student_params(args.student_id)

    with open("results/salted_params.json", "w") as file:
        json.dump(salted_params, file, indent=4)
    print("Host profile saved successfully!")
    print(json.dumps(profile, indent=4))


if __name__ == "__main__":
    main()