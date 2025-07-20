import streamlit as st
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Load Sheliak Timewave data (normalized 0 = high novelty, 100 = low novelty)
raw_wave = np.array([0, 0, 0, 0, 0, 0, 2, 3, 2, 2, 2, 8, 5, 3, 1, 3, 2, 10, 9, 4, 9, 6, 16, 14, 10, 8, 12, 9, 9, 11, 9, 9, 8, 23, 29, 28, 18, 18, 20, 12, 12, 9, 31, 23, 16, 30, 24, 36, 22, 23, 18, 42, 43, 47, 30, 32, 29, 26, 26, 26, 20, 21, 21, 15, 15, 15, 69, 69, 69, 63, 65, 66, 44, 44, 44, 26, 29, 27, 19, 19, 20, 27, 32, 31, 14, 16, 14, 26, 13, 23, 33, 30, 26, 26, 24, 22, 28, 25, 19, 11, 12, 16, 80, 78, 72, 68, 82, 74, 42, 38, 40, 38, 43, 44, 27, 29, 28, 34, 36, 38, 11, 11, 11, 6, 5, 6, 12, 12, 12, 18, 18, 18, 27, 27, 29, 54, 53, 53, 23, 29, 26, 56, 58, 60, 38, 36, 41, 69, 60, 66, 31, 29, 16, 14, 18, 15, 38, 44, 42, 52, 47, 50, 44, 43, 42, 36, 34, 36, 27, 24, 22, 28, 27, 23, 33, 45, 42, 25, 34, 30, 22, 22, 24, 23, 20, 20, 20, 20, 19, 18, 18, 18, 24, 24, 24, 24, 24, 24, 6, 5, 4, 4, 4, 4, 31, 29, 31, 33, 28, 40, 33, 24, 33, 30, 40, 38, 28, 26, 30, 27, 27, 29, 27, 27, 26, 23, 23, 26, 36, 32, 38, 30, 24, 23, 31, 25, 24, 30, 24, 36, 28, 29, 24, 20, 19, 19, 18, 20, 17, 40, 40, 42, 68, 69, 69, 51, 51, 51, 33, 33, 33, 33, 33, 34, 52, 52, 52, 16, 23, 25, 37, 39, 34, 37, 30, 21, 18, 24, 14, 12, 13, 7, 69, 66, 62, 62, 60, 58, 32, 29, 29, 37, 36, 32, 28, 30, 30, 36, 34, 40, 28, 36, 30, 30, 27, 16, 19, 17, 16, 22, 24, 26, 17, 17, 17, 8, 7, 6, 60, 60, 60, 36, 36, 36, 27, 27, 29, 54, 53, 53, 35, 35, 38, 30, 28, 28, 28, 40, 33, 31, 26, 28, 31, 29, 16, 16, 18, 21, 18, 20, 18, 28, 23, 26, 26, 25, 24, 30, 28, 30, 15, 12, 10, 16, 15, 11, 7, 15, 12, 11, 6, 8, 4, 4, 6, 5, 2, 2, 2, 2, 1, 0, 0, 0])  # Omitted for brevity - use the full list in actual file

# Normalize wave from 0 (high novelty) to 100 (low novelty)
wave = 100 - (raw_wave - np.min(raw_wave)) / (np.max(raw_wave) - np.min(raw_wave)) * 100

# Helper: Calculate novelty value
def novelty_score(birth_date, target_date):
    lifespan_days = int(71.822 * 365.25)
    days_passed = (target_date - birth_date).days
    index = int((days_passed / lifespan_days) * (len(wave) - 1))
    index = max(0, min(index, len(wave) - 1))
    return wave[index]

# Streamlit UI
st.title("Sheliak Timewave Novelty Calculator")
st.markdown("This calculator computes your novelty value based on a 71.822-year personal Timewave cycle.")

birth_date = st.date_input("Enter your birth date:", datetime.date(2000, 1, 1))
target_date = st.date_input("Select a date to check novelty:", datetime.date.today())

if birth_date >= target_date:
    st.warning("Target date must be after birth date.")
else:
    score = novelty_score(birth_date, target_date)
    st.metric(label="Novelty Score (0 = High Novelty, 100 = Low Novelty)", value=f"{score:.2f}")

    # Plot full wave for the user
    days = [birth_date + datetime.timedelta(days=int(i * 365.25 * 71.822 / len(wave))) for i in range(len(wave))]
    plt.figure(figsize=(10, 4))
    plt.plot(days, wave, label="Novelty Curve")
    plt.axvline(target_date, color='red', linestyle='--', label='Selected Date')
    plt.xlabel("Date")
    plt.ylabel("Novelty (0 = High)")
    plt.title("Personal Timewave Over Lifetime")
    plt.legend()
    st.pyplot(plt.gcf())
