"""
CS5001
Final Project - Text Report Class
Spring 2026
21 Apr 26
Adele Ka
"""
from data_loader import DataLoader
from analysis import Analysis


def print_report(report):
    """ Prints the final report. This method takes the report dictionary and prints each section in a clean and simple format.
        Args: report (dict): The full report dictionary from the Analysis class.
    """
    summary = report["summary_of_data_set"]
    insights = report["meaningful_insights"]
    cross_summary = report["cross_data_set_summary"]

    print("\n============================================================")
    print("VANCOUVER PARKS AND CRIMES REPORT")
    print("Reporting Period: 05 - 12 Apr 2026 ")
    print("By Adele Ka")

    print("\n============================================================")
    print("1. SUMMARY OF DATA SET")
    print("============================================================")
    print(f"Total parks: {summary['parks_count']}")
    print(f"Total crimes: {summary['crimes_count']}")
    
    print("\n============================================================")
    print("2. MEANINGFUL INSIGHTS")
    print("============================================================")
    park_neighbourhood, park_count = insights["neighbourhood_with_most_parks"]
    crime_neighbourhood, crime_count = insights["neighbourhood_with_most_crime"]
    common_crime, common_crime_count = insights["most_common_crime_type"]

    print(f"Neighbourhood with the most parks: {park_neighbourhood} ({park_count})")
    print(f"Neighbourhood with the most crime: {crime_neighbourhood} ({crime_count})")
    print(f"Most common crime type: {common_crime} ({common_crime_count})")

    print("\nCrime type counts:")
    crime_type_counts = insights["crime_type_counts"]
    for crime_type, count in sorted(crime_type_counts.items(), key=lambda item: item[1], reverse=True):
        print(f"- {crime_type}: {count}")
    
    print("\n============================================================")
    print("3. CROSS DATA-SET SUMMARY")
    print("============================================================")
    correlation = cross_summary["park_crime_correlation"]
    print(f"Correlation between park count and crime count by neighbourhood: {correlation:.4f}")

    print("\nCrime proximity to parks:")
    proximity = cross_summary["crime_proximity_to_parks"]
    for radius, count in proximity.items():
        print(f"- Crimes within {radius} m of a park: {count}")
    print("\n")


def main():
    """Runs the report program. This method loads the data, runs the analysis, and prints the report."""
    try:
        loader = DataLoader()
        parks = loader.load_parks()
        crimes = loader.load_crimes()

        analysis = Analysis(parks, crimes)
        report = analysis.full_report()
        print_report(report)
    
    except Exception as e:
        print(f"Program error: {e}")

if __name__ == "__main__":
    main()