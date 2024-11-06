import firebase_admin
from firebase_admin import credentials, db
import psutil
import time

# Inisialisasi Firebase Admin SDK
cred = credentials.Certificate("pc-cpu-monitoring-firebase-adminsdk-2yfd5-cf147c47f5.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pc-cpu-monitoring-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# Referensi ke node 'cpu_usage' di Firebase
ref = db.reference('cpu_usage')

# Fungsi untuk mengirim data CPU usage ke Firebase
def push_cpu_data():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)  # Mengambil CPU usage

        # Disk usage relative to current Drive (D)
        disk_usage = psutil.disk_usage('/')
        disk_metrics = {
            'total_disk_gb': disk_usage.total / (1024**3),  # in GB
            'used_disk_gb': disk_usage.used / (1024**3),    # in GB
            'free_disk_gb': disk_usage.free / (1024**3),    # in GB
            'disk_percent': disk_usage.percent              # percentage used
        }
        
        # Network statistics
        net_io = psutil.net_io_counters()
        network_metrics = {
            'bytes_sent_mb': net_io.bytes_sent / (1024**2),     # in MB
            'bytes_recv_mb': net_io.bytes_recv / (1024**2),     # in MB
            'packets_sent': net_io.packets_sent,                # packet count
            'packets_recv': net_io.packets_recv                 # packet count
        }
            

        data = {
            'cpu': cpu_percent,
            'disk' : disk_metrics,
            'net' : network_metrics,
            'timestamp': time.time()  # Menyimpan timestamp
        }

        ref.push(data)  # Mengirim data ke Firebase

        print(f"Data sent to Firebase: {data}")
        time.sleep(5)  # Mengirim data setiap 5 detik

if __name__ == "__main__":
    push_cpu_data()