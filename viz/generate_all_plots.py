import argparse
from data_utils import plot_data
import os

def main():
    parser = argparse.ArgumentParser(description="Visualize all plots in a directory.")
    parser.add_argument("--directory", type=str, required=True,
                        help="Directory containing CSV files to plot (e.g. output/LunarLander/)")
    args = parser.parse_args()

    directory = args.directory
    if not directory.endswith("/"):
        directory += "/"
    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return

    # Only plot types for which files exist
    plot_types = []
    for pt in ["performance", "distance", "query_types"]:
        # check if at least one file for this plot_type exists in directory
        if any(pt in f for f in os.listdir(directory)):
            plot_types.append(pt)

    if not plot_types:
        print(f"No recognized plot types found in {directory}")
        return

    titles = {
        "performance": "Performance",
        "distance": "Distance",
        "query_types": "Query Types"
    }

    for plot_type in plot_types:
        plot_title = f"<b>{titles[plot_type]} - {os.path.basename(os.path.normpath(directory))}</b>"
        args_dict = {
            "directory": directory,
            "plot_type": plot_type,
            "save": False,
            "title": plot_title,
            "show_plot": True
        }
        result = plot_data(args_dict)
        if result is None:
            print(f"No data found for plot type: {plot_type}")
            continue
        fig, auc = result
        out_file = f"{directory}{plot_type}.png"
        fig.write_image(out_file, width=1250, height=850, scale=2)
        print(f"Saved {out_file}")

if __name__ == "__main__":
    main()