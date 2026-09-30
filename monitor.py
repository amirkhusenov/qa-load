import csv
import time
import psutil


with open("metrics.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "timestamp",
        "cpu_percent",
        "memory_percent",
        "disk_read_mb_s",
        "disk_write_mb_s"
    ])

    previous_disk = psutil.disk_io_counters()

    while True:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory().percent

        current_disk = psutil.disk_io_counters()

        read_mb_s = (
            current_disk.read_bytes - previous_disk.read_bytes
        ) / (1024 ** 2)

        write_mb_s = (
            current_disk.write_bytes - previous_disk.write_bytes
        ) / (1024 ** 2)

        previous_disk = current_disk

        writer.writerow([
            timestamp,
            cpu,
            memory,
            read_mb_s,
            write_mb_s
        ])

        file.flush()