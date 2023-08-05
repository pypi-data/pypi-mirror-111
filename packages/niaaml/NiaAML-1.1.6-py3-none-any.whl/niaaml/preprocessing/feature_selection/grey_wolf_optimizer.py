from niapy.algorithms.basic import GreyWolfOptimizer as GWO
from niapy.task import Task
from niaaml.preprocessing.feature_selection.feature_selection_algorithm import (
    FeatureSelectionAlgorithm,
)
from niaaml.preprocessing.feature_selection._feature_selection_threshold_problem import (
    _FeatureSelectionThresholdProblem,
)
import numpy

__all__ = ["GreyWolfOptimizer"]


class GreyWolfOptimizer(FeatureSelectionAlgorithm):
    r"""Implementation of feature selection using GWO algorithm.

    Date:
        2020

    Author:
        Luka Pečnik

    Reference:
        The implementation is adapted according to the following article:
        D. Fister, I. Fister, T. Jagrič, I. Fister Jr., J. Brest. A novel self-adaptive differential evolution for feature selection using threshold mechanism . In: Proceedings of the 2018 IEEE Symposium on Computational Intelligence (SSCI 2018), pp. 17-24, 2018.

    Reference URL:
        http://iztok-jr-fister.eu/static/publications/236.pdf

    License:
        MIT

    See Also:
        * :class:`niaaml.preprocessing.feature_selection.feature_selection_algorithm.FeatureSelectionAlgorithm`
    """
    Name = "Grey Wolf Optimizer"

    def __init__(self, **kwargs):
        r"""Initialize GWO feature selection algorithm."""
        super(GreyWolfOptimizer, self).__init__()
        self.__gwo = GWO(population_size=10)

    def __final_output(self, sol):
        r"""Calculate final array of features.

        Arguments:
            sol (numpy.ndarray[float]): Individual of population/ possible solution.

        Returns:
            numpy.ndarray[bool]: Mask of selected features.
        """
        selected = numpy.ones(sol.shape[0] - 1, dtype=bool)
        threshold = sol[sol.shape[0] - 1]
        for i in range(sol.shape[0] - 1):
            if sol[i] < threshold:
                selected[i] = False
        return selected

    def select_features(self, x, y, **kwargs):
        r"""Perform the feature selection process.

        Arguments:
            x (pandas.core.frame.DataFrame): Array of original features.
            y (pandas.core.series.Series) Expected classifier results.

        Returns:
            numpy.ndarray[bool]: Mask of selected features.
        """
        problem = _FeatureSelectionThresholdProblem(x, y)
        task = Task(problem=problem, max_evals=1000)
        self.__gwo.run(task)
        return self.__final_output(problem.get_best_solution())

    def to_string(self):
        r"""User friendly representation of the object.

        Returns:
            str: User friendly representation of the object.
        """
        return FeatureSelectionAlgorithm.to_string(self).format(
            name=self.Name, args=self._parameters_to_string(self.__gwo.get_parameters())
        )
