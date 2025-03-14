import time
import threading
from image_matcher import ImageMatcher

# Třida pro sledování výpočtu
class ProgressMonitor:

    def __init__(self, matcher: ImageMatcher):
        self.__matcher = matcher
        self.__start_time: float = 0
        self.__total_jobs: int = 0
        self.__thread: threading.Thread | None = None

    def monitor_progress(self) -> None:
        # Celkový počtu úkolů a zaznamenání zbývajícího času
        self.__start_time = time.time()
        self.__total_jobs = self.__matcher.get_total_jobs()

        while True:
            # Počet dokončených úkolů
            done_jobs = len(self.__matcher.get_results())
            # Procentuální stav zpracování
            percent_done = (done_jobs / self.__total_jobs) * 100
            # Doba která uplinula od začátku měření
            elapsed_time = time.time() - self.__start_time
            estimated_total_time = (elapsed_time / done_jobs) * self.__total_jobs if done_jobs > 0 else 0
            remaining_time = estimated_total_time - elapsed_time

            print(f"\rZpracováno: {min(percent_done, 100):.2f}% | Zbývající čas: {max(remaining_time, 0):.2f}s", end="")

            if done_jobs >= self.__total_jobs:
                break

            time.sleep(1)

    def start(self) -> None:
        # Spustí monitorovací vlákno
        self.__thread = threading.Thread(target=self.monitor_progress)
        self.__thread.start()

    def stop(self) -> None:
        # Ukončí monitorovací vlákno
        if self.__thread:
            self.__thread.join()
