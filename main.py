import time
from image_matcher import ImageMatcher
from progress_monitor import ProgressMonitor


class MainApp:
    """Třída pro řízení hlavního běhu aplikace."""

    def __init__(self, input_image, template_image, output_file):
        self.matcher = ImageMatcher(input_image, template_image, output_file)
        self.progress_monitor = ProgressMonitor(self.matcher)

    def run(self):
        """Spustí celou aplikaci."""
        print("▶ Načítám obrázky...")
        self.matcher.load_images()

        h_obr, w_obr = self.matcher.obr.shape
        h_vzr, w_vzr = self.matcher.vzr.shape
        total_jobs = w_obr - w_vzr + 1

        print("▶ Spouštím paralelní hledání...")
        self.progress_monitor.start(total_jobs)
        start_time = time.time()

        self.matcher.run_parallel_search()

        self.progress_monitor.stop()

        end_time = time.time()
        processing_time = end_time - start_time

        print("\n✅ Výpočet dokončen. Ukládám výsledky...")
        self.matcher.save_results(processing_time)

        print(f"✅ Hotovo! Výsledky uloženy do {self.matcher.output_file}")


if __name__ == "__main__":
    # Zde zadáš obrázky a výstupní soubor
    INPUT_IMAGE = "obrazek.png"
    TEMPLATE_IMAGE = "vzor.png"
    OUTPUT_FILE = "vysledek.txt"

    app = MainApp(INPUT_IMAGE, TEMPLATE_IMAGE, OUTPUT_FILE)
    app.run()
