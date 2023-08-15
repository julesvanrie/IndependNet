from independnet.calc.params import CORPORATE_TAX_RATE, REDUCED_CORPORATE_TAX_RATE
from independnet.calc.corporate import income_tax
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