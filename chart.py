"""
CS5001
Final Project - Chart Generation
Spring 2026
21 Apr 26
Adele Ka
"""
from pathlib import Path
import matplotlib.pyplot as plt
from analysis import Analysis
from data_loader import DataLoader

PASTEL_100 = '#f9c5d1'
PASTEL_200 = '#f7d794'
PASTEL_500 = '#c7ceea'
CHARTS_DIR = Path('charts')

def sorted_counts(counts_dict):
    """Sorts a dictionary of counts from highest to lowest.

    Args:
        counts_dict (dict): A dictionary where the keys are category names
        and the values are numeric counts.

    Returns:
        list: A list of key-value tuples sorted in descending order by count.
    """
    return sorted(counts_dict.items(), key=lambda item: item[1], reverse=True)

def make_charts(parks, crimes, analysis):
    """Creates and saves PNG charts for the parks and crimes project.

    This function generates bar charts, a scatter plot, and a proximity chart using the analysis results. The output image files are saved in the charts
    folder.

    Args:
        parks (list): A list of Park objects.
        crimes (list): A list of Crime objects.
        analysis (Analysis): An Analysis object containing summary methods
        used to prepare chart data.

    Returns:
        None
    """
    CHARTS_DIR.mkdir(exist_ok=True)

    park_counts = sorted_counts(analysis.parks_by_neighbourhood())
    plt.figure(figsize=(12, 6))
    plt.bar([item[0] for item in park_counts], [item[1] for item in park_counts], color='#9b5de5', edgecolor='black')
    plt.title('Number of Parks by Neighbourhood')
    plt.xlabel('Neighbourhood')
    plt.ylabel('Number of Parks')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'parks_by_neighbourhood.png', dpi=200)
    plt.close()

    crime_counts = sorted_counts(analysis.crime_type_counts())
    plt.figure(figsize=(10, 6))
    plt.bar([item[0] for item in crime_counts], [item[1] for item in crime_counts], color='#5dade2', edgecolor='black')
    plt.title('Crime Counts by Crime Type')
    plt.xlabel('Crime Type')
    plt.ylabel('Number of Crimes')
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'crime_types.png', dpi=200)
    plt.close()

    park_by_neighbourhood = analysis.parks_by_neighbourhood()
    crime_by_neighbourhood = analysis.crimes_by_neighbourhood()
    neighbourhoods = sorted(set(park_by_neighbourhood) | set(crime_by_neighbourhood))
    x_values = [park_by_neighbourhood.get(name, 0) for name in neighbourhoods]
    y_values = [crime_by_neighbourhood.get(name, 0) for name in neighbourhoods]
    plt.figure(figsize=(9, 7))
    plt.scatter(x_values, y_values, color='#ff7f7f', s=70)
    for name, x_value, y_value in zip(neighbourhoods, x_values, y_values):
        plt.annotate(name, (x_value, y_value), fontsize=7, alpha=0.8)
    plt.title('Parks vs Crimes by Neighbourhood')
    plt.xlabel('Number of Parks')
    plt.ylabel('Number of Crimes')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'parks_vs_crimes.png', dpi=200)
    plt.close()

    proximity = analysis.crime_proximity_to_parks()
    plt.figure(figsize=(8, 5))
    plt.bar([str(radius) for radius in proximity], [proximity[radius] for radius in proximity], color=[PASTEL_100, PASTEL_200, PASTEL_500], edgecolor='black')
    plt.title('Crimes Near Parks by Radius')
    plt.xlabel('Radius (meters)')
    plt.ylabel('Crime Count')
    plt.tight_layout()
    plt.savefig(CHARTS_DIR / 'crimes_near_parks.png', dpi=200)
    plt.close()