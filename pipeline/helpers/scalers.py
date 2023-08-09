import numpy as np

from sklearn.preprocessing import (
    FunctionTransformer,
    PowerTransformer,
)


class LogTransformer(FunctionTransformer):
    def __init__(self):
        super().__init__(func=np.log1p, inverse_func=np.expm1)
        self.shift_ = None

    def fit(self, X, y=None):
        self.shift_ = np.min(X, axis=0)
        if np.any(self.shift_ < 0):
            self.shift_ = np.abs(self.shift_) + 1
        else:
            self.shift_ = 0
        return self

    def transform(self, X):
        X_shifted = X + self.shift_
        return super().transform(X_shifted)

    def inverse_transform(self, X):
        X_orig = super().inverse_transform(X)
        return X_orig - self.shift_


class ShiftedBoxCoxTransformer(PowerTransformer):
    def __init__(self):
        super().__init__(method="box-cox", standardize=True)
        self.shift = None

    def fit(self, X, y=None):
        self.shift = abs(np.min(X)) + 1e-8
        return super().fit(X + self.shift, y)

    def transform(self, X):
        assert (
            self.shift is not None
        ), "Transformer must be fitted before calling transform"
        return super().transform(X + np.full(X.shape, self.shift))

    def inverse_transform(self, X):
        assert (
            self.shift is not None
        ), "Transformer must be fitted before calling inverse_transform"
        return super().inverse_transform(X) - np.full(X.shape, self.shift)
