"""
SME Risk Intelligence — Backend Training Script
=================================================
يُستخدم لإعادة تدريب pipeline.pkl الخاص بالـ backend (مستقل تمامًا عن أي
pipeline قديم مبني على utils.helper من مشروع Streamlit).

التشغيل:
    python -m app.ml.train_pipeline --data-path Data/SMEs_Data.csv
"""

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler

from app.ml.feature_engineering import SMEFeatureEngineer

TARGET_COLUMN = "risk_sharp"


def load_data(data_path: Path) -> pd.DataFrame:
    df = pd.read_csv(data_path)
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    return df


def build_pipeline() -> Pipeline:
    preprocessor = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", RobustScaler()),
        ]
    )

    base_classifier = HistGradientBoostingClassifier(
        max_iter=300,
        learning_rate=0.15,
        max_depth=3,
        min_samples_leaf=30,
        class_weight="balanced",
        random_state=42,
    )

    return Pipeline(
        [
            ("feat_eng", SMEFeatureEngineer()),
            ("preprocessor", preprocessor),
            (
                "classifier",
                CalibratedClassifierCV(
                    estimator=clone(base_classifier),
                    method="isotonic",
                    cv=5,
                ),
            ),
        ]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path",
        type=str,
        default="Data/SMEs_Data.csv",
        help="Path to training CSV file",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory to save pipeline.pkl and metrics json",
    )
    args = parser.parse_args()

    data_path = Path(args.data_path)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  SME Risk Intelligence — Backend Model Training")
    print("=" * 60)

    df = load_data(data_path)
    print(f"[OK] Data loaded: {df.shape[0]:,} rows x {df.shape[1]} columns")

    features = [c for c in df.columns if c != TARGET_COLUMN]
    X = df[features]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )
    print(f"[OK] Train: {len(X_train):,} | Test: {len(X_test):,}")

    pipeline = build_pipeline()
    print("[RUN] Fitting calibrated pipeline...")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    metrics = {
        "test_accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "test_precision": round(precision_score(y_test, y_pred) * 100, 2),
        "test_recall": round(recall_score(y_test, y_pred) * 100, 2),
        "test_f1": round(f1_score(y_test, y_pred) * 100, 2),
        "test_roc_auc": round(roc_auc_score(y_test, y_proba) * 100, 2),
        "features_used": features,
    }

    print("=" * 60)
    print("  FINAL METRICS")
    print("=" * 60)
    for key, value in metrics.items():
        if key != "features_used":
            print(f"  {key}: {value}")
    print(classification_report(y_test, y_pred))

    joblib.dump(pipeline, output_dir / "pipeline.pkl")
    print(f"[OK] pipeline.pkl saved to {output_dir / 'pipeline.pkl'}")

    with open(output_dir / "model_metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[OK] model_metrics.json saved to {output_dir / 'model_metrics.json'}")


if __name__ == "__main__":
    main()