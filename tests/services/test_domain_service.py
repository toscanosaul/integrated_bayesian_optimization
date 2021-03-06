from __future__ import absolute_import

from doubles import allow, expect
import unittest

import numpy as np
import os
from mock import patch, MagicMock

from stratified_bayesian_optimization.services.domain import DomainService
from stratified_bayesian_optimization.util.json_file import JSONFile
from stratified_bayesian_optimization.entities.domain import(
    BoundsEntity,
    DomainEntity,
)


class MockMkdir(object):
    def __init__(self):
        self.received_args = None

    def __call__(self, *args):
        self.received_args = args


class TestDomainService(unittest.TestCase):

    def setUp(self):

        self.bounds_domain_x = BoundsEntity({
            'lower_bound': 0,
            'upper_bound': 1
        })

        self.spec = {
            'dim_x': 1,
            'choose_noise': True,
            'bounds_domain_x': [self.bounds_domain_x]
        }

    def test_load_discretization_file_not_exists(self):
        allow(JSONFile).read
        expect(JSONFile).write.twice()
        expect(DomainEntity).discretize_domain.twice().and_return([])
        expect(BoundsEntity).get_bounds_as_lists.twice().and_return([2])

        assert DomainService.load_discretization('test_problem', 1, 0) == []

        with patch('os.path.exists', new=MagicMock(return_value=False)):
            os.mkdir = MockMkdir()
            assert DomainService.load_discretization('test_problem', 1, 0) == []

    def test_load_discretization_file_exists(self):
        allow(JSONFile).read.and_return([])
        expect(DomainEntity).discretize_domain.never()
        expect(BoundsEntity).get_bounds_as_lists.once().and_return([2])

        assert DomainService.load_discretization('test_problem', 1, 0) == []

    def test_domain_from_dict(self):
        expect(DomainService).load_discretization.never()
        DomainService.from_dict(self.spec)

        expect(DomainService).load_discretization.once().and_return([])
        self.spec['number_points_each_dimension'] = [5]
        self.spec['problem_name'] = 'test'
        DomainService.from_dict(self.spec)

    def test_get_points_domain(self):
        sample = DomainService.get_points_domain(2, [[1, 5], [2, 3, 4]], [0, 1], 1)
        np.random.seed(1)

        assert sample == [[2.668088018810296, 2], [3.8812979737686324, 3]]

        sample_2 = DomainService.get_points_domain(2, [[1, 5], [2, 3]], random_seed=1)
        np.random.seed(1)
        a = list(np.random.uniform(1, 5, 2))
        b = list(np.random.uniform(2, 3, 2))

        assert sample_2 == [[a[0], b[0]], [a[1], b[1]]]
