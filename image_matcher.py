import cv2
import numpy as np
import multiprocessing as mp


class ImageMatcher:

    def __init__(self, input_image, template_image, output_file):
        self.input_image = input_image
        self.template_image = template_image
        self.output_file = output_file

        self.obr = None
        self.vzr = None
        # Seznam pro ukládání výsledků
        self.results = []

    def load_images(self):
        # Načte oba černobíle obrázky
        self.obr = cv2.imread(self.input_image, cv2.IMREAD_GRAYSCALE)
        self.vzr = cv2.imread(self.template_image, cv2.IMREAD_GRAYSCALE)

        # Kontrola načtení obrázku
        if self.obr is None or self.vzr is None:
            raise FileNotFoundError("Chyba při načítání obrázků.")

    def compute_metric(self, start_x, end_x, queue):
        # Ziskání rozměru obrázků
        h_obr, w_obr = self.obr.shape
        h_vzr, w_vzr = self.vzr.shape

        # Sdílené výsledky
        local_results = []

        # Procházení sloupců a řádků tak, aby se vzor vešel do obrázku
        for x in range(start_x, end_x):
            for y in range(h_obr - h_vzr + 1):
                patch = self.obr[y:y + h_vzr, x:x + w_vzr]
                metric = np.sum((patch - self.vzr) ** 2) / (h_vzr * w_vzr)
                local_results.append((metric, x, y))

        queue.put(local_results)

    def run_parallel_search(self):
        # Zjistí počet dostupných CPU jader, které se použijí pro paralelní zpracování
        num_processes = mp.cpu_count()
        # Vytvoření fronty, do které se budou posílat výsledky
        queue = mp.Queue()
        # Seznam do kterého se ukládají vytvořené procesy
        processes = []

        # Získaní rozměru obrazků
        h_obr, w_obr = self.obr.shape
        h_vzr, w_vzr = self.vzr.shape

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
            self.results.extend(queue.get())

        for p in processes:
            p.join()

    # Setřízení a zápis výsledku do souboru (Top 10)
    def save_results(self, processing_time):
        self.results.sort()
        best_results = self.results[:10]

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(f"Doba zpracování: {processing_time:.2f} sekund\n")
            f.write("Top 10 shod (hodnota metriky, x, y):\n")
            for metric, x, y in best_results:
                f.write(f"{metric:.4f}, {x}, {y}\n")
