import matplotlib.pyplot as plt

try:
    # Works when run from project root with src on PYTHONPATH.
    from datapreprocessor.visualize.flaw_report_plot import plot_flaw_counts
except ModuleNotFoundError:
    # Fallback for direct execution from this folder.
    from flaw_report_plot import plot_flaw_counts


def main():
    fig, ax = plot_flaw_counts("flaw_report.txt")
    plt.show()


if __name__ == "__main__":
    main()
