import cv2
import numpy as np
import multiprocessing as mp
from typing import List, Tuple


class ImageMatcher:

    def __init__(self, input_image: str, template_image: str, output_file: str):
        self.__input_image: str = input_image
        self.__template_image: str = template_image
        self.__output_file: str = output_file
        self.__obr: np.ndarray | None = None
        self.__vzr: np.ndarray | None = None
        self.__results: List[Tuple[float, int, int]] = []
        self.__total_jobs: int = 0  # Počet posunů vzoru přes obraz

    def load_images(self):
        # Načte oba černobíle obrázky
        self.__obr = cv2.imread(self.__input_image, cv2.IMREAD_GRAYSCALE)
        self.__vzr = cv2.imread(self.__template_image, cv2.IMREAD_GRAYSCALE)

        # Kontrola načtení obrázku
        if self.__obr is None or self.__vzr is None:
            raise FileNotFoundError("Chyba při načítání obrázků.")

         # Počet možných pozic vzoru na hlavním obrázku
        h_obr, w_obr = self.__obr.shape
        h_vzr, w_vzr = self.__vzr.shape
        self.__total_jobs = (h_obr - h_vzr + 1) * (w_obr - w_vzr + 1)

    def compute_metric(self, start_x, end_x, queue):
        # Kontrola zda jsou obrazky načtené
        assert self.__obr is not None and self.__vzr is not None
        # Ziskání rozměru obrázků
        h_obr, w_obr = self.__obr.shape
        h_vzr, w_vzr = self.__vzr.shape
        local_results: List[Tuple[float, int, int]] = []

        # Procházení sloupců a řádků tak, aby se vzor vešel do obrázku
        for x in range(start_x, end_x):
            for y in range(h_obr - h_vzr + 1):
                patch = self.__obr[y:y + h_vzr, x:x + w_vzr]
                metric = np.sum((patch - self.__vzr) ** 2) / (h_vzr * w_vzr)
                local_results.append((metric, x, y))

        queue.put(local_results)

    def run_parallel_search(self):
        # Zjistí počet dostupných CPU jader, které se použijí pro paralelní zpracování
        num_processes: int = mp.cpu_count()
        # Vytvoření fronty, do které se budou posílat výsledky
        queue: mp.Queue = mp.Queue()
        # Seznam do kterého se ukládají vytvořené procesy
        processes: List[mp.Process] = []

        # Získaní rozměru obrazků
        h_obr, w_obr = self.__obr.shape
        h_vzr, w_vzr = self.__vzr.shape

        # Určuje šířku segmentu pro jeden proces
        step = (w_obr - w_vzr + 1) // num_processes
        ranges = [(i * step, (i + 1) * step if i != num_processes - 1 else (w_obr - w_vzr + 1)) for i in
                  range(num_processes)]

        # Pro každé rozmezí vytvoříme proces, který volá compute_metric
        for start_x, end_x in ranges:
            p = mp.Process(target=self.compute_metric, args=(start_x, end_x, queue))
            p.start()
            processes.append(p)

        for _ in processes:
            self.__results.extend(queue.get())

        for p in processes:
            p.join()

    # Setřízení a zápis výsledku do souboru (Top 10)
    def save_results(self, processing_time):
        self.__results.sort()
        best_results = self.__results[:10]

        with open(self.__output_file, "w", encoding="utf-8") as f:
            f.write(f"Doba zpracování: {processing_time:.2f} sekund\n")
            f.write("Top 10 shod (hodnota metriky, x, y):\n")
            for metric, x, y in best_results:
                f.write(f"{metric:.4f}, {x}, {y}\n")

    def get_total_jobs(self) -> int:
        # Vrací celkový počet úloh
        return self.__total_jobs

    def get_results(self) -> List[Tuple[float, int, int]]:
        # Vrátí aktuální výsledky
        return self.__results