# 📌 Paralelní hledání vzoru v obraze

Tento projekt implementuje paralelní algoritmus pro vyhledání vzoru v černobílém obraze.  
Využívá **multiprocessing** pro efektivní výpočet a **threading** pro sledování průběhu.

---

## 🚀 Jak projekt funguje?

1. **Načte se hlavní obrázek (`obrazek.png`) a vzor (`vzor.png`).**
2. **Provede se prohledávání pomocí konvoluce** (metrika = součet druhých mocnin rozdílů).
3. **Paralelizace** – využívá se více procesů pro urychlení výpočtu.
4. **Sledování průběhu výpočtu** – běží ve vedlejším vlákně.
5. **Uložení výsledků do souboru UTF-8 (`vysledek.txt`).**