import time
from image_matcher import ImageMatcher
from progress_monitor import ProgressMonitor

# Řízení hlavní aplikace
class MainApp:

    def __init__(self, input_image, template_image, output_file):
        # ImageMatcher se stará o načtení a zpracování obrázků
        self.matcher = ImageMatcher(input_image, template_image, output_file)
        # ProgressMonitor sleduje průběh vyhledávání
        self.progress_monitor = ProgressMonitor(self.matcher)

    # Spustí aplikaci
    def run(self):
        print("Načítám obrázky...")
        # Načte vstupní a vzorový obrázek
        self.matcher.load_images()

        # Zjistí rozměry hlavního obrázku (obr) a vzoru (vzr)
        h_obr, w_obr = self.matcher.obr.shape
        h_vzr, w_vzr = self.matcher.vzr.shape
        total_jobs = w_obr - w_vzr + 1

        print("Spouštím paralelní hledání...")
        # Zobrazí počet úkolů, které bude zpracovávat
        self.progress_monitor.start(total_jobs)
        # Uložení aktuálního času pro pozdější výpočet doby zpracování
        start_time = time.time()

        # Paralelní vyhledávání vzoru v obrázku
        self.matcher.run_parallel_search()

        # Po dokončení vyhledávání zastaví průběh sledování
        self.progress_monitor.stop()

        # Zjištění času po ukončení vyhledávání a spočíta celkovou dobu
        end_time = time.time()
        processing_time = end_time - start_time

        print("\nVýpočet dokončen. Ukládám výsledky...")
        self.matcher.save_results(processing_time)

        print(f"Hotovo! Výsledky uloženy do {self.matcher.output_file}")


if __name__ == "__main__":
    # Zde zadáš obrázky a výstupní soubor
    INPUT_IMAGE = "obrazek.png"
    TEMPLATE_IMAGE = "vzor.png"
    OUTPUT_FILE = "vysledek.txt"

    app = MainApp(INPUT_IMAGE, TEMPLATE_IMAGE, OUTPUT_FILE)
    app.run()
