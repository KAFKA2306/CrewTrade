import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from chronos import ChronosPipeline
def main():
    print("Initializing Chronos Pipeline...")
    model_name = "amazon/chronos-t5-tiny"
    device_map = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device_map}")
    pipeline = ChronosPipeline.from_pretrained(
        model_name,
        device_map=device_map,
        torch_dtype=torch.bfloat16 if device_map == "cuda" else torch.float32,
    )
    print(f"Model {model_name} loaded successfully.")
    print("Generating sample data...")
    t = np.linspace(0, 20, 100)
    data = np.sin(t) + np.random.normal(0, 0.1, 100)
    context = torch.tensor(data)
    prediction_length = 20
    print(f"Forecasting {prediction_length} steps ahead...")
    forecast = pipeline.predict(
        context,
        prediction_length=prediction_length,
        num_samples=20,
    )
    print("Forecast shape:", forecast.shape)
    low, median, high = np.quantile(forecast[0].numpy(), [0.1, 0.5, 0.9], axis=0)
    print("Forecast validation:")
    print(f"Median of last predicted point: {median[-1]:.4f}")
    try:
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 7))
        fig.patch.set_facecolor('
        ax.set_facecolor('
        color_primary = '
        color_accent = '
        color_history = '
        ax.plot(range(len(data)), data, color=color_history, alpha=0.8, linewidth=1.5, label="Historical Data")
        ax.plot(range(len(data), len(data) + prediction_length), median, color=color_accent, linewidth=2, label="Serendie Forecast (Median)")
        ax.fill_between(
            range(len(data), len(data) + prediction_length), 
            low, 
            high, 
            color=color_primary, 
            alpha=0.25, 
            label="Confidence Interval (80%)"
        )
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(color='
        plt.legend(frameon=False)
        plt.title(f"Forecasting Engine: Chronos ({model_name})", fontsize=14, loc='left', pad=20, color='white', fontweight='bold')
        plt.xlabel("Time Step", alpha=0.7)
        plt.ylabel("Value", alpha=0.7)
        output_file = "chronos_test_plot.png"
        plt.tight_layout()
        plt.savefig(output_file, facecolor='
        print(f"Plot saved to {output_file} with Integrated Tone standard.")
    except Exception as e:
        print(f"Could not save plot: {e}")
    print("Success! Chronos-2 is working.")
if __name__ == "__main__":
    main()
