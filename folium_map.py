"""
CS5001
Final Project - Folium Map Builder
Spring 2026
21 Apr 26
Adele Ka
"""
from pathlib import Path
import json
import math
import folium
from branca.element import Element
from analysis import Analysis
from data_loader import DataLoader

PASTEL_100 = '#f9c5d1'
PASTEL_200 = '#f7d794'
PASTEL_500 = '#c7ceea'
PURPLE_SCALE = ['#f5e9ff', '#e6ccff', '#d3a9ff', '#bb86fc', '#9b5de5']
MAP_CENTER = [49.255, -123.115]
OUTPUT_MAP = Path('map.html')


def crime_emoji(crime_type):
    """ Returns an emoji that matches a given crime type.

        Args:
        crime_type (str): The name of the crime type.

        Returns: str: An emoji used to represent the crime type on the map. If the crime type is not in the preset mapping, a default pin emoji is returned.
    """
    mapping = {
        'Theft from Vehicle': '🚗',
        'Break and Enter Residential/Other': '🏠',
        'Break and Enter Commercial': '🏢',
        'Mischief': '⚠️',
        'Offence Against a Person': '🚨',
        'Other Theft': '👜',
    }
    return mapping.get(crime_type, '📍')


def purple_for_hectare(hectare):
    """ Chooses a purple color based on park size in hectares.

        Args: hectare (float): The size of the park in hectares.

        Returns: str: A hexadecimal color value from the purple scale that represents the park size category.
    """
    if hectare < 0.5:
        return PURPLE_SCALE[0]
    if hectare < 1.5:
        return PURPLE_SCALE[1]
    if hectare < 5:
        return PURPLE_SCALE[2]
    if hectare < 15:
        return PURPLE_SCALE[3]
    return PURPLE_SCALE[4]


def radius_for_hectare(hectare):
    return max(4, min(14, 4 + math.sqrt(max(hectare, 0)) * 1.3))
    """Calculates a marker radius based on park size.

    Args: hectare (float): The size of the park in hectares.

    Returns: float: A scaled marker radius used to size park markers on the map. The value is limited to a minimum of 4 and a maximum of 14.
    """

def build_map(parks, crimes):
    """Builds and saves an interactive Folium map of parks and nearby crimes.

    This function creates a Folium map centered on Vancouver, prepares park and
    crime data for JavaScript use, adds a custom search panel, and displays
    selected parks with crime proximity circles and crime markers.

    Args:
        parks (list): A list of Park objects.
        crimes (list): A list of Crime objects.

    Returns:
        None: The finished map is saved as an HTML file.
    """
    analysis = Analysis(parks, crimes)
    map_object = folium.Map(location=MAP_CENTER, zoom_start=12, tiles='CartoDB positron')

    parks_payload = []
    for park in parks:
        nearby_crimes = []
        for crime in crimes:
            distance = analysis.haversine_distance_meters(
                park.latitude,
                park.longitude,
                crime.latitude,
                crime.longitude
            )

            if distance <= 500:
                if distance <= 100:
                    band = '100 m'
                    color = '#cc6f95'
                elif distance <= 200:
                    band = '200 m'
                    color = '#e4a15d'
                else:
                    band = '500 m'
                    color = '#7991d1'

                nearby_crimes.append({
                    'crime_type': crime.crime_type,
                    'neighbourhood': crime.neighbourhood,
                    'latitude': crime.latitude,
                    'longitude': crime.longitude,
                    'address': getattr(crime, 'address', 'Address not available'),
                    'emoji': crime_emoji(crime.crime_type),
                    'distance': round(distance, 1),
                    'band': band,
                    'color': color,
                })

        parks_payload.append({
            'name': park.name,
            'neighbourhood': park.neighbourhood,
            'address': park.address() if hasattr(park, 'address') else '',
            'latitude': park.latitude,
            'longitude': park.longitude,
            'hectare': park.hectare,
            'amenities': park.amenities() if hasattr(park, 'amenities') else [],
            'color': purple_for_hectare(park.hectare),
            'radius': radius_for_hectare(park.hectare),
            'nearby_crimes': nearby_crimes,
        })

    neighbourhoods = sorted({park.neighbourhood for park in parks})
    parks_json = json.dumps(parks_payload, ensure_ascii=False)
    neighbourhoods_json = json.dumps(neighbourhoods, ensure_ascii=False)

    custom_html = f"""
<style>
    .workflow-panel {{
        position: fixed;
        top: 12px;
        left: 12px;
        z-index: 9999;
        width: 330px;
        max-height: calc(100vh - 24px);
        overflow-y: auto;
        background: rgba(255, 255, 255, 0.96);
        border: 2px solid #7d5fff;
        border-radius: 14px;
        box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18);
        padding: 14px;
        font-family: Arial, sans-serif;
    }}

    .workflow-panel h3 {{
        margin: 0 0 6px 0;
        color: #6c3eb8;
        font-size: 18px;
    }}

    .workflow-panel p {{
        margin: 0 0 10px 0;
        font-size: 12px;
        line-height: 1.4;
        color: #333;
    }}

    .workflow-panel input {{
        width: 100%;
        padding: 10px 12px;
        font-size: 14px;
        border-radius: 10px;
        border: 1px solid #bbb;
        box-sizing: border-box;
    }}

    .suggestions {{
        margin-top: 8px;
        border: 1px solid #ddd;
        border-radius: 10px;
        max-height: 180px;
        overflow-y: auto;
        background: #fff;
    }}

    .suggestion-item {{
        padding: 10px 12px;
        cursor: pointer;
        border-bottom: 1px solid #eee;
        font-size: 13px;
    }}

    .suggestion-item:last-child {{
        border-bottom: none;
    }}

    .suggestion-item:hover {{
        background: #f4efff;
    }}

    .selected-wrap {{
        margin-top: 14px;
    }}

    .selected-head {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 8px;
    }}

    .selected-head h4 {{
        margin: 0;
        font-size: 14px;
        color: #333;
    }}

    .button-row {{
        display: flex;
        gap: 8px;
    }}

    .display-btn {{
        background: #f4efff;
        color: #6c3eb8;
        border: 1px solid #d6c6ff;
        border-radius: 8px;
        padding: 7px 10px;
        cursor: pointer;
        font-size: 12px;
    }}

    .clear-btn {{
        background: #6c3eb8;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 7px 10px;
        cursor: pointer;
        font-size: 12px;
    }}

    .park-chip {{
        background: #f4efff;
        border: 1px solid #d6c6ff;
        border-radius: 10px;
        padding: 8px 10px;
        margin-top: 8px;
        font-size: 12px;
        cursor: pointer;
    }}

    .legend-box {{
        margin-top: 12px;
        font-size: 12px;
        line-height: 1.5;
    }}

    .legend-dot {{
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 6px;
    }}
</style>

<div class="workflow-panel">
    <h3>Vancouver Parks and Nearby Crimes</h3>
    <p>Search for a park or neighbourhood. Suggestions are case-insensitive and appear as you type.</p>

    <input
        id="mapSearchInput"
        type="text"
        placeholder="Search park or neighbourhood"
        autocomplete="off"
    >

    <div id="suggestions" class="suggestions"></div>

    <div class="selected-wrap">
        <div class="selected-head">
            <h4>Selected parks</h4>
            <div class="button-row">
                <button class="display-btn" onclick="displayAllParks()">Display all</button>
                <button class="clear-btn" onclick="clearAllSelections()">Clear all</button>
            </div>
        </div>
        <div id="selectedParksList"></div>
    </div>

    <div class="legend-box">
        <div><span class="legend-dot" style="background:#cc6f95;"></span>Crimes within 100 m</div>
        <div><span class="legend-dot" style="background:#e4a15d;"></span>Crimes within 200 m</div>
        <div><span class="legend-dot" style="background:#7991d1;"></span>Crimes within 500 m</div>
    </div>
</div>

<script>
(function() {{
    const parksData = {parks_json};
    const neighbourhoods = {neighbourhoods_json};

    function startCustomSearch() {{
        const mapRef = window["{map_object.get_name()}"];
        if (!mapRef) {{
            setTimeout(startCustomSearch, 200);
            return;
        }}

        const selectedParks = new Map();
        const drawnLayers = [];

        function getSearchInput() {{
            return document.getElementById('mapSearchInput');
        }}

        function getSuggestionsBox() {{
            return document.getElementById('suggestions');
        }}

        function getSelectedParksList() {{
            return document.getElementById('selectedParksList');
        }}

        function escapeHtml(text) {{
            return String(text)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }}

        function normalizeText(value) {{
            return String(value || '')
                .normalize('NFD')
                .replace(/[\\u0300-\\u036f]/g, '')
                .toLowerCase()
                .trim();
        }}

        function scoreMatch(name, query) {{
            const normalizedName = normalizeText(name);
            if (normalizedName === query) return 0;
            if (normalizedName.startsWith(query)) return 1;
            if (normalizedName.includes(query)) return 2;
            return 99;
        }}

        function parkPopupHtml(park) {{
            return `
                <div style="font-family:Arial,sans-serif;min-width:220px;">
                    <h4 style="margin:0 0 8px 0;color:#6c3eb8;">${{escapeHtml(park.name)}}</h4>
                    <div><b>Neighbourhood:</b> ${{escapeHtml(park.neighbourhood)}}</div>
                    <div><b>Street address:</b> ${{escapeHtml(park.address || '')}}</div>
                    <div><b>Latitude:</b> ${{Number(park.latitude).toFixed(6)}}</div>
                    <div><b>Longitude:</b> ${{Number(park.longitude).toFixed(6)}}</div>
                    <div><b>Hectares:</b> ${{Number(park.hectare).toFixed(2)}}</div>
                    <div><b>Amenities:</b> ${{escapeHtml((park.amenities || []).join(', '))}}</div>
                </div>
            `;
        }}

        function crimePopupHtml(crime) {{
            return `
                <div style="font-family:Arial,sans-serif;min-width:220px;">
                    <h4 style="margin:0 0 8px 0;color:#444;">${{escapeHtml((crime.emoji || '') + ' ' + crime.crime_type)}}</h4>
                    <div><b>Neighbourhood:</b> ${{escapeHtml(crime.neighbourhood)}}</div>
                    <div><b>Address:</b> ${{escapeHtml(crime.address || '')}}</div>
                    <div><b>Latitude:</b> ${{Number(crime.latitude).toFixed(6)}}</div>
                    <div><b>Longitude:</b> ${{Number(crime.longitude).toFixed(6)}}</div>
                    <div><b>Distance band:</b> ${{escapeHtml(crime.band)}}</div>
                    <div><b>Distance:</b> ${{Number(crime.distance).toFixed(1)}} m</div>
                </div>
            `;
        }}

        function renderSelectedParks() {{
            const selectedParksList = getSelectedParksList();
            selectedParksList.innerHTML = '';

            const names = Array.from(selectedParks.keys());
            if (!names.length) {{
                selectedParksList.innerHTML = '<div style="margin-top:8px;font-size:12px;color:#666;">No parks added yet.</div>';
                return;
            }}

            names.forEach(name => {{
                const chip = document.createElement('div');
                chip.className = 'park-chip';
                chip.textContent = name;
                chip.onclick = () => zoomToPark(name);
                selectedParksList.appendChild(chip);
            }});
        }}

        function zoomToPark(name) {{
            const item = selectedParks.get(name);
            if (!item) return;
            mapRef.setView([item.park.latitude, item.park.longitude], 16);
            item.marker.openPopup();
        }}

        window.clearAllSelections = function() {{
            drawnLayers.forEach(layer => mapRef.removeLayer(layer));
            drawnLayers.length = 0;
            selectedParks.clear();
            renderSelectedParks();
            const suggestions = getSuggestionsBox();
            if (suggestions) suggestions.innerHTML = '';
        }};

        window.displayAllParks = function() {{
            clearAllSelections();
            parksData.forEach(park => {{
                addParkToMap(park);
            }});
        }};

        function addLayer(layer) {{
            layer.addTo(mapRef);
            drawnLayers.push(layer);
            return layer;
        }}

        function addParkToMap(park) {{
            if (selectedParks.has(park.name)) {{
                zoomToPark(park.name);
                return;
            }}

            const treeIcon = L.AwesomeMarkers.icon({{
                icon: 'tree-conifer',
                prefix: 'glyphicon',
                markerColor: 'green',
                iconColor: 'white'
            }});

            const marker = addLayer(L.marker([park.latitude, park.longitude], {{
                icon: treeIcon
            }}));

            marker.bindPopup(parkPopupHtml(park));
            marker.bindTooltip(park.name);

            addLayer(L.circle([park.latitude, park.longitude], {{
                radius: 500,
                color: '{PASTEL_500}',
                weight: 2,
                fillColor: '{PASTEL_500}',
                fillOpacity: 0.08
            }}));

            addLayer(L.circle([park.latitude, park.longitude], {{
                radius: 200,
                color: '{PASTEL_200}',
                weight: 2,
                fillColor: '{PASTEL_200}',
                fillOpacity: 0.14
            }}));

            addLayer(L.circle([park.latitude, park.longitude], {{
                radius: 100,
                color: '{PASTEL_100}',
                weight: 2,
                fillColor: '{PASTEL_100}',
                fillOpacity: 0.22
            }}));

            (park.nearby_crimes || []).forEach(crime => {{
                const crimeMarker = addLayer(L.circleMarker([crime.latitude, crime.longitude], {{
                    radius: 5,
                    color: crime.color,
                    weight: 1,
                    fillColor: crime.color,
                    fillOpacity: 0.95
                }}));
                crimeMarker.bindPopup(crimePopupHtml(crime));
                crimeMarker.bindTooltip(`${{crime.emoji || ''}} ${{crime.crime_type}}`);
            }});

            selectedParks.set(park.name, {{ park, marker }});
            renderSelectedParks();
            mapRef.setView([park.latitude, park.longitude], 16);
            marker.openPopup();
        }}

        function openNeighbourhood(name) {{
            const matches = parksData.filter(
                park => normalizeText(park.neighbourhood) === normalizeText(name)
            );
            if (!matches.length) return;
            matches.forEach(addParkToMap);
            const bounds = L.latLngBounds(matches.map(park => [park.latitude, park.longitude]));
            mapRef.fitBounds(bounds.pad(0.2));
        }}

        function buildSuggestions(query) {{
            const suggestions = getSuggestionsBox();
            suggestions.innerHTML = '';

            const cleaned = normalizeText(query);
            if (!cleaned) return;

            const parkMatches = parksData
                .filter(park => scoreMatch(park.name, cleaned) < 99)
                .sort((a, b) =>
                    scoreMatch(a.name, cleaned) - scoreMatch(b.name, cleaned) ||
                    a.name.localeCompare(b.name)
                )
                .slice(0, 10);

            const neighbourhoodMatches = neighbourhoods
                .filter(name => scoreMatch(name, cleaned) < 99)
                .sort((a, b) =>
                    scoreMatch(a, cleaned) - scoreMatch(b, cleaned) ||
                    a.localeCompare(b)
                )
                .slice(0, 8);

            parkMatches.forEach(park => {{
                const item = document.createElement('div');
                item.className = 'suggestion-item';
                item.innerHTML = `<b>Park:</b> ${{escapeHtml(park.name)}}<br><span style="color:#666;">${{escapeHtml(park.neighbourhood)}}</span>`;
                item.onclick = () => {{
                    getSearchInput().value = '';
                    getSuggestionsBox().innerHTML = '';
                    addParkToMap(park);
                }};
                suggestions.appendChild(item);
            }});

            neighbourhoodMatches.forEach(name => {{
                const item = document.createElement('div');
                item.className = 'suggestion-item';
                item.innerHTML = `<b>Neighbourhood:</b> ${{escapeHtml(name)}}`;
                item.onclick = () => {{
                    getSearchInput().value = '';
                    getSuggestionsBox().innerHTML = '';
                    openNeighbourhood(name);
                }};
                suggestions.appendChild(item);
            }});

            if (!parkMatches.length && !neighbourhoodMatches.length) {{
                const item = document.createElement('div');
                item.className = 'suggestion-item';
                item.innerHTML = '<span style="color:#666;">No matches found</span>';
                suggestions.appendChild(item);
            }}
        }}

        function bindSearchEvents() {{
            const searchInput = getSearchInput();
            if (!searchInput || searchInput.dataset.bound === 'yes') return;

            searchInput.dataset.bound = 'yes';
            searchInput.addEventListener('focus', event => buildSuggestions(event.target.value));
            searchInput.addEventListener('click', event => buildSuggestions(event.target.value));
            searchInput.addEventListener('input', event => buildSuggestions(event.target.value));
            searchInput.addEventListener('keydown', event => {{
                if (event.key === 'Enter') {{
                    event.preventDefault();
                    const first = getSuggestionsBox().querySelector('.suggestion-item');
                    if (first) first.click();
                }}
            }});
        }}

        bindSearchEvents();
        renderSelectedParks();
    }}

    startCustomSearch();
    }})();
    </script>
    """


    map_object.get_root().html.add_child(Element(custom_html))
    map_object.save(OUTPUT_MAP)
    print(f"Map saved to {OUTPUT_MAP.resolve()}")
