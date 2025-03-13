import time
import threading

# Třida pro sledování výpočtu
class ProgressMonitor:

    def __init__(self, matcher):
        self.matcher = matcher
        self.start_time = None
        # Celkový počet úkolů
        self.total_jobs = 0
        # Vlákno ve kterém poběží sledování
        self.thread = None

    def monitor_progress(self, total_jobs):
        # Celkový počtu úkolů a zaznamenání času
        self.total_jobs = total_jobs
        self.start_time = time.time()

        while True:
            # Počet dokončených úkolů
            done_jobs = len(self.matcher.results)
            # Procentuální stav zpracování
            percent_done = (done_jobs / total_jobs) * 100
            # Doba která uplinula od začátku měření
            elapsed_time = time.time() - self.start_time
            estimated_total_time = (elapsed_time / done_jobs) * total_jobs if done_jobs > 0 else 0
            remaining_time = estimated_total_time - elapsed_time

            print(f"\rZpracováno: {percent_done:.2f}% | Zbývající čas: {remaining_time:.2f}s", end="")
            if done_jobs >= total_jobs:
                break
            time.sleep(1)

    def start(self, total_jobs):
        """Spustí monitorovací vlákno."""
        self.thread = threading.Thread(target=self.monitor_progress, args=(total_jobs,))
        self.thread.start()

    def stop(self):
        """Ukončí monitorovací vlákno."""
        if self.thread:
            self.thread.join()
