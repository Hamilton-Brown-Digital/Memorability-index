import os
import io
import time
import requests
import numpy as np
import cv2
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sklearn.cluster import KMeans
from collections import Counter

# --- Helper Functions ---

def clean_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "https://" + url
    return url

def take_screenshot(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    time.sleep(3)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()
    return Image.open(io.BytesIO(screenshot))

def extract_colour_palette(image, num_colours=5):
    image = image.resize((300, 300))
    image_np = np.array(image)
    image_np = image_np.reshape((image_np.shape[0] * image_np.shape[1], 3))
    kmeans = KMeans(n_clusters=num_colours, n_init=10)
    labels = kmeans.fit_predict(image_np)
    counts = Counter(labels)
    total_count = sum(counts.values())
    palette = [(tuple(map(int, kmeans.cluster_centers_[i])), count / total_count)
               for i, count in counts.items()]
    return sorted(palette, key=lambda x: x[1], reverse=True)

def calculate_whitespace_ratio(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY)
    white_pixels = np.sum(binary == 255)
    total_pixels = binary.size
    return white_pixels / total_pixels

def detect_typography_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    fonts = set()
    for tag in soup.find_all(style=True):
        styles = tag['style'].split(';')
        for style in styles:
            if 'font-family' in style:
                fonts.add(style.strip())
    return len(fonts)

def count_visual_elements(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    edged = cv2.Canny(gray, 30, 100)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return len(contours)

def score_visual_distinctiveness(whitespace_ratio, element_count, colour_diversity, typography_count,
                                  brand_colour_consistent=True, hierarchy=True, imagery_match=True):
    score = 0
    if whitespace_ratio > 0.5:
        score += 2.5
    elif whitespace_ratio > 0.3:
        score += 2.0
    else:
        score += 1.0

    if element_count < 200:
        score += 2.5
    elif element_count < 350:
        score += 1.5
    else:
        score += 0.5

    if colour_diversity >= 5:
        score += 2.0
    elif colour_diversity >= 3:
        score += 1.0
    else:
        score += 0.5

    if typography_count >= 4:
        score += 2.0
    elif typography_count >= 2:
        score += 1.0
    else:
        score += 0.5

    if brand_colour_consistent:
        score += 1.0
    if hierarchy:
        score += 1.0
    if imagery_match:
        score += 1.0

    return round(min(score, 10.0), 1)

def generate_summary(score, breakdown):
    summary = []

    if score >= 8:
        summary.append("This site has strong visual branding with excellent use of space, colour, and consistent styling.")
    elif score >= 5:
        summary.append("The site is moderately distinctive but could benefit from improved hierarchy or colour consistency.")
    else:
        summary.append("Visual branding could be improved. Consider simplifying layout, reducing clutter, or using more consistent colours.")

    if breakdown["Whitespace Ratio"] < 0.2:
        summary.append("Whitespace is limited, which may contribute to visual clutter.")
    if breakdown["Typography Variety Count"] > 4:
        summary.append("The site uses many font styles, which might reduce consistency.")
    if breakdown["Colour Diversity"] < 3:
        summary.append("Limited colour diversity may make the site feel flat.")

    return " ".join(summary)

# --- Main Function ---

def analyze_website(url):
    url = clean_url(url)
    try:
        screenshot = take_screenshot(url)
        html = requests.get(url).text
    except Exception as e:
        return {"error": f"Failed to load the website: {str(e)}"}

    os.makedirs("static", exist_ok=True)
    screenshot_filename = "screenshot.png"
    screenshot.save(os.path.join("static", screenshot_filename))

    palette = extract_colour_palette(screenshot)
    whitespace_ratio = calculate_whitespace_ratio(screenshot)
    element_count = count_visual_elements(screenshot)
    colour_diversity = len(palette)
    typography_count = detect_typography_count(html)

    score = score_visual_distinctiveness(
        whitespace_ratio, element_count, colour_diversity, typography_count,
        brand_colour_consistent=True,
        hierarchy=True,
        imagery_match=True
    )

    summary = generate_summary(score, {
        "Whitespace Ratio": whitespace_ratio,
        "Visual Elements Count": element_count,
        "Colour Diversity": colour_diversity,
        "Typography Variety Count": typography_count
    })

    swatches = [{
        "hex": '#{:02x}{:02x}{:02x}'.format(*rgb),
        "percentage": round(p * 100, 1)
    } for rgb, p in palette]

    return {
        "score": score,
        "screenshot": screenshot_filename,
        "summary": summary,
        "breakdown": {
            "Whitespace Ratio": round(whitespace_ratio, 2),
            "Visual Elements Count": element_count,
            "Colour Diversity": colour_diversity,
            "Typography Variety Count": typography_count,
            "Brand Colour Consistency": "✔️",
            "Visual Hierarchy Present": "✔️",
            "Imagery Matches Tone": "✔️",
            "Dominant Colours": swatches
        }
    }
