from __future__ import absolute_import

import unittest

from stratified_bayesian_optimization.entities.domain import(
    BoundsEntity,
    DomainEntity,
    ModelValidationError,
)


class TestDomainEntity(unittest.TestCase):

    def setUp(self):
        super(TestDomainEntity, self).setUp()

        self.bounds_domain_x = BoundsEntity({
            'lower_bound': 0,
            'upper_bound': 1
        })

        self.discretization_domain_x = [0]

        self.domain = DomainEntity({
            'dim_x': 1,
            'choose_noise': True,
            'bounds_domain_x': [self.bounds_domain_x],
            'dim_w': 1,
            'domain_w': [[3]],
            'discretization_domain_x': [self.discretization_domain_x]
        })

        self.spec = {
            'dim_x': 1,
            'choose_noise': True,
            'bounds_domain_x': [self.bounds_domain_x]
        }

    def test_discretize_domain(self):
        discretization = DomainEntity.discretize_domain([self.bounds_domain_x], [1])
        assert discretization == [self.discretization_domain_x]

        with self.assertRaises(ValueError):
            DomainEntity.discretize_domain([self.bounds_domain_x], [1, 2])

    def test_get_bounds_as_lists(self):
        bounds = [self.bounds_domain_x]
        assert [[0.0, 1.0]] == BoundsEntity.get_bounds_as_lists(bounds)

    def test_validate(self):

        self.domain.validate()

        wrong_bounds = BoundsEntity({
            'lower_bound': 1,
            'upper_bound': 0
        })

        with self.assertRaises(ModelValidationError):
            wrong_bounds.validate()

        bad_dim_domain_w = DomainEntity({
            'choose_noise': True,
            'dim_x': 1,
            'bounds_domain_x': [self.bounds_domain_x]
        })

        with self.assertRaises(ModelValidationError):
            bad_dim_domain_w.validate()

        bad_dim_domain_w_ = DomainEntity({
            'choose_noise': True,
            'dim_x': 2,
            'bounds_domain_x': [self.bounds_domain_x]
        })

        with self.assertRaises(ModelValidationError):
            bad_dim_domain_w_.validate()

        bad_dim_domain_w_2 = DomainEntity({
            'choose_noise': True,
            'dim_x': 1.0,
            'bounds_domain_x': [self.bounds_domain_x],
            'dim_w': 1
        })

        with self.assertRaises(ModelValidationError):
            bad_dim_domain_w_2.validate()

        bad_dim_domain_w_3 = DomainEntity({
            'choose_noise': True,
            'dim_x': 1,
            'bounds_domain_x': [self.bounds_domain_x],
            'dim_w': 1,
            'domain_w': [self.discretization_domain_x]
        })

        with self.assertRaises(ModelValidationError):
            bad_dim_domain_w_3.validate()

        bad_dim_domain_w_4 = DomainEntity({
            'choose_noise': True,
            'dim_x': 1,
            'bounds_domain_x': [self.bounds_domain_x],
            'dim_w': 1,
            'domain_w': [self.discretization_domain_x],
            'discretization_domain_x': [[5, 6]],
        })

        with self.assertRaises(ModelValidationError):
            bad_dim_domain_w_4.validate()

        bad_dim_domain_w_5 = DomainEntity({
            'choose_noise': True,
            'dim_x': 1,
            'bounds_domain_x': [self.bounds_domain_x],
            'dim_w': 1,
            'domain_w': [self.discretization_domain_x],
            'discretization_domain_x': [[5]],
            'bounds_domain_w': [self.bounds_domain_x, self.bounds_domain_x],
        })

        with self.assertRaises(ModelValidationError):
            bad_dim_domain_w_5.validate()

        bad_dim_domain_w_6 = DomainEntity({
            'choose_noise': True,
            'dim_x': 1,
            'bounds_domain_x': [self.bounds_domain_x],
            'dim_w': 1,
            'domain_w': [self.discretization_domain_x, [4, 5]],
            'discretization_domain_x': [[5]],
            'bounds_domain_w': [self.bounds_domain_x],
        })

        with self.assertRaises(ModelValidationError):
            bad_dim_domain_w_6.validate()
