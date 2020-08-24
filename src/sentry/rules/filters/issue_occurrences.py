from __future__ import absolute_import

from django import forms

from sentry.rules.filters.base import EventFilter


class IssueOccurrencesForm(forms.Form):
    value = forms.IntegerField()


class IssueOccurrencesFilter(EventFilter):
    form_cls = IssueOccurrencesForm
    form_fields = {
        "value": {"type": "number", "placeholder": 10},
    }

    label = "An issue has happened at least {value} times"

    def passes(self, event, state):
        try:
            value = int(self.get_option("value"))
        except (TypeError, ValueError):
            return False

        # This value is slightly delayed due to us batching writes to times_seen
        # which can cause the filter to be delayed or occasionally not work as expected.
        issue_occurrences = event.group.times_seen
        return issue_occurrences >= value