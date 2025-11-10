# importing modules and packages
import pandas as pd
import numpy as np
import statistics as stats
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn import preprocessing
import matplotlib.image as mpimg
from sklearn.preprocessing import PolynomialFeatures
from matplotlib.patches import Patch
from matplotlib.widgets import RadioButtons


def draw_the_map():
    # Accumulate all months to year
    axMap.cla()
    axMap.imshow(img, extent=(0, 13, 0, 10))
    if current_data == "Nedbor":
        draw_the_map_nedbor()
    if current_data == "Vindstyrke":
        draw_the_map_vindstyrke()

def draw_the_map_nedbor():
    df_year = df.groupby(['X', 'Y']).agg({'Nedbor': 'sum'}).reset_index()
    xr = df_year['X'].tolist()
    yr = df_year['Y'].tolist()
    nedborAar = df_year['Nedbor']
    ColorList = [color_from_nedbor(n) for n in nedborAar]
    axMap.scatter(xr, yr, c=ColorList, s=size_from_nedbor(nedborAar/12), alpha=1)
    labels = [label_from_nedbor(n) for n in nedborAar]
    for i, y in enumerate(xr):
        axMap.text(xr[i], yr[i], s=labels[i], color='white',
                   fontsize=10, ha='center', va='center')

    legend_elements = [
        Patch(facecolor='lightblue', label='<1300 mm'),
        Patch(facecolor='darkcyan', label='1300–1700 mm'),
        Patch(facecolor='blue', label='1700–2500 mm'),
        Patch(facecolor='darkblue', label='2500–3200 mm'),
        Patch(facecolor='black', label='>3200 mm')
    ]
    axMap.legend(handles=legend_elements, title="Årsnedbør (mm)",
                 loc='upper right', fontsize=8)
    axMap.set_title("Årsnedbør – Stor Bergen")
    axMap.axis('off')

def draw_the_map_vindstyrke():
    df_year = df_vind.groupby(['X', 'Y']).agg({'Vindstyrke': 'mean'}).reset_index()
    xr = df_year['X'].tolist()
    yr = df_year['Y'].tolist()
    vindstyrkeaar = df_year['Vindstyrke']
    ColorList = [color_from_vindstyrke(n) for n in vindstyrkeaar]
    axMap.scatter(xr, yr, c=ColorList, s=size_from_nedbor(vindstyrkeaar), alpha=1)
    labels = [label_from_vindstyrke(n) for n in vindstyrkeaar]
    for i, y in enumerate(xr):
        axMap.text(xr[i], yr[i], s=labels[i], color=color_for_font(ColorList[i]),
                   fontsize=10, ha='center', va='center')
    legend_elements = size_legend_element(vindstyrkeaar)
    axMap.legend(handles=legend_elements, title="Vindstyrke (m/s)",
                 loc='upper right', fontsize=8)
    axMap.set_title("Vindstyrke – Stor Bergen")
    
def size_legend_element(data):
    largest = float('-inf')
    for n in data:
        if n > largest:
            largest = n
    return_legend_element = [Patch(facecolor='#FFFFFF', label='0–0.2 m/s')]
    if largest > 0.3: return_legend_element.append(Patch(facecolor='#E0FFFF', label='0.3–1.5 m/s'))
    if largest > 1.6: return_legend_element.append(Patch(facecolor='#ADD8E6', label='1.6–3.3 m/s'))
    if largest > 3.4: return_legend_element.append(Patch(facecolor='#87CEEB', label='3.4–5.4 m/s'))
    if largest > 5.5: return_legend_element.append(Patch(facecolor='#4682B4', label='5.5–7.9 m/s'))
    if largest > 8.0: return_legend_element.append(Patch(facecolor='#0000FF', label='8.0–10.7 m/s'))
    if largest > 10.8: return_legend_element.append(Patch(facecolor='#00008B', label='10.8–13.8 m/s'))
    if largest > 13.9: return_legend_element.append(Patch(facecolor='#4B0082', label='13.9–17.1 m/s'))
    if largest > 17.2: return_legend_element.append(Patch(facecolor='#800080', label='17.2–20.7 m/s'))
    if largest > 20.8: return_legend_element.append(Patch(facecolor='#8B0000', label='20.8–24.4 m/s'))
    if largest > 24.5: return_legend_element.append(Patch(facecolor='#A52A2A', label='24.5–28.4 m/s'))
    if largest > 28.5: return_legend_element.append(Patch(facecolor='#D2691E', label='28.5–32.5 m/s'))
    if largest >= 32.6: return_legend_element.append(Patch(facecolor='#FF4500', label='>32.6 m/s'))
    return return_legend_element
        
    

def index_from_nedbor(x):
    if x < 1300: return 0
    if x < 1700: return 1
    if x < 2500: return 2
    if x < 3200: return 3
    return 4


def color_from_nedbor(nedbor):
    return colors[index_from_nedbor(nedbor)]


def size_from_nedbor(nedbor):
    return 350


def label_from_nedbor(nedbor):
    return str(int(nedbor / 100))

def index_from_vindstyrke(x):
    if x < 0.3: return 0
    if x < 1.6: return 1
    if x < 3.4: return 2
    if x < 5.5: return 3
    if x < 8.0: return 4
    if x < 10.8: return 5
    if x < 13.9: return 6
    if x < 17.2: return 7
    if x < 20.8: return 8
    if x < 24.5: return 9
    if x < 28.5: return 10
    if x < 32.6: return 11
    return 12

def color_from_vindstyrke(vindstyrke):
    return baufort_color[index_from_vindstyrke(vindstyrke)]

def label_from_vindstyrke(vindstyrke):
    return str(round(vindstyrke,1))

def color_for_font(color):
    hex_str = color.lstrip('#')
    r, g, b = int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)
    brightness = (r * 299 + g * 587 + b * 114) / 1000
    if brightness > 125:
        return 'black'
    else:
        return 'white'


def on_click(event) :
    global marked_point
    if event.inaxes != axMap:
        return
    marked_point = (event.xdata, event.ydata)
    x,y = marked_point

    # Predict monthly rainfall for clicked location
    vectors = np.vstack([[x, y, m] for m in range(1, 13)])
    AtPointM = poly.fit_transform(vectors)
    y_pred = model.predict(AtPointM)
    aarsnedbor = sum(y_pred)

    vectors_vind = np.vstack([[x, y, m] for m in range(1, 13)])
    AtPointV = poly_vind.fit_transform(vectors_vind)
    y_pred_vind = model_vind.predict(AtPointV)
    print(y_pred_vind)
    aarsvindstyrke = stats.mean(y_pred_vind)
    if aarsvindstyrke < 0: aarsvindstyrke = 0

    # Redraw map and highlight selected point
    draw_the_map()
    axMap.scatter(x, y, c='red', s=400, marker='o')
    if current_data == 'Nedbor': axMap.text(x, y, s=label_from_nedbor(aarsnedbor), color='white', ha='center', va='center', fontsize=10)
    if current_data == 'Vindstyrke': axMap.text(x, y, s=label_from_vindstyrke(aarsvindstyrke), color='white', ha='center', va='center', fontsize=10)
    # Update left graph
    axGraph.cla()
    if current_view == "Måned":
        if current_data == 'Nedbor': plot_month_view(y_pred, aarsnedbor)
        if current_data == 'Vindstyrke': plot_month_view(y_pred_vind, aarsvindstyrke)
    else:
        if current_data == 'Nedbor': plot_quarter_view(y_pred, aarsnedbor)
        if current_data == 'Vindstyrke': plot_quarter_view(y_pred_vind, aarsvindstyrke)
    plt.draw()


def plot_month_view(y_pred, aarsnedbor):
    months = np.linspace(1, 12, 12)
    m_vals = [sum(y_pred[i * 1:(i + 1) * 1]) for i in range(12)]
    if current_data == 'Nedbor': axGraph.bar(months, y_pred, color=[color_from_nedbor(n * 12) for n in y_pred]) # Tegn stolpediagram
    if current_data == 'Vindstyrke': axGraph.bar(months, y_pred, color=[color_from_vindstyrke(n) for n in y_pred]) # Tegn stolpediagram
    draw_label_and_ticks()
    avg_m = np.mean(m_vals)
    if current_data == 'Nedbor':axGraph.axhline(avg_m, color='r', linestyle='--', label=f'Gjennomsnitt: {avg_m:.1f} mm')
    if current_data == 'Vindstyrke':axGraph.axhline(avg_m, color='r', linestyle='--', label=f'Gjennomsnitt: {avg_m:.1f} m/s')
    axGraph.legend(fontsize=10, loc='upper right')
    if current_data == 'Nedbor':axGraph.set_title(f"Nedbør per måned – Årsnedbør {int(aarsnedbor)} mm")
    if current_data == 'Vindstyrke':axGraph.set_title(f"Vindstyrke per måned")

def plot_quarter_view(y_pred, aarsnedbor):
    quarters = [1, 2, 3, 4]
    q_vals = [sum(y_pred[i*3:(i+1)*3]) for i in range(4)]
    if current_data == 'Nedbor': axGraph.bar(quarters, q_vals, color=[color_from_nedbor(n * 12) for n in y_pred])
    if current_data == 'Vindstyrke': axGraph.bar(quarters, q_vals, color=[color_from_vindstyrke(n) for n in y_pred])
    axGraph.set_xticks(quarters)
    axGraph.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    avg_q = np.mean(q_vals)
    if avg_q < 0: avg_q = 0
    if current_data == 'Nedbor': axGraph.axhline(avg_q, color='r', linestyle='--', label=f'Gjennomsnitt: {avg_q:.1f} mm')
    if current_data == 'Vindstyrke': axGraph.axhline(avg_q, color='r', linestyle='--', label=f'Gjennomsnitt: {avg_q:.1f} m/s')
    axGraph.legend(fontsize=10, loc='upper right')
    if current_data == 'Nedbor':axGraph.set_title(f"Nedbør per kvartal – Årsnedbør {int(aarsnedbor)} mm")
    if current_data == 'Vindstyrke':axGraph.set_title(f"Vindstyrke per kvartal")

def draw_label_and_ticks():
    xlabels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    axGraph.set_xticks(np.linspace(1, 12, 12))
    axGraph.set_xticklabels(xlabels)


def switch_view(label):
    global current_view
    current_view = label
    axGraph.cla()
    if label == "Måned":
        axGraph.set_title("Nedbør per måned")
        draw_label_and_ticks()
    else:
        axGraph.bar([1, 2, 3, 4], [0, 0, 0, 0], color='skyblue')
        axGraph.set_xticks([1, 2, 3, 4])
        axGraph.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
        axGraph.set_title("Nedbør per kvartal")
    plt.draw()

def switch_data(label):
    global current_data
    current_data = label
    axGraph.cla()
    draw_the_map()
    plt.draw()


fig = plt.figure(figsize=(12, 5))

axGraph = fig.add_axes((0.05, 0.1, 0.35, 0.8))

axMap = fig.add_axes((0.45, 0.1, 0.52, 0.8))

img = mpimg.imread('StorBergen2.png')
axMap.set_title("Årsnedbør Stor Bergen")
axGraph.set_title("Per måned")
axMap.axis('off')

# Radiobutton – placed far left so it doesn’t overlap
axRadio_view = plt.axes([0.40, 0.20, 0.09, 0.12])
radio_view = RadioButtons(axRadio_view, ('Måned', 'Kvartal'))
radio_view.on_clicked(switch_view)
current_view = "Måned"

axRadio_data = plt.axes([0.40, 0.35, 0.09, 0.12])
radio_data = RadioButtons(axRadio_data, ('Nedbor', 'Vindstyrke'))
radio_data.on_clicked(switch_data)
current_data = "Nedbor"

# Read rain data, and split in train and test.py data
df = pd.read_csv('NedborX.csv')
marked_point = (0,0)
ns = df['Nedbor']
X = df.drop('Nedbor',  axis=1)
poly = PolynomialFeatures(degree=3)
X_poly = poly.fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(
    X_poly, ns, test_size=0.25)

model = LinearRegression(positive=True)
model.fit(X_train, Y_train) # fitting the model
Y_pred = model.predict(X_test)

r_squared = r2_score(Y_test, Y_pred)
print(f"R-squared: {r_squared:.2f}")
print('mean_absolute_error (mnd) : ', mean_absolute_error(Y_test, Y_pred))

df_vind = pd.read_csv('VindstyrkeX.csv')
ns_vind = df_vind['Vindstyrke']
X_vind = df_vind.drop('Vindstyrke',  axis=1)
poly_vind = PolynomialFeatures(degree=3)
X_poly_vind = poly_vind.fit_transform(X_vind)
X_train_vind, X_test_vind, Y_train_vind, Y_test_vind = train_test_split(
    X_poly_vind, ns_vind, test_size=0.25)

model_vind = LinearRegression()
model_vind.fit(X_train_vind, Y_train_vind) # fitting the model
Y_pred_vind = model_vind.predict(X_test_vind)


r_squared_vind = r2_score(Y_test_vind, Y_pred_vind)
print(f"R-squared Vindstyrke: {r_squared_vind:.2f}")
print('mean_absolute_error Vindstyrke (mnd) : ', mean_absolute_error(Y_test_vind, Y_pred_vind))

colors = ['lightblue', 'darkcyan', 'blue', 'darkblue', 'black']
baufort_color = ['#FFFFFF', '#E0FFFF', '#ADD8E6', '#87CEEB', '#4682B4',
                 '#0000FF', '#00008B', '#4B0082', '#800080', '#8B0000',
                 '#A52A2A', '#D2691E', '#FF4500']
draw_the_map()

plt.connect('button_press_event', on_click)
plt.show()
