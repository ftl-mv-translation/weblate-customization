import re

from django.utils.translation import gettext_lazy as _
from weblate.checks.base import TargetCheck


# Scientifc numbers support because we never know
MATCH_NUMBERS_RE = "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?"


class NumbersNotChanged(TargetCheck):
    """If there's the same amount of number is the same
    in the source and the target, check whether the numbers
    are the same."""

    check_id = "numbers_not_changed"
    name = _("Numbers are not the same.")
    description = _(
        "This likely means the imported translation"
        "didn't match the version of the source files"
    )

    def check_single(self, source, target, unit):
        s_numbers = re.findall(MATCH_NUMBERS_RE, source)
        t_numbers = re.findall(MATCH_NUMBERS_RE, target)

        # Ignore if not same length as it means there's no way
        # to be sure the check is valid
        if len(set(s_numbers)) != len(set(t_numbers)):
            return False
        return set(s_numbers) != set(t_numbers)
