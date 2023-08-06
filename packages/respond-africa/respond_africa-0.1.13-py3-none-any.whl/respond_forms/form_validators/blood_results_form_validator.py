from django import forms
from edc_blood_results import BloodResultsFormValidatorMixin
from edc_constants.constants import FASTING
from edc_lab_panel.panels import (
    blood_glucose_panel,
    blood_glucose_poc_panel,
    fbc_panel,
    hba1c_panel,
    lft_panel,
    lipids_panel,
    rft_panel,
)


class BloodResultsGluFormValidator(BloodResultsFormValidatorMixin):
    panels = [blood_glucose_panel, blood_glucose_poc_panel]

    @property
    def extra_options(self):
        if not self.cleaned_data.get("fasting"):
            raise forms.ValidationError({"fasting": "This field is required."})
        fasting = True if self.cleaned_data.get("fasting") == FASTING else False
        return dict(fasting=fasting)


class BloodResultsFbcFormValidator(BloodResultsFormValidatorMixin):
    panels = fbc_panel


class BloodResultsHba1cFormValidator(BloodResultsFormValidatorMixin):
    panel = hba1c_panel

    # def validate_reportable_fields(self, **kwargs):
    #     pass


class BloodResultsLipidFormValidator(BloodResultsFormValidatorMixin):
    panel = lipids_panel


class BloodResultsLftFormValidator(BloodResultsFormValidatorMixin):
    panel = lft_panel


class BloodResultsRftFormValidator(BloodResultsFormValidatorMixin):
    panel = rft_panel
