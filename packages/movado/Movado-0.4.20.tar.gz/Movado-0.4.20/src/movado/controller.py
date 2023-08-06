def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn

from abc import abstractmethod, ABC
from typing import Tuple, Optional, Callable, Any, List, Dict, Union
from scipy.stats import PearsonRConstantInputWarning
from sklearn.preprocessing import StandardScaler
import sklearn.gaussian_process as gp
import numpy as np
import scipy as sp
import time
from pathlib import Path
import math

from movado.estimator import Estimator
from movado.mab_handler import MabHandler

is_call_exact: List[bool] = []  # i-th element True if i-th call is exact


class Controller(ABC):
    @abstractmethod
    def __init__(
        self,
        exact_fitness: Callable[[List[float]], List[float]] = None,
        estimator: Estimator = None,
        self_exact: Optional[object] = None,
        debug: bool = False,
        **kwargs
    ):
        self.__scaler = StandardScaler()
        self.__time_dataset: List[float] = []
        self.__error_dataset: List[float] = []
        self.__cost_dataset: List[float] = []
        self.__to_reshape = False
        self._exact: Callable[[List[float]], List[float]] = exact_fitness
        self._estimator: Estimator = estimator
        self._debug = debug
        self._self_exact = self_exact
        if self._debug:
            Path("movado_debug").mkdir(exist_ok=True)
            self._controller_debug = "movado_debug/controller.csv"
            Path(self._controller_debug).open("w").close()

    @abstractmethod
    def compute_objective(
        self, point: List[int], decision_only: bool = False
    ) -> List[float]:
        pass

    def learn(
        self,
        is_exact: bool,
        point: List[float],
        exec_time: float = None,
        mab: Optional[Tuple[MabHandler, Union[int, float]]] = None,
        mab_forced_probability: Optional[float] = None,
        mab_forced_action: Optional[Union[int, float]] = None,
        mab_weight: Optional[MabHandler] = None,
        mab_weight_forced_probability: Optional[float] = None,
        mab_weight_forced_action: Optional[Union[int, float]] = None,
        is_point_in_context: bool = True,
    ):

        self.__time_dataset.append(exec_time)
        self.__error_dataset.append(0 if is_exact else self._estimator.get_error())
        if mab:
            if mab_weight:
                time_weight = (
                    mab_weight.predict(
                        self._compute_weighting_context(self.get_mab().get_mean_cost())
                    )
                    / 100
                )
                mab[0].learn(
                    cost=self.get_time_error_z_score(
                        time_weight=time_weight, error_weight=1 - time_weight
                    ),
                    context=self._compute_controller_context(point),
                    forced_predict_probability=mab_forced_probability,
                    forced_action=mab_forced_action,
                ),
                mab_weight.learn(
                    cost=self.compute_first_order_sensitivity_index(),
                    context=self._compute_weighting_context(
                        self.get_mab().get_mean_cost()
                    ),
                    forced_predict_probability=mab_weight_forced_probability,
                    forced_action=mab_weight_forced_action,
                )
            else:
                mab[0].learn(
                    cost=self.get_time_error_z_score(),
                    context=self._compute_controller_context(point),
                    forced_predict_probability=mab_forced_probability,
                    forced_action=mab_forced_action,
                )

    def _compute_exact(
        self,
        point: List[int],
        mab: Optional[Tuple[MabHandler, Union[int, float]]] = None,
        mab_forced_probability: Optional[int] = None,
        mab_weight: Optional[MabHandler] = None,
        mab_weight_forced_probability: Optional[int] = None,
        is_point_in_context: bool = True,
    ) -> Tuple[List[float], float]:
        global is_call_exact
        is_call_exact.append(True)

        if self._self_exact:
            exact, exec_time = Controller.measure_execution_time(
                self._exact, self._self_exact, point
            )
        else:
            exact, exec_time = Controller.measure_execution_time(self._exact, point)

        self.learn(
            is_exact=True,
            point=point,
            exec_time=exec_time,
            mab=mab,
            mab_forced_probability=mab_forced_probability,
            mab_weight=mab_weight,
            mab_weight_forced_probability=mab_weight_forced_probability,
            is_point_in_context=is_point_in_context,
        )

        self._estimator.train(point, exact)
        return exact, exec_time

    @staticmethod
    def __extract_time_context_features(series: List[float]):
        return (
            (np.mean(series), np.var(series), max(series), min(series), series[-1])
            if len(series) > 0
            else (0, 0, 0, 0, 0)
        )

    @staticmethod
    def _compute_controller_context(point: List[float]):
        return point

    # def _compute_controller_context(self, point: List[int] = None) -> List[float]:
    #     exact_execution_times: List[float] = list(
    #         compress(self.__time_dataset, self.__is_call_exact)
    #     )
    #     estimated_execution_times: List[float] = [
    #         x for x in self.__time_dataset if x not in exact_execution_times
    #     ]
    #     context = [
    #         self._estimator.get_error(),
    #         *self.__extract_time_context_features(exact_execution_times),
    #         *self.__extract_time_context_features(estimated_execution_times),
    #     ]
    #     if not point:
    #         return context
    #     else:
    #         return context + point

    @staticmethod
    def _compute_weighting_context(mab_loss: float) -> List[float]:
        global is_call_exact
        exact_calls = is_call_exact.count(True)
        return [mab_loss, exact_calls, len(is_call_exact) - exact_calls]

    def _compute_estimated(
        self,
        point: List[int],
        mab: Optional[Tuple[MabHandler, Union[int, float]]] = None,
        mab_weight: MabHandler = None,
        is_point_in_context: bool = True,
    ) -> Tuple[List[float], float]:
        global is_call_exact
        is_call_exact.append(False)

        estimation, exec_time = Controller.measure_execution_time(
            self._estimator.predict,
            point,
        )
        self.__time_dataset.append(exec_time)
        self.__error_dataset.append(self._estimator.get_error())

        self.learn(
            is_exact=False,
            point=point,
            exec_time=exec_time,
            mab=mab,
            mab_forced_probability=None,
            mab_weight=mab_weight,
            mab_weight_forced_probability=None,
            is_point_in_context=is_point_in_context,
        )

        return estimation, exec_time

    @abstractmethod
    def initialize_debug(self):
        pass

    @abstractmethod
    def write_debug(self, debug_info: Dict[str, Any]):
        pass

    def __reshape(self, to_reshape):
        if len(self.__time_dataset) > 1:
            return np.reshape(to_reshape, (-1, 1))
        else:
            return np.reshape(to_reshape, (1, -1))

    def get_time_error_z_score(
        self,
        time_weight: float = 1,
        error_weight: float = 1,
    ) -> float:
        reshaped_time = self.__reshape(self.__time_dataset)
        reshaped_error = self.__reshape(self.__error_dataset)
        self.__scaler.fit(reshaped_time)
        time_z_score: float = self.__scaler.transform(reshaped_time)[-1][0]
        self.__scaler.fit(reshaped_error)
        error_z_score: float = self.__scaler.transform(reshaped_error)[-1][0]
        out = (time_weight * time_z_score) + (error_weight * error_z_score)
        self.__cost_dataset.append(out)
        return out

    @staticmethod
    def __is_constant(x):
        return x.count(x[0]) == len(x)

    def get_time_error_correlation(self):
        try:
            samples = len(self.__error_dataset)
            independent_vars = 2
            if (
                self.__is_constant(self.__error_dataset)
                or self.__is_constant(self.__time_dataset)
                or self.__is_constant(self.__cost_dataset)
                or samples - independent_vars == 1
            ):
                return 0
            time_cost_correlation: float = sp.stats.pearsonr(
                self.__time_dataset, self.__cost_dataset
            )[0]
            error_cost_correlation: float = sp.stats.pearsonr(
                self.__error_dataset, self.__cost_dataset
            )[0]
            time_error_correlation: float = sp.stats.pearsonr(
                self.__time_dataset, self.__error_dataset
            )[0]
            R2 = np.sqrt(
                (
                    np.abs(time_cost_correlation ** 2)
                    + np.abs(error_cost_correlation ** 2)
                    - 2
                    * time_cost_correlation
                    * error_cost_correlation
                    * time_error_correlation
                )
                / (1 - np.abs(time_error_correlation))
            )
            if R2 == np.nan:
                return 0
            R2_adj = 1 - (
                ((1 - R2 ** 2) * (samples - 1)) / (samples - independent_vars - 1)
            )
            return -R2_adj
        except ValueError:
            return 0

    def compute_first_order_sensitivity_index(self):
        if len(self.__cost_dataset) == 1:
            return 0
        kernel = gp.kernels.ConstantKernel(1.0, (1e-1, 1e3)) * gp.kernels.RBF(
            10.0, (1e-3, 1e3)
        )
        model_time = gp.GaussianProcessRegressor(
            kernel=kernel, n_restarts_optimizer=30, alpha=0.1, normalize_y=True
        )
        model_error = gp.GaussianProcessRegressor(
            kernel=kernel, n_restarts_optimizer=30, alpha=0.1, normalize_y=True
        )
        reshaped_time = self.__reshape(self.__time_dataset)
        reshaped_error = self.__reshape(self.__error_dataset)
        model_time.fit(reshaped_time, self.__cost_dataset)
        model_error.fit(reshaped_error, self.__cost_dataset)
        fitted_time = [
            float(model_time.predict(self.__reshape([x]))) for x in self.__time_dataset
        ]
        fitted_error = [
            float(model_error.predict(self.__reshape([x])))
            for x in self.__error_dataset
        ]
        time_importance = np.sum(
            [
                ((fitted - np.mean(fitted_time)) ** 2)
                / (cost - np.mean(self.__cost_dataset)) ** 2
                for fitted, cost in zip(fitted_time, self.__cost_dataset)
            ]
        )
        error_importance = np.sum(
            [
                ((fitted - np.mean(fitted_error)) ** 2)
                / (cost - np.mean(self.__cost_dataset)) ** 2
                for fitted, cost in zip(fitted_error, self.__cost_dataset)
            ]
        )
        importance_sum = np.sum([time_importance, error_importance])
        time_importance = time_importance / importance_sum
        error_importance = error_importance / importance_sum
        # target (normalized) importance for both is 0.5
        return ((0.5 - time_importance) + (0.5 - error_importance)) ** 2

    @staticmethod
    def measure_execution_time(
        func: Callable[..., Any], *args, **kwargs
    ) -> Tuple[Any, float]:
        start = time.time()
        out = func(*args, **kwargs)
        execution_time = time.time() - start
        return out, execution_time

    @abstractmethod
    def get_mab(self) -> MabHandler:
        pass

    @abstractmethod
    def get_weight_mab(self) -> MabHandler:
        pass

    @abstractmethod
    def get_parameters(self):
        pass
