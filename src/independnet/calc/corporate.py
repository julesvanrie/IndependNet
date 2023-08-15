"""Various functions to calculate tax and net payout for profits left in the
company

Functions
---------
    income_tax
"""
# import numpy as np
import numpy.typing as npt
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
    # Ensure tax is not negative
    if isinstance(tax, (int, float)):
        tax = max(tax, 0)
    else:
        tax[tax<0] = 0
    return tax


def withholding_tax(net_profit: npt.ArrayLike,
                    eligible_reduced: npt.ArrayLike = False) -> npt.ArrayLike:
    """Calculates the dividend withholding tax

    Parameters
    ----------
    net_profit : npt.ArrayLike
        The net profit of the company after deducting remuneration of directors
    eligible_reduced : npt.ArrayLike, default: False
        Whether the company can benefit from the reduced withholding tax rate

    Returns
    -------
    npt.ArrayLike
        The dividend withholding tax to be paid
    """
    tax_rate = (eligible_reduced * REDUCED_WHT_DIVIDEND
                + (1 - eligible_reduced) * WHT_DIVIDEND)
    tax = tax_rate * net_profit
    # Ensure tax is not negative
    if isinstance(tax, (int, float)):
        tax = max(tax, 0)
    else:
        tax[tax<0] = 0
    return tax
