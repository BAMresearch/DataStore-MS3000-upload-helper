"""
attachs.py – Erzeugt die Ergebnisdateien:
- results.txt (semicolon-separated)
- freq.png (Verteilung q3)
- sum.png  (kumulative Verteilung Q3)
- preview.png (Doppelachse)
"""
import matplotlib.pyplot as plt


def make_outputs(parsed: dict):
    """Erstellt results.txt & drei PNGs. Gibt die Dateipfade zurück."""
    base = parsed["file_path"]
    results_file = base.replace('.txt', '_results.txt')
    freq_file = base.replace('.txt', '_freq.png')
    sum_file = base.replace('.txt', '_sum.png')
    preview_file = base.replace('.txt', '_preview.png')

    # results.txt
    with open(results_file, "w", encoding="utf-8") as f:
        f.write("particle size/µm;frequency/%;particle size/µm;undersize/%\n")
        for a, b, c, d in zip(parsed["particle_size"], parsed["frequency"],
                              parsed["particle_size_undersize"], parsed["undersize"]):
            f.write(f"{a};{b};{c};{d}\n")

    # freq.png
    plt.figure()
    plt.plot(parsed["particle_size"], parsed["frequency"], linewidth=1)
    plt.title(parsed["dia_title"])
    plt.xscale('log')
    plt.xlabel('particle size / µm')
    plt.ylabel(r'volume density distribution $q_{3}(x)$ / %')
    plt.savefig(freq_file, bbox_inches="tight")
    plt.close()

    # sum.png
    plt.figure()
    plt.plot(parsed["particle_size_undersize"], parsed["undersize"], linewidth=1, color='red')
    plt.title(parsed["dia_title"])
    plt.xscale('log')
    plt.xlabel('particle size / µm')
    plt.ylabel(r'cumulative volume distribution $Q_{3}(x)$ / %')
    plt.savefig(sum_file, bbox_inches="tight")
    plt.close()

    # preview.png (Doppelachse)
    fig, ax1 = plt.subplots()
    ax1.set_xscale('log')
    ax1.set_xlabel('particle size / µm')
    ax1.set_ylabel(r'volume density distribution $q_{3}(x)$ / %', color='tab:blue')
    ax1.plot(parsed["particle_size"], parsed["frequency"], color='tab:blue', label='frequency')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel(r'cumulative volume distribution $Q_{3}(x)$ / %', color='tab:red')
    ax2.plot(parsed["particle_size_undersize"], parsed["undersize"], color='tab:red', label='undersize')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    plt.title(parsed["dia_title"])
    plt.savefig(preview_file, bbox_inches="tight")
    plt.close()

    return results_file, freq_file, sum_file, preview_file
