"""
CS5001
Final Project - Main Program
Spring 2026
21 Apr 26
Adele Ka
"""
from data_loader import DataLoader
from analysis import Analysis
from text_report import print_report
from chart import make_charts
from folium_map import build_map


def main():
    """Runs the full project: loads data, prints report, creates charts, and builds the interactice html map.
    
    Returns: None
        
    """
    try:
        print("Loading park and crime data...")
        loader = DataLoader()
        parks = loader.load_parks()
        crimes = loader.load_crimes()

        print("Saving parsed CSV files...")
        loader.save_parse_data(parks, crimes)

        print("Running analysis...")
        analysis = Analysis(parks, crimes)
        report = analysis.full_report()

        print("Generating text report...")
        print_report(report)

        print("Generating charts...")
        make_charts(parks, crimes, analysis)

        print("Generating folium map...")
        build_map(parks, crimes)

        print("Done.")
        print("Created files:")
        print("- parks_parsed.csv")
        print("- crimes_parsed.csv")
        print("- charts/parks_by_neighbourhood.png")
        print("- charts/crime_types.png")
        print("- charts/parks_vs_crimes.png")
        print("- charts/crimes_near_parks.png")
        print("- folium_map.html")

    except Exception as e:
        print(f"Program error: {e}")


if __name__ == "__main__":
    main()
