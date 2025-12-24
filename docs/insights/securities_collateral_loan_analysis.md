# 有価証券担保ローンを活用した動的ポートフォリオ最適化：IS/OOSパフォーマンス乖離と市場適応性に関する実証分析

**Dynamic Portfolio Optimization under Securities Collateral Loan Constraints: An Empirical Analysis of In-Sample vs. Out-of-Sample Performance Degradation**

**Date**: 2025/12/24

## 1. Abstract
本稿では、LTV (Loan-to-Value) 制約下におけるMean-Variance最適化モデルの実効性を検証するため、最適化計算上の理論値「In-Sample (IS) Performance」と、リバランス後の実績値「Out-of-Sample (OOS) Performance」の乖離（Degradation）を分析した。
2021年から2025年の分析において、本モデルは平均して年次40-50%のTurnoverを伴う高い適応性を示したが、パフォーマンスの安定性には顕著なバラつきが確認された。特に**2024年にはIS Sharpe 1.44に対しOOS Sharpe -0.21と深刻な劣化（Degradation: -1.66）**を記録し、過学習的傾向が見られた。一方で**2025年にはOOS Sharpe 6.13（Alpha +5.14）**という異例の好成績を収めた。この極端な二面性は、市場レジームの変化に対するモデルの感応度（Sensitivity）が極めて高く、安定的なアルファの源泉というよりは、特定局面における「ホームラン」を狙う性質が強いことを示唆している。

## 2. Methodology: IS/OOS Comparison
本分析では、単純なリターン比較ではなく、リスク調整後リターン（Sharpe Ratio）の比較を通じて、最適化の効用と堅牢性を評価する。

*   **In-Sample (IS) Sharpe**: 最適化に使用した過去データ区間における理論シャープレシオ（期待値）。
*   **Out-of-Sample (OOS) Sharpe**: リバランス後、次期リバランスまでの保有期間における実績シャープレシオ。
*   **Degradation**: OOS Sharpe - IS Sharpe。負の値が大きいほど、モデルが過去データに過剰適合（Overfitting）し、実運用でワークしなかったことを示す。

## 3. Performance Analysis

### Table 1: In-Sample vs. Out-of-Sample Sharpe Ratio Degradation
| Year | IS Sharpe (Exp) | OOS Return | OOS Vol | **OOS Sharpe (Real)** | **Degradation** | Evaluation |
|---|---|---|---|---|---|---|
| 2021 | 0.752 | 4.87% | 12.05% | **0.404** | -0.348 | Moderate Decay |
| 2022 | 0.837 | 13.73% | 9.70% | **1.415** | +0.578 | Robust |
| 2023 | 1.045 | 18.25% | 8.11% | **2.250** | +1.205 | Superior |
| 2024 | **1.443** | -2.73% | 12.77% | **-0.214** | **-1.657** | **Failure (Overfitting)** |
| 2025 | 0.986 | 40.73% | 6.65% | **6.125** | **+5.139** | **Outlier Success** |

### Discussion on Stability
*   **2024 Analysis (The Trap of Optimization)**: 2024年はIS Sharpeが1.443と過去最高水準であり、モデルは「非常に効率的なポートフォリオが見つかった」と判定していた。しかしOOSではSharpe -0.214（マイナス）へ転落した。これは典型的な「最適化の罠（過去データへの過剰適合）」であり、過去の低ボラティリティ・低相関が将来も続くと過信した結果、市場の反転（コリレーションの崩壊）に巻き込まれたことを意味する。
*   **2025 Analysis (Correction or Luck?)**: 2025年は逆に、IS Sharpe 0.986と期待値は平凡であったが、OOSでは6.125という異常値に近い高パフォーマンスを記録した。これはTurnover 89%（後述）による抜本的なリスク回避（債券・Goldの放棄）が、結果として市場の新たなトレンド（JGB/REIT選好）と完璧に合致したためである。これを「モデルの学習効果」と呼ぶか「偶然の産物」と呼ぶかは慎重な判断が必要だが、少なくとも「静的なバイ・アンド・ホールド」では不可能な挙動である。

## 4. Portfolio Turnover Dynamics

### Table 2: Turnover and Structural Shifts
| Era | Turnover | Key Action |
|---|---|---|
| **Early Phase (2021-2023)** | ~48% | 分散化とインフレ対応への段階的シフト。 |
| **The Failure (2024)** | 36% | 新興国債券(+11%)を追加するも、既存ポジションが機能せず。 |
| **The Regime Shift (2025)** | **89%** | **全ポジションの総入替**。<br>Sell: 外国債券/Gold (全売却)<br>Buy: **JGBs [21%], J-REITs [~24%]** |

2024年の失敗を受け、2025年にはポートフォリオを白紙化（Turnover 89%）し、ボラティリティが高まった外国資産を切り捨て、相対的に安定した国内資産へ回帰した。この「逃げ足の速さ」こそが、2025年の高OOS Sharpeを実現した主因である。

## 5. Conclusion
1.  **予測能力の限界**: IS Sharpeが高いからといって、OOSパフォーマンスが保証されるわけではない（2024年の事例）。最適化スコアを絶対視することは危険である。
2.  **市場適応の有効性**: 一方で、市場環境の変化に応じて（たとえコストを払ってでも）大胆にポジションを変える能力（2025年の事例）は、致命的なドローダウンを防ぎ、市場平均を上回るリターンを得るために有効に機能した。
3.  **不安定性の受容**: 本システムは「安定的にコツコツ稼ぐ」タイプではなく、「相場環境にハマれば爆発的に稼ぐが、外すときは大きく外す」というアクティブ運用の特性を色濃く持っている。LTV制約がある以上、このボラティリティは管理すべきリスクであり、今後もOOS Sharpeのモニタリングが不可欠である。

---
*Note: Forward metrics for 2025 are annualized based on the period 2025/06/02 - 2025/10/31.*
