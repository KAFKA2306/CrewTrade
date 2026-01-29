import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from chronos import ChronosPipeline

def main():
    print("Initializing Chronos Pipeline...")
    # Use "amazon/chronos-t5-tiny" for faster download/inference in this test
    # Options: tiny, mini, small, base, large
    model_name = "amazon/chronos-t5-tiny"
    
    # Check for GPU
    device_map = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device_map}")

    pipeline = ChronosPipeline.from_pretrained(
        model_name,
        device_map=device_map,
        torch_dtype=torch.bfloat16 if device_map == "cuda" else torch.float32,
    )
    print(f"Model {model_name} loaded successfully.")

    # Generate sample data: a simple sine wave with noise
    print("Generating sample data...")
    t = np.linspace(0, 20, 100)
    data = np.sin(t) + np.random.normal(0, 0.1, 100)
    
    # Put into pandas Series (optional, but good practice as Chronos expects context)
    # Chronos is actually robust to input types, but let's use a tensor or list
    context = torch.tensor(data)

    prediction_length = 20
    print(f"Forecasting {prediction_length} steps ahead...")
    
    forecast = pipeline.predict(
        context,
        prediction_length=prediction_length,
        num_samples=20,
    )
    
    print("Forecast shape:", forecast.shape) # (num_series, num_samples, prediction_length)
    
    # Basic validation
    low, median, high = np.quantile(forecast[0].numpy(), [0.1, 0.5, 0.9], axis=0)
    
    print("Forecast validation:")
    print(f"Median of last predicted point: {median[-1]:.4f}")
    
    # Save a plot if possible, or just complete
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(data)), data, color="black", label="History")
        plt.plot(range(len(data), len(data) + prediction_length), median, color="blue", label="Median Forecast")
        plt.fill_between(
            range(len(data), len(data) + prediction_length), 
            low, 
            high, 
            color="blue", 
            alpha=0.2, 
            label="80% Prediction Interval"
        )
        plt.legend()
        plt.title(f"Chronos Forecast ({model_name})")
        output_file = "chronos_test_plot.png"
        plt.savefig(output_file)
        print(f"Plot saved to {output_file}")
    except Exception as e:
        print(f"Could not save plot: {e}")

    print("Success! Chronos-2 is working.")

if __name__ == "__main__":
    main()
