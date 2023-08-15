"""Various functions to calculate tax and net payout for profits left in the
company

Functions
---------
    income_tax
    withholding_tax
    profit_after_tax
    net_dividend
"""
import numpy.typing as npt
from independnet.utils import make_non_negative
from independnet.calc.params import (
    CORPORATE_TAX_RATE,
    REDUCED_CORPORATE_TAX_RATE,
    WHT_DIVIDEND,
    REDUCED_WHT_DIVIDEND
)

def income_tax(net_profit: npt.ArrayLike,
               small_company: npt.ArrayLike = False,
               highest_remuneration: npt.ArrayLike = 0) -> npt.ArrayLike:
    """Calculates the corporate tax income

    Parameters
    ----------
    net_profit : npt.ArrayLike
        The net profit of the company after deducting remuneration of directors
    small_company : npt.ArrayLike, default: False
        Whether the company is a small company as required to benefit from
        the reduced tax rate
    highest_remuneration : npt.ArrayLike, default: 0
        The highest remuneration paid out to one of the directores

    Returns
    -------
    npt.ArrayLike
        The corporate income tax to be paid
    """
    eligible_reduced = (highest_remuneration > net_profit) & small_company # type: ignore
    tax_rate = (eligible_reduced * REDUCED_CORPORATE_TAX_RATE
                + (1 - eligible_reduced) * CORPORATE_TAX_RATE)
    tax = tax_rate * net_profit
    tax = make_non_negative(tax)
    return tax


def withholding_tax(net_profit: npt.ArrayLike,
                    eligible_reduced_wht: npt.ArrayLike = False) -> npt.ArrayLike:
    """Calculates the dividend withholding tax

    Parameters
    ----------
    net_profit : npt.ArrayLike
        The net profit of the company after deducting remuneration of directors
    eligible_reduced_wht : npt.ArrayLike, default: False
        Whether the company can benefit from the reduced withholding tax rate

    Returns
    -------
    npt.ArrayLike
        The dividend withholding tax to be paid
    """
    tax_rate = (eligible_reduced_wht * REDUCED_WHT_DIVIDEND  # type: ignore
                + (1 - eligible_reduced_wht) * WHT_DIVIDEND) # type: ignore
    tax = tax_rate * net_profit
    tax = make_non_negative(tax)
    return tax


def profit_after_tax(net_profit: npt.ArrayLike,
                     small_company: npt.ArrayLike = False,
                     highest_remuneration: npt.ArrayLike = 0) -> npt.ArrayLike:
    """Calculates the profit after corporate income tax

    Parameters
    ----------
    net_profit : npt.ArrayLike
        The net profit of the company after deducting remuneration of directors
    small_company : npt.ArrayLike, default: False
        Whether the company is a small company as required to benefit from
        the reduced tax rate
    highest_remuneration : npt.ArrayLike, default: 0
        The highest remuneration paid out to one of the directores

    Returns
    -------
    npt.ArrayLike
        The profit after corporate income tax
    """
    tax = income_tax(net_profit=net_profit,
                     small_company=small_company,
                     highest_remuneration=highest_remuneration)
    return net_profit - tax # type: ignore


def net_dividend(net_profit: npt.ArrayLike,
                 small_company: npt.ArrayLike = False,
                 highest_remuneration: npt.ArrayLike = 0,
                 eligible_reduced_wht: npt.ArrayLike = False) -> npt.ArrayLike:
    """Calculates the net dividend after corporate income tax and after
    withholding tax

    Parameters
    ----------
    net_profit : npt.ArrayLike
        The net profit of the company after deducting remuneration of directors
    small_company : npt.ArrayLike, default: False
        Whether the company is a small company as required to benefit from
        the reduced tax rate
    highest_remuneration : npt.ArrayLike, default: 0
        The highest remuneration paid out to one of the directores
    eligible_reduced_wht : npt.ArrayLike, default: False
        Whether the company can benefit from the reduced withholding tax rate

    Returns
    -------
    npt.ArrayLike
        The net dividend after corporate income tax and after withholding tax
    """
    before_wht = profit_after_tax(net_profit=net_profit,
                                  small_company=small_company,
                                  highest_remuneration=highest_remuneration)
    wht = withholding_tax(net_profit=before_wht,
                          eligible_reduced_wht=eligible_reduced_wht)
    before_wht = make_non_negative(before_wht)
    return before_wht - wht # type: ignore
