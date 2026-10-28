# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "python-igraph==0.11.9",
# ]
# ///
#
# Mini project M06 -- Where do New York's referrals jam, and how do you fix it?
#
# Two questions, built on one simulated referral network among the hospitals of
# New York City.
#
#   Q1  Which hospitals are the bottlenecks?  First with no capacity limit
#       (betweenness is exactly the answer), then with capacity limits
#       (betweenness stops being the answer; the team designs a score that is).
#   Q2  With a fixed budget, write a function that upgrades the network.
#
# The notebook travels alone (molab, one file). The hospitals, their catchment
# populations, the two referral networks and the two capacity vectors are
# literals between the BUILT-DATA markers below, written by
# tools/build_m06_mini_data.py. Nothing is fetched at run time.
#
# TWO PENCIL CELLS. PLAN_1B and PLAN_2 are the team's reasoning in plain English
# and are what is graded. The code beside each is the same reasoning as code,
# which the team's coding agent may write from the plan.
#
# Calibration (the starting code and the benchmarks are run by the notebook
# itself; the numbers on the page are the numbers we see). Averages over A, B:
#   Q1a  in-degree 0.71, PageRank 0.73, closeness 0.79, betweenness 1.00 (exact)
#   Q1b  betweenness 0.45, betweenness x population 0.27,
#        benchmark (a 4-step walk seeded by the overload) 0.81
#   Q2   do nothing 2.35% unserved, random spending 1.67%, starting code 1.67%,
#        benchmark 1.22%, a greedy search that runs the simulator 0.71%

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The kit. Nothing here is yours to edit.
    import time
    import types

    import igraph
    import marimo as mo
    import numpy as np

    # ---------------------------------------------------------------- style
    INK, MUTED, RULE = "#1a1a1a", "#6b6b6b", "#d8d4cc"
    RUST, BLUE = "#b5482f", "#2f5d8a"
    SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
    MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

    # ---------------------------------------------------------------- data
    # BUILT-DATA-BEGIN
    HOSPITALS = [
        ('Long Island Jewish Medical Center', 40.7547, -73.7066, 120600),
        ('David H. Koch Center For Cancer Care', 40.7676, -73.9516, 40900),
        ('Maimonides Midwood Community Hospital', 40.6134, -73.9490, 157900),
        ('New York-Presbyterian David H. Koch Center', 40.7648, -73.9553, 7400),
        ('University Hospital of Brooklyn', 40.6545, -73.9450, 164400),
        ('Maimonides Medical Center', 40.6394, -73.9984, 375100),
        ('Long Island Jewish Forest Hills', 40.7287, -73.8510, 234000),
        ('Staten Island University Hosp-North', 40.5845, -74.0856, 127800),
        ('Hospital for Special Surgery', 40.7654, -73.9542, 10800),
        ('Calvary Hospital', 40.6464, -74.0210, 81100),
        ("Staten Island University Hospital Prince's Bay", 40.5168, -74.1968, 135800),
        ('Montefiore Medical Center - Henry & Lucy Moses Div', 40.8799, -73.8799, 76700),
        ('Flushing Hospital Medical Center', 40.7555, -73.8155, 276700),
        ('Mount Sinai Brooklyn', 40.6180, -73.9432, 148200),
        ('Mount Sinai -  Behavioral Health Center', 40.7208, -73.9911, 114000),
        ('Queens Hospital Center', 40.7172, -73.8036, 316400),
        ('Metropolitan Hospital Center', 40.7848, -73.9437, 72800),
        ('BronxCare Hospital Center (Bronx)', 40.8436, -73.9115, 147800),
        ('Mount Sinai Hospital - Mount Sinai Hospital of Queens', 40.7683, -73.9245, 209000),
        ('Northwell Greenwich Village Hospital', 40.7376, -74.0005, 124000),
        ('NYU Langone Hospital-Brooklyn', 40.6466, -74.0204, 52700),
        ('Mount Sinai Morningside', 40.8059, -73.9616, 126100),
        ('Bellevue Hospital Center', 40.7396, -73.9765, 33500),
        ('St Johns Episcopal Hospital So Shore', 40.5986, -73.7528, 147000),
        ('Montefiore Medical Center-Wakefield Hospital', 40.8946, -73.8614, 119900),
        ('Kingsbrook Jewish Medical Village', 40.6594, -73.9340, 81900),
        ('Elmhurst Hospital Center', 40.7443, -73.8857, 423000),
        ('New York Eye and Ear Infirmary of Mount Sinai', 40.7322, -73.9847, 79400),
        ('New York-Presbyterian Hospital - New York Weill Cornell Center', 40.7641, -73.9549, 35200),
        ('Jacobi Medical Center', 40.8574, -73.8467, 136900),
        ('New York-Presbyterian Hospital - Columbia Presbyterian Center', 40.8413, -73.9407, 175000),
        ('Mount Sinai West', 40.7701, -73.9878, 193800),
        ('Woodhull Medical & Mental Health Center', 40.7005, -73.9417, 397900),
        ('SBH Health System', 40.8539, -73.8910, 180900),
        ('New York-Presbyterian Hospital - Allen Hospital', 40.8725, -73.9128, 165100),
        ('Lenox Hill Hospital', 40.7739, -73.9606, 89700),
        ('Kings County Hospital Center', 40.6558, -73.9441, 46100),
        ("Montefiore Einstein Children's Center for Mental Health of the Children's Hospital at Montefiore Einstein", 40.8461, -73.8385, 65200),
        ('NewYork-Presbyterian/Queens', 40.7475, -73.8260, 73800),
        ('Calvary Hospital Inc', 40.8473, -73.8447, 2700),
        ('Harlem Hospital Center', 40.8143, -73.9405, 134600),
        ('Brookdale Hospital Medical Center', 40.6551, -73.9126, 394100),
        ('RUMC-Bayley Seton', 40.6214, -74.0748, 72900),
        ('Interfaith Medical Center', 40.6779, -73.9375, 237200),
        ('North Central Bronx Hospital', 40.8805, -73.8815, 62500),
        ('Montefiore Medical Center - Montefiore Westchester Square', 40.8404, -73.8482, 193500),
        ('NewYork-Presbyterian Brooklyn Methodist Hospital', 40.6681, -73.9789, 111900),
        ('Mount Sinai Hospital', 40.7905, -73.9538, 95300),
        ('South Brooklyn Health', 40.5866, -73.9658, 307600),
        ('Montefiore Med Center - Jack D Weiler Hosp of A Einstein College Div', 40.8496, -73.8451, 9200),
        ('BronxCare Hospital Center (Bronx)', 40.8318, -73.9037, 210000),
        ('NYU Langone Hospitals', 40.7429, -73.9742, 103200),
        ('Brooklyn Hospital Center - Downtown Campus', 40.6898, -73.9775, 137400),
        ('New York-Presbyterian/Lower Manhattan Hospital', 40.7104, -74.0055, 99600),
        ('NYU Langone Hospital - Joseph S. and Diane H. Steinberg Ambulatory Care Center', 40.6909, -73.9975, 83600),
        ('Richmond University Medical Center', 40.6358, -74.1067, 172400),
        ('Memorial Hospital for Cancer and Allied Diseases', 40.7644, -73.9568, 76000),
        ('Henry J. Carter Specialty Hospital', 40.8030, -73.9408, 75200),
        ('NYU Langone Orthopedic Hospital', 40.7341, -73.9831, 51500),
        ('Lincoln Medical & Mental Health Center', 40.8177, -73.9242, 136800),
        ('Jamaica Hospital Medical Center', 40.7014, -73.8163, 472400),
    ]
    EDGES = {
        'A': [(0, 12), (0, 15), (0, 32), (0, 58), (1, 3), (1, 8), (1, 25), (1, 60), (2, 10), (2, 13), (2, 42), (2, 48), (3, 8), (3, 28), (3, 45), (3, 60), (4, 2), (4, 19), (4, 25), (4, 36), (5, 9), (5, 20), (5, 27), (5, 31), (6, 9), (6, 26), (6, 38), (6, 50), (7, 26), (7, 37), (7, 42), (7, 55), (8, 3), (8, 28), (8, 32), (8, 38), (9, 2), (9, 5), (9, 20), (9, 30), (10, 7), (10, 46), (10, 55), (11, 24), (11, 32), (11, 39), (11, 44), (12, 6), (12, 21), (12, 28), (12, 38), (13, 2), (13, 48), (13, 60), (14, 18), (14, 27), (14, 58), (15, 14), (15, 29), (15, 38), (15, 60), (16, 7), (16, 35), (16, 47), (17, 26), (17, 33), (17, 49), (17, 50), (18, 1), (18, 12), (18, 16), (18, 32), (19, 15), (19, 27), (19, 58), (20, 5), (20, 9), (20, 45), (20, 53), (21, 16), (21, 34), (21, 47), (21, 57), (22, 30), (22, 36), (22, 51), (22, 58), (23, 15), (23, 21), (23, 60), (24, 4), (24, 11), (24, 44), (24, 60), (25, 4), (25, 36), (25, 41), (25, 43), (26, 6), (26, 10), (26, 18), (26, 33), (27, 16), (27, 22), (27, 40), (27, 58), (28, 3), (28, 8), (28, 10), (28, 48), (29, 39), (29, 49), (29, 55), (29, 60), (30, 17), (30, 32), (30, 33), (30, 59), (31, 6), (31, 35), (31, 43), (31, 56), (32, 8), (32, 40), (32, 43), (32, 52), (33, 11), (33, 17), (33, 48), (33, 50), (34, 33), (34, 37), (34, 44), (34, 57), (35, 1), (35, 8), (35, 46), (35, 57), (36, 4), (36, 25), (36, 47), (37, 23), (37, 32), (37, 39), (37, 49), (38, 5), (38, 6), (38, 12), (38, 28), (39, 5), (39, 37), (39, 49), (39, 51), (40, 3), (40, 38), (40, 57), (40, 59), (41, 25), (41, 36), (41, 52), (42, 7), (42, 20), (42, 34), (42, 55), (43, 1), (43, 15), (43, 25), (43, 36), (44, 11), (44, 22), (44, 24), (44, 51), (45, 17), (45, 31), (45, 37), (45, 39), (46, 31), (46, 50), (46, 52), (46, 54), (47, 16), (47, 45), (47, 57), (47, 59), (48, 2), (48, 9), (48, 13), (48, 16), (49, 37), (49, 39), (49, 50), (49, 56), (50, 17), (50, 41), (50, 44), (50, 59), (51, 22), (51, 47), (51, 54), (51, 58), (52, 12), (52, 24), (52, 46), (52, 54), (53, 0), (53, 14), (53, 48), (53, 54), (54, 12), (54, 26), (54, 52), (54, 53), (55, 5), (55, 7), (55, 15), (55, 42), (56, 3), (56, 12), (56, 28), (56, 51), (57, 19), (57, 40), (57, 47), (57, 52), (58, 13), (58, 22), (58, 27), (58, 53), (59, 29), (59, 40), (59, 57), (60, 6), (60, 15)],
        'B': [(0, 5), (0, 12), (0, 15), (0, 36), (1, 3), (1, 8), (1, 15), (1, 54), (2, 13), (2, 48), (2, 57), (3, 8), (3, 21), (3, 28), (3, 34), (4, 6), (4, 25), (4, 36), (4, 37), (5, 3), (5, 9), (5, 20), (5, 28), (6, 26), (6, 30), (6, 38), (6, 52), (7, 11), (7, 42), (7, 49), (7, 55), (8, 3), (8, 12), (8, 28), (8, 45), (9, 5), (9, 6), (9, 17), (9, 20), (10, 6), (10, 7), (10, 26), (10, 55), (11, 24), (11, 29), (11, 32), (11, 44), (12, 6), (12, 27), (12, 31), (12, 38), (13, 2), (13, 34), (13, 35), (13, 48), (14, 27), (14, 39), (14, 45), (14, 58), (15, 8), (15, 38), (15, 60), (16, 17), (16, 35), (16, 47), (16, 55), (17, 33), (17, 38), (17, 41), (17, 50), (18, 1), (18, 16), (18, 43), (18, 47), (19, 17), (19, 27), (19, 40), (19, 58), (20, 0), (20, 5), (20, 9), (20, 23), (21, 34), (21, 47), (21, 57), (21, 60), (22, 18), (22, 51), (22, 58), (22, 60), (23, 15), (23, 18), (23, 33), (23, 60), (24, 11), (24, 44), (24, 55), (24, 56), (25, 4), (25, 13), (25, 34), (25, 36), (26, 0), (26, 6), (26, 18), (26, 31), (27, 22), (27, 47), (27, 48), (27, 58), (28, 2), (28, 3), (28, 7), (28, 8), (29, 15), (29, 39), (29, 43), (29, 49), (30, 17), (30, 22), (30, 23), (30, 59), (31, 5), (31, 35), (31, 56), (31, 58), (32, 25), (32, 41), (32, 43), (32, 52), (33, 17), (33, 28), (33, 50), (33, 59), (34, 12), (34, 33), (34, 44), (34, 45), (35, 1), (35, 8), (35, 40), (36, 4), (36, 18), (36, 20), (36, 25), (37, 5), (37, 39), (37, 45), (37, 49), (38, 6), (38, 12), (38, 43), (38, 51), (39, 13), (39, 24), (39, 37), (39, 49), (40, 30), (40, 50), (40, 57), (40, 59), (41, 25), (41, 27), (41, 36), (41, 38), (42, 7), (42, 41), (42, 53), (42, 55), (43, 18), (43, 25), (43, 36), (43, 50), (44, 11), (44, 14), (44, 24), (44, 26), (45, 37), (45, 39), (45, 41), (45, 46), (46, 50), (46, 52), (46, 54), (47, 6), (47, 16), (47, 57), (48, 2), (48, 13), (48, 44), (48, 52), (49, 25), (49, 37), (49, 39), (49, 43), (50, 17), (50, 29), (50, 59), (51, 9), (51, 19), (51, 22), (51, 58), (52, 32), (52, 41), (52, 46), (52, 54), (53, 14), (53, 17), (53, 26), (53, 54), (54, 9), (54, 52), (54, 53), (55, 7), (55, 10), (55, 15), (55, 42), (56, 3), (56, 28), (56, 32), (56, 42), (57, 11), (57, 25), (57, 40), (57, 47), (58, 22), (58, 27), (58, 35), (58, 46), (59, 4), (59, 12), (59, 40), (59, 57), (60, 2), (60, 6), (60, 11), (60, 15)],
    }
    CAPACITY = {
        'A': [126900, 78200, 284000, 6100, 149000, 306700, 313400, 129200, 15700, 36600, 284900, 76100, 389500, 144500, 99600, 403900, 109400, 139800, 202200, 175000, 36900, 66100, 41500, 112700, 52400, 58900, 355200, 48100, 18600, 144300, 271600, 180900, 295100, 223000, 236300, 81200, 61100, 108100, 69700, 1900, 163100, 456600, 123900, 137900, 48100, 137500, 53200, 104600, 404300, 6800, 406100, 154800, 188900, 123700, 133200, 98100, 103800, 102200, 24100, 165800, 437500],
        'B': [255500, 9500, 226300, 7100, 277100, 415500, 495900, 120700, 8000, 98100, 153600, 60800, 230500, 190800, 145700, 235900, 57500, 61000, 414300, 104400, 89600, 141700, 74800, 273400, 128800, 148500, 256900, 130300, 16800, 148800, 263100, 199600, 314100, 117200, 131800, 134000, 64100, 54000, 39200, 3400, 65300, 289000, 48800, 308600, 64700, 221800, 117800, 65400, 364500, 16200, 192300, 127800, 120900, 147300, 105100, 238100, 82800, 146500, 40800, 109600, 337000],
    }
    BASEMAP = [[(-73.9626, 40.739), (-73.9614, 40.7428), (-73.9562, 40.7497), (-73.9413, 40.7669), (-73.9364, 40.7695), (-73.935, 40.7717), (-73.9375, 40.7725), (-73.9379, 40.7741), (-73.9364, 40.7769), (-73.9339, 40.7781), (-73.9318, 40.7779), (-73.9299, 40.7762), (-73.9248, 40.7788), (-73.9172, 40.7842), (-73.9103, 40.7907), (-73.9107, 40.7931), (-73.9125, 40.7961), (-73.8906, 40.7901), (-73.8883, 40.787), (-73.8783, 40.7854), (-73.8731, 40.7859), (-73.8708, 40.7879), (-73.8702, 40.7909), (-73.863, 40.7977), (-73.8531, 40.8001), (-73.8354, 40.8022), (-73.8174, 40.8058), (-73.8113, 40.8054), (-73.7941, 40.8005), (-73.7952, 40.7917), (-73.7939, 40.789), (-73.7841, 40.7901), (-73.7808, 40.7919), (-73.7807, 40.7956), (-73.7783, 40.7967), (-73.7756, 40.7956), (-73.7706, 40.7884), (-73.7743, 40.7862), (-73.7678, 40.7788), (-73.7655, 40.7745), (-73.7579, 40.7669), (-73.7562, 40.7664), (-73.7549, 40.7672), (-73.7553, 40.7717), (-73.7534, 40.7731), (-73.7551, 40.7766), (-73.753, 40.7813), (-73.7503, 40.7825), (-73.7016, 40.7525), (-73.7004, 40.7392), (-73.7079, 40.7278), (-73.7165, 40.7265), (-73.7303, 40.7222), (-73.727, 40.7107), (-73.7256, 40.6796), (-73.7275, 40.6742), (-73.7282, 40.6625), (-73.7262, 40.6585), (-73.725, 40.6527), (-73.7297, 40.6506), (-73.7351, 40.6497), (-73.7414, 40.6469), (-73.7414, 40.6405), (-73.7423, 40.6401), (-73.7395, 40.6357), (-73.74, 40.6351), (-73.7426, 40.6356), (-73.7413, 40.6373), (-73.7424, 40.6381), (-73.7439, 40.6375), (-73.746, 40.6352), (-73.7674, 40.6266), (-73.7688, 40.6244), (-73.7676, 40.6215), (-73.7667, 40.615), (-73.7652, 40.6149), (-73.76, 40.6113), (-73.7547, 40.6104), (-73.7491, 40.6118), (-73.7455, 40.6118), (-73.7432, 40.6072), (-73.7384, 40.6027), (-73.7385, 40.5959), (-73.7372, 40.593), (-73.7445, 40.5929), (-73.751, 40.589), (-73.7503, 40.5906), (-73.7523, 40.5918), (-73.7579, 40.5921), (-73.7749, 40.5908), (-73.8068, 40.5846), (-73.8345, 40.5774), (-73.8788, 40.5621), (-73.8962, 40.5574), (-73.9051, 40.5564), (-73.938, 40.5437), (-73.9405, 40.544), (-73.9399, 40.554), (-73.9354, 40.5574), (-73.9316, 40.5575), (-73.9255, 40.5613), (-73.9112, 40.5649), (-73.9058, 40.5625), (-73.8998, 40.5634), (-73.8921, 40.5683), (-73.8824, 40.5682), (-73.8792, 40.5747), (-73.8499, 40.5887), (-73.8345, 40.6072), (-73.833, 40.6283), (-73.8483, 40.6435), (-73.8549, 40.6427), (-73.8561, 40.6492), (-73.8632, 40.6583), (-73.8576, 40.6601), (-73.8584, 40.6635), (-73.8557, 40.6639), (-73.8576, 40.6717), (-73.8604, 40.6713), (-73.8623, 40.6792), (-73.8633, 40.6794), (-73.8641, 40.6824), (-73.866, 40.6819), (-73.8689, 40.6951), (-73.874, 40.6942), (-73.8796, 40.6911), (-73.8845, 40.6867), (-73.8896, 40.6842), (-73.8901, 40.685), (-73.8925, 40.6834), (-73.8942, 40.6853), (-73.8965, 40.6824), (-73.9012, 40.6879), (-73.9018, 40.6908), (-73.9012, 40.6914), (-73.9058, 40.6941), (-73.9043, 40.6957), (-73.9118, 40.6999), (-73.9107, 40.701), (-73.9129, 40.7024), (-73.9118, 40.7034), (-73.9219, 40.7094), (-73.9207, 40.7105), (-73.9222, 40.7129), (-73.924, 40.714), (-73.9243, 40.7156), (-73.9227, 40.7165), (-73.9278, 40.7265), (-73.9291, 40.7277), (-73.9375, 40.7298), (-73.9397, 40.7315), (-73.9422, 40.7357), (-73.9471, 40.7375), (-73.9551, 40.7394), (-73.9625, 40.7368), (-73.9626, 40.739)], [(-73.7724, 40.8595), (-73.7705, 40.8601), (-73.7656, 40.8557), (-73.7689, 40.8517), (-73.7688, 40.8482), (-73.7679, 40.8457), (-73.7698, 40.845), (-73.7716, 40.8472), (-73.7724, 40.8595)], [(-73.7926, 40.8548), (-73.7906, 40.8585), (-73.7888, 40.8584), (-73.7879, 40.8541), (-73.7848, 40.8512), (-73.7822, 40.8467), (-73.7831, 40.8445), (-73.7815, 40.8389), (-73.783, 40.8375), (-73.7842, 40.8371), (-73.7856, 40.838), (-73.7911, 40.8472), (-73.7899, 40.8504), (-73.7926, 40.8548)], [(-73.9338, 40.8822), (-73.9298, 40.8887), (-73.9183, 40.9177), (-73.8594, 40.9004), (-73.8591, 40.9025), (-73.8572, 40.9029), (-73.8574, 40.9046), (-73.8563, 40.9062), (-73.8538, 40.9072), (-73.8549, 40.9082), (-73.8527, 40.9099), (-73.8511, 40.91), (-73.8535, 40.9075), (-73.8515, 40.9066), (-73.8502, 40.9074), (-73.8453, 40.9056), (-73.8444, 40.9042), (-73.8414, 40.9042), (-73.8392, 40.8992), (-73.8397, 40.8972), (-73.8384, 40.8941), (-73.824, 40.8899), (-73.8224, 40.8896), (-73.8232, 40.8912), (-73.7941, 40.8836), (-73.7945, 40.8831), (-73.7937, 40.8823), (-73.7949, 40.8806), (-73.7949, 40.8792), (-73.7937, 40.8787), (-73.7908, 40.8802), (-73.7889, 40.879), (-73.7848, 40.8785), (-73.7834, 40.8718), (-73.786, 40.8695), (-73.7912, 40.8689), (-73.7952, 40.8575), (-73.7988, 40.8542), (-73.7981, 40.8513), (-73.7998, 40.8487), (-73.8014, 40.8488), (-73.8046, 40.8546), (-73.8038, 40.8581), (-73.8044, 40.8616), (-73.806, 40.8618), (-73.8076, 40.8605), (-73.809, 40.8605), (-73.8109, 40.8628), (-73.8154, 40.8646), (-73.818, 40.8636), (-73.8169, 40.8615), (-73.8137, 40.8604), (-73.8126, 40.8587), (-73.8126, 40.8544), (-73.8166, 40.8535), (-73.815, 40.8452), (-73.8167, 40.8439), (-73.8152, 40.8311), (-73.8129, 40.8277), (-73.8142, 40.8259), (-73.8128, 40.8244), (-73.8085, 40.8257), (-73.807, 40.8252), (-73.8045, 40.8185), (-73.7983, 40.8168), (-73.7983, 40.8159), (-73.8034, 40.8115), (-73.8018, 40.8103), (-73.7909, 40.8066), (-73.7902, 40.805), (-73.7937, 40.8035), (-73.7941, 40.8005), (-73.8113, 40.8054), (-73.8174, 40.8058), (-73.8354, 40.8022), (-73.8531, 40.8001), (-73.863, 40.7977), (-73.8702, 40.7909), (-73.8716, 40.7868), (-73.8731, 40.7859), (-73.8783, 40.7854), (-73.8883, 40.787), (-73.8906, 40.7901), (-73.9125, 40.7961), (-73.9189, 40.7989), (-73.923, 40.8024), (-73.9273, 40.8026), (-73.9325, 40.8089), (-73.9323, 40.8195), (-73.9335, 40.8332), (-73.933, 40.8357), (-73.9282, 40.8455), (-73.92, 40.8567), (-73.9098, 40.8683), (-73.9086, 40.8717), (-73.907, 40.8735), (-73.9072, 40.8764), (-73.9095, 40.8789), (-73.9114, 40.8793), (-73.9152, 40.8756), (-73.9198, 40.8766), (-73.9226, 40.8788), (-73.9338, 40.8822)], [(-74.0064, 40.6887), (-73.9985, 40.7003), (-73.9975, 40.6997), (-74.002, 40.6918), (-74.0007, 40.6906), (-74.003, 40.6904), (-74.0046, 40.6882), (-74.0064, 40.6887)], [(-74.0232, 40.7199), (-74.014, 40.7576), (-73.9632, 40.8269), (-73.9528, 40.8511), (-73.9338, 40.8822), (-73.9226, 40.8788), (-73.9198, 40.8766), (-73.9152, 40.8756), (-73.9114, 40.8793), (-73.9095, 40.8789), (-73.9072, 40.8764), (-73.9071, 40.873), (-73.9086, 40.8717), (-73.9098, 40.8683), (-73.92, 40.8567), (-73.9282, 40.8455), (-73.933, 40.8357), (-73.9335, 40.8332), (-73.9323, 40.8195), (-73.9325, 40.8089), (-73.9273, 40.8026), (-73.923, 40.8024), (-73.9189, 40.7989), (-73.9125, 40.7961), (-73.9107, 40.7931), (-73.9103, 40.7907), (-73.9172, 40.7842), (-73.9283, 40.7769), (-73.9299, 40.7762), (-73.9318, 40.7779), (-73.9339, 40.7781), (-73.9364, 40.7769), (-73.9379, 40.7741), (-73.9375, 40.7725), (-73.935, 40.7717), (-73.9364, 40.7695), (-73.9413, 40.7669), (-73.9597, 40.7453), (-73.9626, 40.739), (-73.9623, 40.7329), (-73.9612, 40.7295), (-73.9615, 40.7239), (-73.9676, 40.7165), (-73.9699, 40.7093), (-73.9696, 40.7076), (-73.9703, 40.7073), (-73.9728, 40.7094), (-73.9755, 40.7075), (-73.981, 40.7054), (-73.9865, 40.705), (-73.9915, 40.7056), (-73.9945, 40.7043), (-73.9951, 40.703), (-73.9977, 40.7013), (-73.9964, 40.7034), (-73.9971, 40.7056), (-74.0001, 40.7064), (-74.0127, 40.7005), (-74.0163, 40.7017), (-74.0192, 40.7066), (-74.0171, 40.7166), (-74.0232, 40.7199)], [(-74.0263, 40.6863), (-74.0195, 40.6934), (-74.0155, 40.6934), (-74.0121, 40.6907), (-74.0134, 40.688), (-74.0246, 40.6839), (-74.0263, 40.6848), (-74.0263, 40.6863)], [(-74.0417, 40.6264), (-74.0387, 40.6355), (-74.0334, 40.6439), (-74.0276, 40.6447), (-74.0245, 40.6474), (-74.0244, 40.6504), (-74.0076, 40.6625), (-74.0043, 40.6615), (-74.0, 40.6638), (-74.0023, 40.6675), (-74.0099, 40.6686), (-74.0117, 40.6651), (-74.016, 40.6647), (-74.0178, 40.6657), (-74.0189, 40.6713), (-74.0188, 40.6796), (-74.0082, 40.686), (-74.0064, 40.6887), (-74.0046, 40.6882), (-74.003, 40.6904), (-74.0007, 40.6906), (-74.002, 40.6918), (-73.9975, 40.6997), (-73.9985, 40.7003), (-73.9945, 40.7043), (-73.9915, 40.7056), (-73.9865, 40.705), (-73.9792, 40.7058), (-73.9728, 40.7094), (-73.9703, 40.7073), (-73.9696, 40.7076), (-73.9699, 40.7093), (-73.9676, 40.7165), (-73.9615, 40.7239), (-73.9612, 40.7295), (-73.9627, 40.7364), (-73.9551, 40.7394), (-73.9527, 40.7393), (-73.9422, 40.7357), (-73.9397, 40.7315), (-73.9375, 40.7298), (-73.9291, 40.7277), (-73.9278, 40.7265), (-73.9227, 40.7165), (-73.9243, 40.7156), (-73.924, 40.714), (-73.9222, 40.7129), (-73.9207, 40.7105), (-73.9219, 40.7094), (-73.9118, 40.7034), (-73.9129, 40.7024), (-73.9107, 40.701), (-73.9118, 40.6999), (-73.9043, 40.6957), (-73.9058, 40.6941), (-73.9012, 40.6914), (-73.9018, 40.6908), (-73.9012, 40.6879), (-73.8965, 40.6824), (-73.8942, 40.6853), (-73.8925, 40.6834), (-73.8901, 40.685), (-73.8896, 40.6842), (-73.8845, 40.6867), (-73.8796, 40.6911), (-73.874, 40.6942), (-73.8689, 40.6951), (-73.866, 40.6819), (-73.8641, 40.6824), (-73.8633, 40.6794), (-73.8623, 40.6792), (-73.8604, 40.6713), (-73.8576, 40.6717), (-73.8557, 40.6639), (-73.8584, 40.6635), (-73.8576, 40.6601), (-73.8632, 40.6583), (-73.8561, 40.6492), (-73.8549, 40.6427), (-73.8483, 40.6435), (-73.833, 40.6283), (-73.8345, 40.6072), (-73.8499, 40.5887), (-73.8792, 40.5747), (-73.8835, 40.5789), (-73.8955, 40.578), (-73.8965, 40.5833), (-73.8987, 40.5875), (-73.9004, 40.5881), (-73.9114, 40.5859), (-73.9133, 40.5829), (-73.9158, 40.582), (-73.9227, 40.5835), (-73.9302, 40.5836), (-73.9331, 40.5823), (-73.9313, 40.5767), (-73.932, 40.5758), (-73.9463, 40.5756), (-73.9909, 40.5706), (-74.002, 40.5706), (-74.0029, 40.5723), (-74.0115, 40.5745), (-74.0129, 40.5779), (-74.0109, 40.5806), (-74.006, 40.582), (-74.0007, 40.5812), (-73.9983, 40.5819), (-73.9993, 40.5846), (-73.9959, 40.5883), (-73.9971, 40.5914), (-74.0109, 40.6008), (-74.0201, 40.6034), (-74.0314, 40.6052), (-74.0402, 40.6148), (-74.0417, 40.6264)], [(-74.2556, 40.5079), (-74.2519, 40.5139), (-74.2443, 40.5185), (-74.2425, 40.5183), (-74.2407, 40.5193), (-74.2407, 40.5205), (-74.2429, 40.5212), (-74.2417, 40.5313), (-74.2478, 40.5434), (-74.2283, 40.5554), (-74.2189, 40.5546), (-74.2122, 40.5572), (-74.2037, 40.585), (-74.2041, 40.5893), (-74.1968, 40.597), (-74.1954, 40.6018), (-74.1961, 40.6162), (-74.201, 40.6169), (-74.2018, 40.6195), (-74.2006, 40.6314), (-74.1877, 40.6426), (-74.1815, 40.6446), (-74.178, 40.6426), (-74.1743, 40.6446), (-74.1614, 40.6387), (-74.1544, 40.6372), (-74.1494, 40.6376), (-74.1488, 40.6389), (-74.1424, 40.6395), (-74.1344, 40.6421), (-74.1298, 40.6415), (-74.1275, 40.6399), (-74.1216, 40.6409), (-74.1204, 40.6424), (-74.1068, 40.6459), (-74.1, 40.6454), (-74.0938, 40.6461), (-74.0865, 40.6486), (-74.079, 40.6482), (-74.0715, 40.6428), (-74.0736, 40.6378), (-74.0733, 40.6308), (-74.0719, 40.624), (-74.0641, 40.6169), (-74.0531, 40.6037), (-74.0536, 40.5995), (-74.076, 40.5783), (-74.0927, 40.5656), (-74.105, 40.5545), (-74.1082, 40.5543), (-74.113, 40.548), (-74.1164, 40.548), (-74.1228, 40.5436), (-74.1354, 40.5304), (-74.1372, 40.5301), (-74.1403, 40.5333), (-74.1397, 40.5351), (-74.1348, 40.5352), (-74.1281, 40.5412), (-74.1275, 40.5426), (-74.1295, 40.5454), (-74.1322, 40.5462), (-74.1357, 40.5464), (-74.1384, 40.5451), (-74.1419, 40.5418), (-74.1422, 40.5373), (-74.1487, 40.5345), (-74.157, 40.529), (-74.1696, 40.5233), (-74.172, 40.5233), (-74.178, 40.5196), (-74.1811, 40.5207), (-74.1845, 40.5195), (-74.1948, 40.5101), (-74.1965, 40.5098), (-74.2008, 40.5132), (-74.2089, 40.5115), (-74.2198, 40.5026), (-74.2332, 40.5013), (-74.2467, 40.4961), (-74.2502, 40.4967), (-74.2546, 40.5023), (-74.2556, 40.5079)]]
    BOROUGHS = [('Queens', -73.7942, 40.6767), ('Bronx', -73.8698, 40.8524), ('Manhattan', -73.9497, 40.7919), ('Brooklyn', -73.9395, 40.6543), ('Staten Island', -74.146, 40.5719)]
    # BUILT-DATA-END

    NAMES = [h[0] for h in HOSPITALS]
    LAT = np.array([h[1] for h in HOSPITALS])
    LON = np.array([h[2] for h in HOSPITALS])
    POP = np.array([h[3] for h in HOSPITALS], dtype=float)
    N = len(HOSPITALS)
    SCENARIOS = list(EDGES)

    HOPS = 4  # a patient is passed on at most this many times
    BUDGET = 100.0
    EDGE_COST = 8.0  # one new referral link
    UNIT = 10_000  # patients of extra capacity ...
    UNIT_COST = 4.0  # ... cost this much
    TIME_BUDGET = 20.0  # seconds per city for your function

    # ------------------------------------------------------------ the model
    def simulate(edges, capacity):
        """Everyone goes to the nearest hospital. A hospital treats patients
        until its capacity is used; the rest are split equally among the
        hospitals it refers to. A patient is passed on at most HOPS times; after
        that nobody takes them.

        Returns arrived (patients sent to a hospital by others, taken or not),
        dropped (patients nobody took, by the hospital that gave up last) and
        unserved (their share of the whole population)."""
        out = [[] for _ in range(N)]
        for i, j in edges:
            out[i].append(j)
        served = np.zeros(N)
        carry = POP.copy()
        arrived = np.zeros(N)
        dropped = np.zeros(N)
        waiting, treated = [], []  # per round: patients present, treated so far
        for hop in range(HOPS + 1):
            waiting.append(carry.copy())
            nxt = np.zeros(N)
            for i in range(N):
                if carry[i] <= 0:
                    continue
                take = min(max(capacity[i] - served[i], 0.0), carry[i])
                served[i] += take
                over = carry[i] - take
                if hop < HOPS and out[i]:
                    for j in out[i]:
                        nxt[j] += over / len(out[i])
                else:
                    dropped[i] += over
            treated.append(served.copy())
            arrived += nxt
            carry = nxt
        return types.SimpleNamespace(
            arrived=arrived,
            dropped=dropped,
            unserved=dropped.sum() / POP.sum(),
            waiting=waiting,
            treated=treated,
        )

    PAIRS = [(a, b) for a in range(N) for b in range(N) if a != b]
    ORDER = np.random.default_rng(5).permutation(len(PAIRS))  # the order patients are sent

    def shortest_paths(edges):
        """{(from, to): every shortest referral path}."""
        g = igraph.Graph(n=N, edges=list(edges), directed=True)
        found = {}
        for a in range(N):
            for p in g.get_all_shortest_paths(a, mode="out"):
                if len(p) > 1:
                    found.setdefault((a, p[-1]), []).append(p)
        return found

    def traffic_of(paths, pairs):
        """No capacity limit. Each pair sends one patient along its shortest
        referral path (ties split equally). Counts, for each hospital, the
        patients that pass through it on the way to somewhere else."""
        traffic = np.zeros(N)
        for pair in pairs:
            ps = paths[pair]
            for p in ps:
                for mid in p[1:-1]:
                    traffic[mid] += 1.0 / len(ps)
        return traffic

    CITY = {
        k: types.SimpleNamespace(
            edges=[tuple(e) for e in EDGES[k]], capacity=np.array(CAPACITY[k], dtype=float)
        )
        for k in SCENARIOS
    }
    PATHS = {k: shortest_paths(CITY[k].edges) for k in SCENARIOS}
    TRAFFIC = {k: traffic_of(PATHS[k], PAIRS) for k in SCENARIOS}
    SIM0 = {k: simulate(CITY[k].edges, CITY[k].capacity) for k in SCENARIOS}
    ARRIVED = {k: SIM0[k].arrived for k in SCENARIOS}

    def graph_of(k):
        return igraph.Graph(n=N, edges=list(CITY[k].edges), directed=True)

    def city_of(k):
        """A fresh copy of one city, for your function to read."""
        c = CITY[k]
        return types.SimpleNamespace(
            n=N,
            names=list(NAMES),
            lat=LAT.copy(),
            lon=LON.copy(),
            pop=POP.copy(),
            capacity=c.capacity.copy(),
            edges=list(c.edges),
            graph=igraph.Graph(n=N, edges=list(c.edges), directed=True),
            budget=BUDGET,
            edge_cost=EDGE_COST,
            unit=UNIT,
            unit_cost=UNIT_COST,
        )

    # ------------------------------------------------------------- scoring
    def _ranks(x):
        x = np.asarray(x, dtype=float)
        order = np.argsort(x, kind="stable")
        r = np.empty(len(x))
        r[order] = np.arange(len(x))
        for v in np.unique(x):
            m = x == v
            if m.sum() > 1:
                r[m] = r[m].mean()
        return r

    def spearman(a, b):
        """Rank correlation: 1 when two scores order the hospitals identically,
        0 when they are unrelated, -1 when the order is reversed."""
        ra, rb = _ranks(a), _ranks(b)
        if ra.std() == 0 or rb.std() == 0:
            return 0.0
        return float(np.corrcoef(ra, rb)[0, 1])

    def _vector(v):
        v = np.asarray(v, dtype=float).reshape(-1)
        if v.shape != (N,):
            raise ValueError(f"return one number per hospital ({N}), got {v.shape[0]}")
        if not np.isfinite(v).all():
            raise ValueError("a score is NaN or infinite")
        return v

    def score_scores(fn, truth, arity):
        rows = {}
        for k in SCENARIOS:
            t0 = time.time()
            notes = []
            value = 0.0
            try:
                c = city_of(k)
                args = [c.graph] if arity == 1 else [c.graph, c.pop, c.capacity]
                value = spearman(_vector(fn(*args)), truth[k])
            except Exception as err:  # noqa: BLE001 -- shown to the team
                notes.append(f"{type(err).__name__}: {err}")
            rows[k] = {"value": value, "seconds": time.time() - t0, "notes": notes}
        return rows

    def _proposal(p, c):
        """Turn what propose() returned into (new edges, extra capacity), or
        raise ValueError saying what is wrong with it."""
        if not isinstance(p, dict):
            raise ValueError('return a dict with the keys "edges" and "capacity"')
        have = set(c.edges)
        new, extra = [], np.zeros(N)
        for e in p.get("edges", []):
            i, j = int(e[0]), int(e[1])
            if not (0 <= i < N and 0 <= j < N) or i == j:
                raise ValueError(f"edge {(i, j)} is not a pair of different hospitals")
            if (i, j) in have:
                raise ValueError(f"edge {(i, j)} already exists (or is listed twice)")
            have.add((i, j))
            new.append((i, j))
        for k, v in dict(p.get("capacity", {})).items():
            k, v = int(k), float(v)
            if not 0 <= k < N or not np.isfinite(v) or v < 0:
                raise ValueError(f"capacity {k}: {v} is not a hospital and a number >= 0")
            extra[k] += v
        cost = EDGE_COST * len(new) + UNIT_COST * extra.sum()
        if cost > BUDGET + 1e-9:
            raise ValueError(f"the proposal costs {cost:.1f}, the budget is {BUDGET:.0f}")
        return new, extra * UNIT, cost

    def run_proposal(fn, k):
        t0 = time.time()
        c = city_of(k)
        notes, new, extra, cost = [], [], np.zeros(N), 0.0
        try:
            new, extra, cost = _proposal(fn(c), CITY[k])
        except Exception as err:  # noqa: BLE001 -- shown to the team
            notes.append(f"{type(err).__name__}: {err}  (nothing was applied)")
        sim = simulate(CITY[k].edges + new, CITY[k].capacity + extra)
        return {
            "value": sim.unserved,
            "seconds": time.time() - t0,
            "notes": notes,
            "new": new,
            "extra": extra,
            "cost": cost,
            "sim": sim,
        }

    def score_proposal(fn):
        return {k: run_proposal(fn, k) for k in SCENARIOS}

    def overall(rows):
        return float(np.mean([r["value"] for r in rows.values()]))

    # --------------------------------------------------------- references
    def _walk(edges, seed, hops):
        P = np.zeros((N, N))
        for i, j in edges:
            P[i, j] = 1.0
        P /= P.sum(axis=1, keepdims=True)
        x, total = seed.astype(float), np.zeros(N)
        for _ in range(hops):
            x = (P * x[:, None]).sum(axis=0)
            total += x
        return total

    def ref_closeness(g):
        return np.nan_to_num(np.array(g.closeness(mode="in")))

    def ref_pagerank(g):
        return np.array(g.pagerank())

    def benchmark_1b(g, pop, capacity):
        """Deliberately not named in the notebook. Beating it is the game."""
        return _walk(g.get_edgelist(), np.maximum(pop - capacity, 0.0), HOPS)

    def benchmark_2(c):
        """Deliberately not named in the notebook. Beating it is the game."""
        sim = simulate(c.edges, c.capacity)
        short = np.maximum(c.pop - c.capacity, 0.0)
        spare = np.maximum(c.capacity - c.pop, 0.0)
        have, edges = set(c.edges), []
        for a in np.argsort(-short)[:3]:
            for b in np.argsort(-spare):
                if a != b and (int(a), int(b)) not in have:
                    edges.append((int(a), int(b)))
                    break
        left = BUDGET - EDGE_COST * len(edges)
        want = np.maximum(sim.arrived + c.pop - c.capacity, 0.0)
        share = want / want.sum()
        return {
            "edges": edges,
            "capacity": {i: float(share[i] * left / UNIT_COST) for i in range(N)},
        }

    def random_2(c):
        rng = np.random.default_rng(7)
        have = set(c.edges)
        edges = []
        while len(edges) < 3:
            e = (int(rng.integers(N)), int(rng.integers(N)))
            if e[0] != e[1] and e not in have:
                have.add(e)
                edges.append(e)
        left = BUDGET - EDGE_COST * 3
        picks = rng.choice(N, size=10, replace=False)
        return {"edges": edges, "capacity": {int(i): left / UNIT_COST / 10 for i in picks}}

    def nothing_2(c):
        return {"edges": [], "capacity": {}}

    # ------------------------------------------------------------- drawing
    def _bar_row(label, value, top, tone, fmt, bold=False):
        width = 0 if top <= 0 else max(0.0, min(100.0, 100.0 * value / top))
        weight = "700" if bold else "400"
        return (
            f'<tr><td style="padding:4px 14px 4px 0;font-family:{SANS};'
            f'font-size:14px;color:{INK};font-weight:{weight};white-space:nowrap">'
            f"{label}</td>"
            f'<td style="width:260px;padding:4px 10px 4px 0">'
            f'<div style="background:#efece6;height:12px;border-radius:2px">'
            f'<div style="width:{width:.1f}%;height:12px;background:{tone};'
            f'border-radius:2px"></div></div></td>'
            f'<td style="font-family:{MONO};font-size:14px;color:{INK};'
            f'font-weight:{weight};padding:4px 0">{fmt(value)}</td></tr>'
        )

    def scoreboard(title, lines, caption, fmt):
        """lines: (label, value, tone, bold)."""
        top = max([v for _, v, _, _ in lines] + [1e-9])
        body = "".join(_bar_row(l, v, top, t, fmt, b) for l, v, t, b in lines)
        return mo.Html(
            f'<div style="font-family:{SANS};font-size:13px;color:{MUTED};'
            f'letter-spacing:.06em;text-transform:uppercase;margin:16px 0 4px">'
            f"{title}</div>"
            f'<table style="border-collapse:collapse">{body}</table>'
            f'<div style="font-family:{SANS};font-size:13px;color:{MUTED};'
            f'margin-top:6px">{caption}</div>'
        )

    def table_html(head, rows, highlight=None):
        cells = "".join(
            f'<th style="text-align:{"left" if i < 1 else "right"};'
            f"padding:4px 18px 6px 0;font-family:{SANS};font-size:12px;"
            f'color:{MUTED};font-weight:700">{h}</th>'
            for i, h in enumerate(head)
        )
        body = "".join(
            "<tr>"
            + "".join(
                f'<td style="text-align:{"left" if i < 1 else "right"};'
                f"padding:5px 18px 5px 0;border-top:1px solid {RULE};"
                f'font-family:{MONO if i > 0 else SANS};font-size:14px;'
                f'color:{RUST if i == highlight else INK}">{v}</td>'
                for i, v in enumerate(row)
            )
            + "</tr>"
            for row in rows
        )
        return mo.Html(
            f'<table style="border-collapse:collapse;margin:10px 0">'
            f"<tr>{cells}</tr>{body}</table>"
        )

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">'
            f"{text}</div>"
        )

    def complaints(rows):
        out = [f"<b>city {k}</b>: {'; '.join(r['notes'])}" for k, r in rows.items() if r["notes"]]
        out += [
            f"<b>city {k}</b>: took {r['seconds']:.0f}s, over the {TIME_BUDGET:.0f}s budget"
            for k, r in rows.items()
            if r["seconds"] > TIME_BUDGET
        ]
        return note("<br>".join(out), RUST) if out else mo.Html("")

    def _ramp(t):
        """0 -> pale, 1 -> rust."""
        lo, hi = np.array([239, 233, 223]), np.array([181, 72, 47])
        r, g_, b = (lo + (hi - lo) * float(np.clip(t, 0, 1))).astype(int)
        return f"rgb({r},{g_},{b})"

    _xs = [p[0] for ring in BASEMAP for p in ring] + list(LON)
    _ys = [p[1] for ring in BASEMAP for p in ring] + list(LAT)
    _KY = np.cos(np.radians(np.mean(_ys)))
    _W, _H = (max(_xs) - min(_xs)) * _KY, max(_ys) - min(_ys)

    def _shade(values, scale):
        v = np.asarray(values, dtype=float)
        t = np.zeros(N)
        if scale == "linear":
            if v.max() > 0:
                t = np.clip(v, 0, None) / v.max()
        elif scale == "rank0":  # zero stays pale; the rest by rank
            pos = v > 0
            if pos.any():
                t[pos] = 0.2 + 0.8 * _ranks(v[pos]) / max(pos.sum() - 1, 1)
        else:
            t = _ranks(v) / max(N - 1, 1)
        return t

    def svg_map(
        values,
        k,
        size=560,
        scale="rank",
        extra_edges=(),
        rings=None,
        path=(),
        fmt="{:,.0f}",
    ):
        """New York City. One circle per hospital: area ~ the people it serves,
        fill ~ `values`. Thin lines are referral links. Blue lines are links
        you added (or the path of the last patient sent); blue rings mark the
        hospitals in `rings`."""
        pad = 12
        s = (size - 2 * pad) / max(_W, _H)

        def px(lon):
            return pad + (np.asarray(lon) - min(_xs)) * _KY * s

        def py(lat):
            return pad + (max(_ys) - np.asarray(lat)) * s

        sx, sy = px(LON), py(LAT)
        land = "".join(
            '<polygon points="'
            + " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in ring)
            + f'" fill="#f4f0e8" stroke="#cfc8b9" stroke-width="0.8"/>'
            for ring in BASEMAP
        )
        names = "".join(
            f'<text x="{px(x):.1f}" y="{py(y):.1f}" text-anchor="middle" '
            f'font-family="{SANS}" font-size="11" letter-spacing="1.5" fill="#8a8272" '
            f'stroke="#f4f0e8" stroke-width="3" paint-order="stroke" '
            f'pointer-events="none">{n.upper()}</text>'
            for n, x, y in BOROUGHS
        )
        t = _shade(values, scale)
        rad = 3.5 + 9.0 * np.sqrt(POP / POP.max())
        links = "".join(
            f'<line x1="{sx[i]:.1f}" y1="{sy[i]:.1f}" x2="{sx[j]:.1f}" y2="{sy[j]:.1f}" '
            f'stroke="#8f8a7e" stroke-opacity="0.35" stroke-width="0.6"/>'
            for i, j in CITY[k].edges
        )
        added = "".join(
            f'<line x1="{sx[i]:.1f}" y1="{sy[i]:.1f}" x2="{sx[j]:.1f}" y2="{sy[j]:.1f}" '
            f'stroke="{BLUE}" stroke-width="2"/>'
            for i, j in list(extra_edges) + list(zip(path[:-1], path[1:]))
        )
        ring_svg = ""
        if rings is not None:
            ring_svg = "".join(
                f'<circle cx="{sx[i]:.1f}" cy="{sy[i]:.1f}" r="{rad[i] + 3.5:.1f}" '
                f'fill="none" stroke="{BLUE}" stroke-width="2"/>'
                for i in range(N)
                if rings[i]
            )
        dots = "".join(
            f'<circle cx="{sx[i]:.1f}" cy="{sy[i]:.1f}" r="{rad[i]:.1f}" '
            f'fill="{_ramp(t[i])}" stroke="{INK}" stroke-width="1">'
            f"<title>#{i} {NAMES[i]} · {fmt.format(values[i])}</title></circle>"
            for i in range(N)
        )
        w, h = pad * 2 + _W * s, pad * 2 + _H * s
        return mo.Html(
            f'<svg width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'style="background:#e9eef1;border:1px solid {RULE};border-radius:4px">'
            f"{land}{links}{added}{ring_svg}{dots}{names}</svg>"
        )

    def _short(name, width=28):
        return name if len(name) <= width else name[: width - 1] + "…"

    def top_table(values, label, how=6, fmt="{:,.0f}"):
        order = np.argsort(-np.asarray(values))[:how]
        return table_html(
            ["hospital", "#", label],
            [[_short(NAMES[i]), str(i), fmt.format(values[i])] for i in order],
        )


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Mini project m06

    ## New York's hospitals

    There are 61 hospitals and 8.8 million people. Everyone goes to the nearest hospital. Circle area represents the people served. Lines are **referral links**: a hospital may send patients to linked hospitals.

    Locations and populations are real. Links and capacities are simulated. Cities **A** and **B** have the same hospitals, but different links and capacities. Your answers must work on both.
    """)
    return


@app.cell(hide_code=True)
def _():
    explore_city = mo.ui.radio(options=SCENARIOS, value=SCENARIOS[0], label="city")
    explore_color = mo.ui.radio(
        options=["people served", "spare capacity"], value="people served", label="colour"
    )
    mo.hstack([explore_city, explore_color], justify="start", gap=2)
    return explore_city, explore_color


@app.cell(hide_code=True)
def _(explore_city, explore_color):
    _k = explore_city.value
    if explore_color.value == "people served":
        _v, _lab = POP, "people"
    else:
        _v, _lab = CITY[_k].capacity - POP, "capacity − people"
    mo.hstack([svg_map(_v, _k), top_table(_v, _lab)], justify="start", gap=2, wrap=True)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Question 1. Where are the bottlenecks?

    ## 1a. No capacity limit

    Every hospital sends one patient to every other hospital along the shortest referral path. A hospital's **traffic** is the number of patients passing through it.

    Send the patients and watch. Then write `bottleneck_no_capacity(g)`. Return one number per hospital. Higher values must indicate more traffic. The score is the rank correlation with the true traffic (1 = same order).
    """)
    return


@app.cell(hide_code=True)
def _():
    sim1a_city = mo.ui.radio(options=SCENARIOS, value=SCENARIOS[0], label="city")
    sim1a_sent = mo.ui.slider(
        0, len(PAIRS), step=N - 1, value=10 * (N - 1), label="patients sent", show_value=True
    )
    mo.hstack([sim1a_city, sim1a_sent], justify="start", gap=2)
    return sim1a_city, sim1a_sent


@app.cell(hide_code=True)
def _(sim1a_city, sim1a_sent):
    _k, _m = sim1a_city.value, sim1a_sent.value
    _pairs = [PAIRS[i] for i in ORDER[:_m]]
    _traffic = traffic_of(PATHS[_k], _pairs)
    _last = PATHS[_k][_pairs[-1]][0] if _pairs else []
    mo.hstack(
        [
            svg_map(_traffic, _k, scale="rank0", path=_last),
            mo.vstack(
                [
                    note("Blue: the last patient's path. Darker: more patients passing through."),
                    top_table(_traffic, "passed through", fmt="{:,.1f}"),
                ]
            ),
        ],
        justify="start",
        gap=2,
        wrap=True,
    )
    return


@app.function
# Q1a — return one number per hospital: higher = more patients pass through.
def bottleneck_no_capacity(g):
    """Starting version: the number of hospitals that refer to this one."""
    return np.array(g.indegree())


@app.cell(hide_code=True)
def _():
    _mine = score_scores(bottleneck_no_capacity, TRAFFIC, 1)
    _rows = {
        "in-degree (the starting code)": score_scores(lambda g: np.array(g.indegree()), TRAFFIC, 1),
        "closeness": score_scores(ref_closeness, TRAFFIC, 1),
        "PageRank": score_scores(ref_pagerank, TRAFFIC, 1),
    }
    _lines = [(n, overall(r), MUTED, False) for n, r in _rows.items()] + [
        ("your team", overall(_mine), RUST, True)
    ]
    mo.vstack(
        [
            scoreboard(
                "1a · traffic",
                _lines,
                "rank correlation with the true traffic, mean of A and B. higher is better.",
                lambda v: f"{v:.2f}",
            ),
            complaints(_mine),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1b. With capacity limits

    Hospitals have capacities, and people fall ill:

    1. Everyone goes to the nearest hospital.
    2. A hospital treats patients until full. The rest are **split equally among the hospitals it links to**.
    3. Those hospitals do the same.
    4. A patient is passed on at most 4 times, then goes unserved.

    A hospital's **load** is the number of referred patients sent to it.

    Run the simulation. Write `bottleneck_with_capacity(g, pop, capacity)`: one number per hospital, higher = more load. The starting code is your 1a answer.
    """)
    return


@app.cell(hide_code=True)
def _():
    sim1b_city = mo.ui.radio(options=SCENARIOS, value=SCENARIOS[0], label="city")
    sim1b_scale = mo.ui.slider(
        0.8, 1.4, step=0.05, value=1.0, label="capacity × (1 = as scored)", show_value=True
    )
    sim1b_round = mo.ui.slider(0, HOPS, step=1, value=0, label="round", show_value=True)
    mo.hstack([sim1b_city, sim1b_scale, sim1b_round], justify="start", gap=2)
    return sim1b_city, sim1b_round, sim1b_scale


@app.cell(hide_code=True)
def _(sim1b_city, sim1b_round, sim1b_scale):
    _k, _r = sim1b_city.value, sim1b_round.value
    _cap = CITY[_k].capacity * sim1b_scale.value
    _sim = simulate(CITY[_k].edges, _cap)
    _full = _sim.treated[_r] >= _cap - 1e-6
    _received = sum(_sim.waiting[1 : _r + 1]) if _r else np.zeros(N)
    mo.hstack(
        [
            svg_map(_sim.waiting[_r], _k, scale="linear", rings=_full),
            mo.vstack(
                [
                    note(
                        "Darker: patients at this hospital in this round. "
                        "Blue ring: full. Round 0 is the catchments."
                    ),
                    note(f"At the end <b>{100 * _sim.unserved:.1f}%</b> of the people are unserved."),
                    top_table(_received, "referrals received so far")
                    if _r
                    else note("Move the round slider to pass the patients on."),
                ]
            ),
        ],
        justify="start",
        gap=2,
        wrap=True,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ 1. Why does your score fit?

    3 to 6 short sentences: what the simulation does that your 1a answer ignores, and how your score captures it. This is graded; the agent codes from it.
    """)
    return


@app.cell
def _():
    # ✍️ 1 — describe your score for 1b in plain English.
    PLAN_1B = """
    ...
    """
    return


@app.function
# Q1b — return one number per hospital: higher = more referred patients arrive.
def bottleneck_with_capacity(g, pop, capacity):
    """Starting version: the answer to 1a, betweenness, ignoring pop and
    capacity."""
    return np.array(g.betweenness(directed=True))


@app.cell(hide_code=True)
def _():
    _mine = score_scores(bottleneck_with_capacity, ARRIVED, 3)
    _lines = [
        (
            "betweenness (the starting code)",
            overall(score_scores(lambda g, p, c: np.array(g.betweenness(directed=True)), ARRIVED, 3)),
            MUTED,
            False,
        ),
        ("benchmark", overall(score_scores(benchmark_1b, ARRIVED, 3)), BLUE, False),
        ("your team", overall(_mine), RUST, True),
    ]
    mo.vstack(
        [
            scoreboard(
                "1b · load",
                _lines,
                "rank correlation with the simulated load, mean of A and B. higher is better.",
                lambda v: f"{v:.2f}",
            ),
            complaints(_mine),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Question 2. Spend 100

    - A new referral link costs **8**.
    - **10,000 patients** of extra capacity at a hospital costs **4** (fractions allowed).
    - You cannot add hospitals or remove links.

    Write `propose(city)`. It returns:

    ```python
    {"edges": [(3, 41), (17, 5)],      # links 3→41 and 17→5
     "capacity": {12: 6.0, 30: 2.5}}   # hospital 12 gets +60,000, hospital 30 gets +25,000
    ```

    ```
    city.names, city.lat, city.lon     per hospital
    city.pop, city.capacity            per hospital (arrays)
    city.edges                         [(from, to), ...]
    city.graph                         the same, as a directed igraph.Graph
    city.budget, city.edge_cost, city.unit, city.unit_cost
    ```

    Score: share of people unserved by the 1b simulation, averaged over A and B. Lower is better.

    A proposal is rejected whole if it exceeds budget, repeats a link, or names a missing hospital.

    `propose(city)` receives one city at a time. It must work on any city of this kind.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ 2. Why there?

    3 to 6 short sentences: where the money goes, and why you split it between links and capacity this way. This is graded; the agent codes from it.
    """)
    return


@app.cell
def _():
    # ✍️ 2 — describe your proposal in plain English.
    PLAN_2 = """
    ...
    """
    return


@app.function
# Q2 — spend the budget.
def propose(city):
    """Starting version: split the whole budget evenly among the five hospitals
    with the largest catchments, as extra capacity. No new links."""
    biggest = np.argsort(-city.pop)[:5]
    each = city.budget / city.unit_cost / 5
    return {"edges": [], "capacity": {int(i): each for i in biggest}}


@app.cell(hide_code=True)
def _():
    _mine = score_proposal(propose)
    _ref = {
        name: overall(score_proposal(fn))
        for name, fn in [
            ("do nothing", nothing_2),
            ("spend at random", random_2),
            ("benchmark", benchmark_2),
        ]
    }
    _lines = [
        ("do nothing", _ref["do nothing"], MUTED, False),
        ("spend at random", _ref["spend at random"], MUTED, False),
        ("benchmark", _ref["benchmark"], BLUE, False),
        ("your team", overall(_mine), RUST, True),
    ]
    mo.vstack(
        [
            scoreboard(
                "2 · people left unserved",
                _lines,
                "mean of A and B. lower is better.",
                lambda v: f"{100 * v:.2f}%",
            ),
            table_html(
                ["city", "unserved", "links", "capacity added", "spent"],
                [
                    [
                        f"city {k}",
                        f"{100 * r['value']:.2f}%",
                        str(len(r["new"])),
                        f"{r['extra'].sum():,.0f}",
                        f"{r['cost']:.0f} / {BUDGET:.0f}",
                    ]
                    for k, r in _mine.items()
                ],
                highlight=1,
            ),
            complaints(_mine),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    watch_city = mo.ui.radio(options=SCENARIOS, value=SCENARIOS[0], label="city")
    watch_when = mo.ui.radio(options=["before", "after your proposal"], value="after your proposal", label="")
    mo.hstack([watch_city, watch_when], justify="start", gap=2)
    return watch_city, watch_when


@app.cell(hide_code=True)
def _(watch_city, watch_when):
    _k = watch_city.value
    if watch_when.value == "before":
        _sim, _new, _rings = SIM0[_k], (), None
    else:
        _r = run_proposal(propose, _k)
        _sim, _new, _rings = _r["sim"], _r["new"], _r["extra"] > 0
    mo.hstack(
        [
            svg_map(_sim.dropped, _k, scale="rank0", extra_edges=_new, rings=_rings),
            mo.vstack(
                [
                    note("Darker: more people left unserved. Blue: your links and the hospitals you enlarged."),
                    note(f"<b>{100 * _sim.unserved:.2f}%</b> unserved."),
                    top_table(_sim.dropped, "people unserved"),
                ]
            ),
        ],
        justify="start",
        gap=2,
        wrap=True,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## Submit

    One submission per team.
    Click Share, then `🔗 Copy Notebook URL`.
    Send the link through **<https://go.skojaku.com/m06mini>**.

    The two ✍️ texts count more than the scores.
    A clear design that loses to the benchmark is a good answer.
    A high score with a vague text is not.
    """)
    return


if __name__ == "__main__":
    app.run()
