from pathlib import Path
from typing import Any
import sys
def get_kronos_forecast(
    df: Any,
    x_timestamp: Any,
    y_timestamp: Any,
    pred_len: int = 120,
    temp: float = 1.0,
    top_p: float = 0.9,
    sample_count: int = 1,
) -> Any:
    """
    Generates a forecast using the Kronos foundation model.
    Lazy-loads the model/tokenizer on first use.
    """
    try:
        from model import Kronos, KronosPredictor, KronosTokenizer
    except ImportError:
        project_root = Path(__file__).resolve().parent.parent.parent
        kronos_path = project_root / "Kronos"
        if str(kronos_path) not in sys.path:
            sys.path.append(str(kronos_path))
        try:
            from model import Kronos, KronosPredictor, KronosTokenizer
        except ImportError as e:
            raise ImportError(
                "Could not import Kronos. Ensure 'Kronos/' directory is in project root."
            ) from e
    tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
    model = Kronos.from_pretrained("NeoQuasar/Kronos-small")
    predictor = KronosPredictor(model, tokenizer, max_context=512)
    return predictor.predict(
        df=df,
        x_timestamp=x_timestamp,
        y_timestamp=y_timestamp,
        pred_len=pred_len,
        T=temp,
        top_p=top_p,
        sample_count=sample_count,
    )
