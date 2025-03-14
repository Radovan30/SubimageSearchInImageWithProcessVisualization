import time
from image_matcher import ImageMatcher
from progress_monitor import ProgressMonitor

# Definované vstupní a výstupní soubory
INPUT_IMAGE = "obrazek.png"
TEMPLATE_IMAGE = "vzor.png"
OUTPUT_FILE = "vysledek.txt"

if __name__ == "__main__":

    matcher = ImageMatcher(INPUT_IMAGE, TEMPLATE_IMAGE, OUTPUT_FILE)
    progress_monitor = ProgressMonitor(matcher)

    print("Načítám obrázky...")
    matcher.load_images()

    print("Spouštím paralelní hledání...")
    progress_monitor.start()
    start_time = time.time()

    matcher.run_parallel_search()

    progress_monitor.stop()

    processing_time = time.time() - start_time
    matcher.save_results(processing_time)

    print(f"\nVýpočet dokončen! Výsledky uloženy do {OUTPUT_FILE}")
