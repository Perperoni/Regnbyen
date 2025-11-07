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

    # Redraw map and highlight selected point
    draw_the_map()
    axMap.scatter(x, y, c='red', s=400, marker='o')
    axMap.text(x, y, s=label_from_nedbor(aarsnedbor),
               color='white', ha='center', va='center', fontsize=10)

    # Update left graph
    axGraph.cla()
    if current_view == "Måned":
        plot_month_view(y_pred, aarsnedbor)
    else:
        plot_quarter_view(y_pred, aarsnedbor)
    plt.draw()


def plot_month_view(y_pred, aarsnedbor):
    months = np.linspace(1, 12, 12)
    m_vals = [sum(y_pred[i * 1:(i + 1) * 1]) for i in range(12)]
    axGraph.bar(months, y_pred,
                color=[color_from_nedbor(n * 12) for n in y_pred]) # Tegn stolpediagram
    draw_label_and_ticks()
    avg_m = np.mean(m_vals)
    axGraph.axhline(avg_m, color='r', linestyle='--', label=f'Gjennomsnitt: {avg_m:.1f} mm')
    axGraph.legend(fontsize=10, loc='upper right')
    axGraph.set_title(f"Nedbør per måned – Årsnedbør {int(aarsnedbor)} mm")

def plot_quarter_view(y_pred, aarsnedbor):
    quarters = [1, 2, 3, 4]
    q_vals = [sum(y_pred[i*3:(i+1)*3]) for i in range(4)]
    axGraph.bar(quarters, q_vals, color=[color_from_nedbor(n * 12) for n in y_pred])
    axGraph.set_xticks(quarters)
    axGraph.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
    avg_q = np.mean(q_vals)
    axGraph.axhline(avg_q, color='r', linestyle='--', label=f'Gjennomsnitt: {avg_q:.1f} mm')
    axGraph.legend(fontsize=10, loc='upper right')
    axGraph.set_title(f"Nedbør per kvartal – Årsnedbør {int(aarsnedbor)} mm")

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


fig = plt.figure(figsize=(12, 5))

axGraph = fig.add_axes((0.05, 0.1, 0.35, 0.8))

axMap = fig.add_axes((0.45, 0.1, 0.52, 0.8))

img = mpimg.imread('StorBergen2.png')
axMap.set_title("Årsnedbør Stor Bergen")
axGraph.set_title("Per måned")
axMap.axis('off')

# Radiobutton – placed far left so it doesn’t overlap
axRadio = plt.axes([0.40, 0.20, 0.08, 0.12])
radio = RadioButtons(axRadio, ('Måned', 'Kvartal'))
radio.on_clicked(switch_view)
current_view = "Måned"

# Read rain data, and split in train and test.py data
df = pd.read_csv('NedborX.csv')
marked_point = (0,0)
ns = df['Nedbor']
X = df.drop('Nedbor',  axis=1)
poly = PolynomialFeatures(degree=3)
X_poly = poly.fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(
    X_poly, ns, test_size=0.25)

model = LinearRegression()
model.fit(X_train, Y_train) # fitting the model
Y_pred = model.predict(X_test)

r_squared = r2_score(Y_test, Y_pred)
print(f"R-squared: {r_squared:.2f}")
print('mean_absolute_error (mnd) : ', mean_absolute_error(Y_test, Y_pred))

colors = ['lightblue', 'darkcyan', 'blue', 'darkblue', 'black']
draw_the_map()

plt.connect('button_press_event', on_click)
plt.show()
