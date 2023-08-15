from independnet.calc.params import (
    CORPORATE_TAX_RATE,
    REDUCED_CORPORATE_TAX_RATE,
    WHT_DIVIDEND,
    REDUCED_WHT_DIVIDEND
)
from independnet.calc.corporate import income_tax, withholding_tax
import numpy as np

class TestIncomeTax:
    def test_number(self):
        net_profit = 20_000
        tax_calculated = income_tax(net_profit)
        tax_expected = net_profit * .25
        assert tax_calculated == tax_expected

    def test_number_small(self):
        net_profit = 20_000
        tax_expected = net_profit * .25
        tax_calculated = income_tax(net_profit,
                                    small_company=True)
        assert tax_calculated == tax_expected

    def test_number_small_with_sufficient_remuneration(self):
        net_profit = 20_000
        remuneration = 30_000
        tax_expected = net_profit * .20
        tax_calculated = income_tax(net_profit,
                                    small_company=True,
                                    highest_remuneration=remuneration)
        assert tax_calculated == tax_expected

    def test_number_small_with_insufficient_remuneration(self):
        net_profit = 20_000
        remuneration = 15_000
        tax_expected = net_profit * .25
        tax_calculated = income_tax(net_profit,
                                    small_company=True,
                                    highest_remuneration=remuneration)
        assert tax_calculated == tax_expected

    def test_number_not_negative(self):
        net_profit = -20_000
        tax_calculated = income_tax(net_profit)
        assert tax_calculated >= 0 # type: ignore

    def test_array(self):
        net_profit = np.array([10_000, 10_000, -10_000])
        tax_expected = np.array([2_500, 2_500, 0])
        tax_calculated = income_tax(net_profit)
        assert np.allclose(tax_calculated, tax_expected)

    def test_array_small(self):
        net_profit = np.array([10_000, 10_000, -10_000])
        remuneration = np.array([9_000, 11_000, 5_000])
        tax_expected = np.array([10_000 * CORPORATE_TAX_RATE,
                                 10_000 * REDUCED_CORPORATE_TAX_RATE,
                                 0])
        tax_calculated = income_tax(net_profit,
                                    small_company=True,
                                    highest_remuneration=remuneration)
        assert np.allclose(tax_calculated, tax_expected)


class TestWithholdingTax:
    def test_number(self):
        net_profit = 10_000
        tax_calculated = withholding_tax(net_profit)
        tax_expected = net_profit * WHT_DIVIDEND
        assert tax_calculated == tax_expected

    def test_number_reduced(self):
        net_profit = 10_000
        tax_calculated = withholding_tax(net_profit, eligible_reduced=True)
        tax_expected = net_profit * REDUCED_WHT_DIVIDEND
        assert tax_calculated == tax_expected

    def test_number_not_negative(self):
        net_profit = -10_000
        tax_calculated = withholding_tax(net_profit)
        assert tax_calculated >= 0 # type: ignore

    def test_array(self):
        net_profit = np.array([10_000,
                               10_000,
                               -10_000])
        tax_expected = np.array([10_000 * WHT_DIVIDEND,
                                 10_000 * WHT_DIVIDEND,
                                 0])
        tax_calculated = withholding_tax(net_profit)
        assert np.allclose(tax_calculated, tax_expected)

    def test_array_reduced(self):
        net_profit = np.array([10_000,
                               10_000,
                               -10_000])
        reduced = np.array([False, True, True])
        tax_expected = np.array([10_000 * WHT_DIVIDEND,
                                 10_000 * REDUCED_WHT_DIVIDEND,
                                 0])
        tax_calculated = withholding_tax(net_profit, eligible_reduced=reduced)
        assert np.allclose(tax_calculated, tax_expected)


class TestProfitAfterTax:
    def test_number(self):
        net_profit = 10_000
        calculated = profit_after_tax(net_profit)
        expected = net_profit * (1 - CORPORATE_TAX_RATE)
        assert calculated == expected

    def test_number_reduced(self):
        net_profit = 10_000
        remuneration = 11_000
        calculated = profit_after_tax(net_profit,
                                      small_company=True,
                                      highest_remuneration=remuneration)
        expected = net_profit * (1 - REDUCED_CORPORATE_TAX_RATE)
        assert calculated == expected

    def test_array(self):
        net_profit = np.array([10_000, 10_000, 10_000, -10_000])
        small_company = np.array([False, True, True])
        remuneration = np.array([11_000, 9_000, 11_000, 5_000])
        expected = np.array([10_000 * CORPORATE_TAX_RATE,
                                 10_000 * CORPORATE_TAX_RATE,
                                 10_000 * REDUCED_CORPORATE_TAX_RATE,
                                 0])
        calculated = profit_after_tax(net_profit,
                                      small_company=small_company,
                                      highest_remuneration=remuneration)
        assert np.allclose(calculated, expected)
