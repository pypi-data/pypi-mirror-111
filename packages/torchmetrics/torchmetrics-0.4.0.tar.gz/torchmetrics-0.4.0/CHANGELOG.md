# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Note: we move fast, but still we preserve 0.1 version (one feature release) back compatibility.**

## [0.4.0] - 2021-06-29

### Added

- Added Cosine Similarity Metric ([#305](https://github.com/PyTorchLightning/metrics/pull/305))
- Added Specificity metric ([#210](https://github.com/PyTorchLightning/metrics/pull/210))
- Added `add_metrics` method to `MetricCollection` for adding additional metrics after initialization ([#221](https://github.com/PyTorchLightning/metrics/pull/221))
- Added pre-gather reduction in the case of `dist_reduce_fx="cat"` to reduce communication cost ([#217](https://github.com/PyTorchLightning/metrics/pull/217))
- Added better error message for `AUROC` when `num_classes` is not provided for multiclass input ([#244](https://github.com/PyTorchLightning/metrics/pull/244))
- Added support for unnormalized scores (e.g. logits) in `Accuracy`, `Precision`, `Recall`, `FBeta`, `F1`, `StatScore`, `Hamming`, `ConfusionMatrix` metrics ([#200](https://github.com/PyTorchLightning/metrics/pull/200))
- Added `MeanAbsolutePercentageError(MAPE)` metric. ([#248](https://github.com/PyTorchLightning/metrics/pull/248))
- Added `squared` argument to `MeanSquaredError` for computing `RMSE` ([#249](https://github.com/PyTorchLightning/metrics/pull/249))
- Added FID metric ([#213](https://github.com/PyTorchLightning/metrics/pull/213))
- Added `is_differentiable` property to `ConfusionMatrix`, `F1`, `FBeta`, `Hamming`, `Hinge`, `IOU`, `MatthewsCorrcoef`, `Precision`, `Recall`, `PrecisionRecallCurve`, `ROC`, `StatScores` ([#253](https://github.com/PyTorchLightning/metrics/pull/253))
- Added audio metrics: SNR, SI_SDR, SI_SNR ([#292](https://github.com/PyTorchLightning/metrics/pull/292))
- Added Inception Score metric to image module ([#299](https://github.com/PyTorchLightning/metrics/pull/299))
- Added KID metric to image module ([#301](https://github.com/PyTorchLightning/metrics/pull/301))
- Added `sync` and `sync_context` methods for manually controlling when metric states are synced ([#302](https://github.com/PyTorchLightning/metrics/pull/302))
- Added `KLDivergence` metric ([#247](https://github.com/PyTorchLightning/metrics/pull/247))

### Changed

- Forward cache is reset when `reset` method is called ([#260](https://github.com/PyTorchLightning/metrics/pull/260))
- Improved per-class metric handling for imbalanced datasets for `precision`, `recall`, `precision_recall`, `fbeta`, `f1`, `accuracy`, and `specificity` ([#204](https://github.com/PyTorchLightning/metrics/pull/204))
- Decorated `torch.jit.unused` to `MetricCollection` forward ([#307](https://github.com/PyTorchLightning/metrics/pull/307))
- Renamed `thresholds` argument to binned metrics for manually controlling the thresholds ([#322](https://github.com/PyTorchLightning/metrics/pull/322))

### Deprecated

- Deprecated `torchmetrics.functional.mean_relative_error` ([#248](https://github.com/PyTorchLightning/metrics/pull/248))
- Deprecated `num_thresholds` argument in `BinnedPrecisionRecallCurve` ([#322](https://github.com/PyTorchLightning/metrics/pull/322))

### Removed

- Removed argument `is_multiclass` ([#319](https://github.com/PyTorchLightning/metrics/pull/319))

### Fixed

- AUC can also support more dimensional inputs when all but one dimension are of size 1 ([#242](https://github.com/PyTorchLightning/metrics/pull/242))
- Fixed `dtype` of modular metrics after reset has been called ([#243](https://github.com/PyTorchLightning/metrics/pull/243))
- Fixed calculation in `matthews_corrcoef` to correctly match formula ([#321](https://github.com/PyTorchLightning/metrics/pull/321))

## [0.3.2] - 2021-05-10

### Added

- Added `is_differentiable` property:
    * To `AUC`, `AUROC`, `CohenKappa` and `AveragePrecision` ([#178](https://github.com/PyTorchLightning/metrics/pull/178))
    * To `PearsonCorrCoef`, `SpearmanCorrcoef`, `R2Score` and `ExplainedVariance` ([#225](https://github.com/PyTorchLightning/metrics/pull/225))

### Changed

- `MetricCollection` should return metrics with prefix on `items()`, `keys()` ([#209](https://github.com/PyTorchLightning/metrics/pull/209))
- Calling `compute` before `update` will now give warning ([#164](https://github.com/PyTorchLightning/metrics/pull/164))

### Removed

- Removed `numpy` as direct dependency ([#212](https://github.com/PyTorchLightning/metrics/pull/212))

### Fixed

- Fixed auc calculation and add tests ([#197](https://github.com/PyTorchLightning/metrics/pull/197))
- Fixed loading persisted metric states using `load_state_dict()` ([#202](https://github.com/PyTorchLightning/metrics/pull/202))
- Fixed `PSNR` not working with `DDP` ([#214](https://github.com/PyTorchLightning/metrics/pull/214))
- Fixed metric calculation with unequal batch sizes ([#220](https://github.com/PyTorchLightning/metrics/pull/220))
- Fixed metric concatenation for list states for zero-dim input ([#229](https://github.com/PyTorchLightning/metrics/pull/229))
- Fixed numerical instability in `AUROC` metric for large input ([#230](https://github.com/PyTorchLightning/metrics/pull/230))

## [0.3.1] - 2021-04-21

- Cleaning remaining inconsistency and fix PL develop integration (
    [#191](https://github.com/PyTorchLightning/metrics/pull/191),
    [#192](https://github.com/PyTorchLightning/metrics/pull/192),
    [#193](https://github.com/PyTorchLightning/metrics/pull/193),
    [#194](https://github.com/PyTorchLightning/metrics/pull/194)
)


## [0.3.0] - 2021-04-20

### Added

- Added `BootStrapper` to easily calculate confidence intervals for metrics ([#101](https://github.com/PyTorchLightning/metrics/pull/101))
- Added Binned metrics  ([#128](https://github.com/PyTorchLightning/metrics/pull/128))
- Added metrics for Information Retrieval ([(PL^5032)](https://github.com/PyTorchLightning/pytorch-lightning/pull/5032)):
    * Added `RetrievalMAP` ([PL^5032](https://github.com/PyTorchLightning/pytorch-lightning/pull/5032))
    * Added `RetrievalMRR` ([#119](https://github.com/PyTorchLightning/metrics/pull/119))
    * Added `RetrievalPrecision` ([#139](https://github.com/PyTorchLightning/metrics/pull/139))
    * Added `RetrievalRecall` ([#146](https://github.com/PyTorchLightning/metrics/pull/146))
    * Added `RetrievalNormalizedDCG` ([#160](https://github.com/PyTorchLightning/metrics/pull/160))
    * Added `RetrievalFallOut` ([#161](https://github.com/PyTorchLightning/metrics/pull/161))
- Added other metrics:
    * Added `CohenKappa` ([#69](https://github.com/PyTorchLightning/metrics/pull/69))
    * Added `MatthewsCorrcoef` ([#98](https://github.com/PyTorchLightning/metrics/pull/98))
    * Added `PearsonCorrcoef` ([#157](https://github.com/PyTorchLightning/metrics/pull/157))
    * Added `SpearmanCorrcoef` ([#158](https://github.com/PyTorchLightning/metrics/pull/158))
    * Added `Hinge` ([#120](https://github.com/PyTorchLightning/metrics/pull/120))
- Added `average='micro'` as an option in AUROC for multilabel problems ([#110](https://github.com/PyTorchLightning/metrics/pull/110))
- Added multilabel support to `ROC` metric ([#114](https://github.com/PyTorchLightning/metrics/pull/114))
- Added testing for `half` precision ([#77](https://github.com/PyTorchLightning/metrics/pull/77),
    [#135](https://github.com/PyTorchLightning/metrics/pull/135)
)
- Added `AverageMeter` for ad-hoc averages of values ([#138](https://github.com/PyTorchLightning/metrics/pull/138))
- Added `prefix` argument to `MetricCollection` ([#70](https://github.com/PyTorchLightning/metrics/pull/70))
- Added `__getitem__` as metric arithmetic operation ([#142](https://github.com/PyTorchLightning/metrics/pull/142))
- Added property `is_differentiable` to metrics and test for differentiability ([#154](https://github.com/PyTorchLightning/metrics/pull/154))
- Added support for `average`, `ignore_index` and `mdmc_average` in `Accuracy` metric ([#166](https://github.com/PyTorchLightning/metrics/pull/166))
- Added `postfix` arg to `MetricCollection` ([#188](https://github.com/PyTorchLightning/metrics/pull/188))

### Changed

- Changed `ExplainedVariance` from storing all preds/targets to tracking 5 statistics ([#68](https://github.com/PyTorchLightning/metrics/pull/68))
- Changed behaviour of `confusionmatrix` for multilabel data to better match `multilabel_confusion_matrix` from sklearn ([#134](https://github.com/PyTorchLightning/metrics/pull/134))
- Updated FBeta arguments ([#111](https://github.com/PyTorchLightning/metrics/pull/111))
- Changed `reset` method to use `detach.clone()` instead of `deepcopy` when resetting to default ([#163](https://github.com/PyTorchLightning/metrics/pull/163))
- Metrics passed as dict to `MetricCollection` will now always be in deterministic order ([#173](https://github.com/PyTorchLightning/metrics/pull/173))
- Allowed `MetricCollection` pass metrics as arguments ([#176](https://github.com/PyTorchLightning/metrics/pull/176))

### Deprecated

- Rename argument `is_multiclass` -> `multiclass` ([#162](https://github.com/PyTorchLightning/metrics/pull/162))

### Removed

- Prune remaining deprecated ([#92](https://github.com/PyTorchLightning/metrics/pull/92))

### Fixed

- Fixed when `_stable_1d_sort` to work when `n>=N` ([PL^6177](https://github.com/PyTorchLightning/pytorch-lightning/pull/6177))
- Fixed `_computed` attribute not being correctly reset ([#147](https://github.com/PyTorchLightning/metrics/pull/147))
- Fixed to Blau score ([#165](https://github.com/PyTorchLightning/metrics/pull/165))
- Fixed backwards compatibility for logging with older version of pytorch-lightning ([#182](https://github.com/PyTorchLightning/metrics/pull/182))


## [0.2.0] - 2021-03-12

### Changed

- Decoupled PL dependency ([#13](https://github.com/PyTorchLightning/metrics/pull/13))
- Refactored functional - mimic the module-like structure: classification, regression, etc. ([#16](https://github.com/PyTorchLightning/metrics/pull/16))
- Refactored utilities -  split to topics/submodules ([#14](https://github.com/PyTorchLightning/metrics/pull/14))
- Refactored `MetricCollection` ([#19](https://github.com/PyTorchLightning/metrics/pull/19))

### Removed

- Removed deprecated metrics from PL base ([#12](https://github.com/PyTorchLightning/metrics/pull/12),
    [#15](https://github.com/PyTorchLightning/metrics/pull/15))



## [0.1.0] - 2021-02-22

- Added `Accuracy` metric now generalizes to Top-k accuracy for (multi-dimensional) multi-class inputs using the `top_k` parameter ([PL^4838](https://github.com/PyTorchLightning/pytorch-lightning/pull/4838))
- Added `Accuracy` metric now enables the computation of subset accuracy for multi-label or multi-dimensional multi-class inputs with the `subset_accuracy` parameter ([PL^4838](https://github.com/PyTorchLightning/pytorch-lightning/pull/4838))
- Added `HammingDistance` metric to compute the hamming distance (loss) ([PL^4838](https://github.com/PyTorchLightning/pytorch-lightning/pull/4838))
- Added `StatScores` metric to compute the number of true positives, false positives, true negatives and false negatives ([PL^4839](https://github.com/PyTorchLightning/pytorch-lightning/pull/4839))
- Added `R2Score` metric ([PL^5241](https://github.com/PyTorchLightning/pytorch-lightning/pull/5241))
- Added `MetricCollection` ([PL^4318](https://github.com/PyTorchLightning/pytorch-lightning/pull/4318))
- Added `.clone()` method to metrics ([PL^4318](https://github.com/PyTorchLightning/pytorch-lightning/pull/4318))
- Added `IoU` class interface ([PL^4704](https://github.com/PyTorchLightning/pytorch-lightning/pull/4704))
- The `Recall` and `Precision` metrics (and their functional counterparts `recall` and `precision`) can now be generalized to Recall@K and Precision@K with the use of `top_k` parameter ([PL^4842](https://github.com/PyTorchLightning/pytorch-lightning/pull/4842))
- Added compositional metrics ([PL^5464](https://github.com/PyTorchLightning/pytorch-lightning/pull/5464))
- Added AUC/AUROC class interface ([PL^5479](https://github.com/PyTorchLightning/pytorch-lightning/pull/5479))
- Added `QuantizationAwareTraining` callback ([PL^5706](https://github.com/PyTorchLightning/pytorch-lightning/pull/5706))
- Added `ConfusionMatrix` class interface ([PL^4348](https://github.com/PyTorchLightning/pytorch-lightning/pull/4348))
- Added multiclass AUROC metric ([PL^4236](https://github.com/PyTorchLightning/pytorch-lightning/pull/4236))
- Added `PrecisionRecallCurve, ROC, AveragePrecision` class metric ([PL^4549](https://github.com/PyTorchLightning/pytorch-lightning/pull/4549))
- Classification metrics overhaul ([PL^4837](https://github.com/PyTorchLightning/pytorch-lightning/pull/4837))
- Added `F1` class metric ([PL^4656](https://github.com/PyTorchLightning/pytorch-lightning/pull/4656))
- Added metrics aggregation in Horovod and fixed early stopping ([PL^3775](https://github.com/PyTorchLightning/pytorch-lightning/pull/3775))
- Added `persistent(mode)` method to metrics, to enable and disable metric states being added to `state_dict` ([PL^4482](https://github.com/PyTorchLightning/pytorch-lightning/pull/4482))
- Added unification of regression metrics ([PL^4166](https://github.com/PyTorchLightning/pytorch-lightning/pull/4166))
- Added persistent flag to `Metric.add_state` ([PL^4195](https://github.com/PyTorchLightning/pytorch-lightning/pull/4195))
- Added classification metrics ([PL^4043](https://github.com/PyTorchLightning/pytorch-lightning/pull/4043))
- Added new Metrics API. ([PL^3868](https://github.com/PyTorchLightning/pytorch-lightning/pull/3868), [PL^3921](https://github.com/PyTorchLightning/pytorch-lightning/pull/3921))
- Added EMB similarity ([PL^3349](https://github.com/PyTorchLightning/pytorch-lightning/pull/3349))
- Added SSIM metrics ([PL^2671](https://github.com/PyTorchLightning/pytorch-lightning/pull/2671))
- Added BLEU metrics ([PL^2535](https://github.com/PyTorchLightning/pytorch-lightning/pull/2535))
