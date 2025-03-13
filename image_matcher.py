import cv2
import numpy as np
import multiprocessing as mp


class ImageMatcher:
    """Třída pro hledání vzoru v obrázku pomocí paralelního zpracování."""

    def __init__(self, input_image, template_image, output_file):
        self.input_image = input_image
        self.template_image = template_image
        self.output_file = output_file
        self.obr = None
        self.vzr = None
        self.results = []

    def load_images(self):
        """Načtení černobílých obrázků."""
        self.obr = cv2.imread(self.input_image, cv2.IMREAD_GRAYSCALE)
        self.vzr = cv2.imread(self.template_image, cv2.IMREAD_GRAYSCALE)

        if self.obr is None or self.vzr is None:
            raise FileNotFoundError("Chyba při načítání obrázků.")

    def compute_metric(self, start_x, end_x, queue):
        """Výpočet metriky pro část obrazu ve vymezeném rozsahu."""
        h_obr, w_obr = self.obr.shape
        h_vzr, w_vzr = self.vzr.shape
        local_results = []

        for x in range(start_x, end_x):
            for y in range(h_obr - h_vzr + 1):
                patch = self.obr[y:y + h_vzr, x:x + w_vzr]
                metric = np.sum((patch - self.vzr) ** 2) / (h_vzr * w_vzr)
                local_results.append((metric, x, y))

        queue.put(local_results)

    def run_parallel_search(self):
        """Spuštění paralelního hledání vzoru."""
        num_processes = mp.cpu_count()
        queue = mp.Queue()
        processes = []
        h_obr, w_obr = self.obr.shape
        h_vzr, w_vzr = self.vzr.shape

        step = (w_obr - w_vzr + 1) // num_processes
        ranges = [(i * step, (i + 1) * step if i != num_processes - 1 else (w_obr - w_vzr + 1)) for i in
                  range(num_processes)]

        for start_x, end_x in ranges:
            p = mp.Process(target=self.compute_metric, args=(start_x, end_x, queue))
            p.start()
            processes.append(p)

        for _ in processes:
            self.results.extend(queue.get())

        for p in processes:
            p.join()

    def save_results(self, processing_time):
        """Uloží výsledky do souboru."""
        self.results.sort()
        best_results = self.results[:10]

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(f"Doba zpracování: {processing_time:.2f} sekund\n")
            f.write("Top 10 shod (hodnota metriky, x, y):\n")
            for metric, x, y in best_results:
                f.write(f"{metric:.4f}, {x}, {y}\n")
