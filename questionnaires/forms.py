from collections import defaultdict

from django.core.exceptions import ValidationError
from django import forms
from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.contrib.forms.forms import FormBuilder

from questionnaires.blocks import VALID_SKIP_SELECTORS, SkipState, VALID_SKIP_LOGIC


class CustomFormBuilder(FormBuilder):
    def create_positivenumber_field(self, field, options):
        options.update({
            'min_value': 0,
        })

        return forms.IntegerField(**options)


class SurveyForm(WagtailAdminPageForm):
    form_field_name = 'survey_form_fields'
    _clean_errors = None

    def clean(self):
        cleaned_data = super().clean()

        question_data = {}
        for form in self.formsets[self.form_field_name]:
            form.is_valid()
            question_data[form.cleaned_data['ORDER']] = form

        for i, form in question_data.items():
            self._clean_errors = {}
            if form.is_valid():
                data = form.cleaned_data
                if self.data.get('multi_step', 'off') == 'off' and data['page_break']:
                    self.add_form_field_error(
                        'page_break',
                        _('Page break is only allowed with multi-step enabled.'),
                    )
                if data['field_type'] == 'checkbox':
                    if len(data['skip_logic']) != 2:
                        self.add_form_field_error(
                            'field_type',
                            _('Checkbox type questions must have 2 Answer '
                              'Options: a on and off'),
                        )
                elif data['field_type'] in VALID_SKIP_LOGIC:
                    for j, logic in enumerate(data['skip_logic']):
                        if not logic.value['choice']:
                            self.add_stream_field_error(
                                j,
                                'choice',
                                _('This field is required.'),
                            )
                        if logic.value['skip_logic'] == SkipState.QUESTION and logic.value['question']:
                            last_question_number = logic.value['question']
                            msg = _(f'Skip to question {question_data[last_question_number].cleaned_data["label"]} '
                                    f'with in-between required questions isn\'t allowed.')
                        elif logic.value['skip_logic'] == SkipState.END:
                            last_question_number = len(question_data)
                            msg = _(f'Skip to end of survey with in-between required questions isn\'t allowed.')
                        else:
                            continue
                        for k in range(i + 1, last_question_number + 1):
                            skip_to_question = question_data[k].cleaned_data
                            if skip_to_question['required']:
                                self.add_stream_field_error(j, 'question', msg)
                                break
                if data['field_type'] in ["checkbox", "checkboxes"]:
                    for i, logic in enumerate(data['skip_logic']):
                        if logic.value['skip_logic'] != SkipState.NEXT:
                            self.add_stream_field_error(
                                i,
                                'skip_logic',
                                _(f'Skipping to {logic.value["skip_logic"]} not allowed for checkbox and checkboxes.'),
                            )
                if self.clean_errors:
                    form._errors = self.clean_errors

        return cleaned_data

    def save(self, commit):
        # Tidy up the skip logic when field cant have skip logic
        for form in self.formsets[self.form_field_name]:
            field_type = form.instance.field_type
            # Copy choices values from skip logic to main choices property
            if field_type in VALID_SKIP_SELECTORS:
                choices_values = []
                for skip_logic in form.instance.skip_logic:
                    choices_values.append(skip_logic.value['choice'].replace(',', u'\u201A'))
                form.instance.choices = ",".join(choices_values)

            if field_type not in VALID_SKIP_SELECTORS:
                if field_type != 'checkboxes':
                    form.instance.skip_logic = []
                else:
                    for skip_logic in form.instance.skip_logic:
                        skip_logic.value['skip_logic'] = SkipState.NEXT
                        skip_logic.value['question'] = None
            elif field_type == 'checkbox':
                for skip_logic in form.instance.skip_logic:
                    skip_logic.value['choice'] = ''

        return super().save(commit)

    def add_stream_field_error(self, position, field, message):
        if position not in self._clean_errors:
            self._clean_errors[position] = defaultdict(list)
        self._clean_errors[position][field].append(message)

    @property
    def clean_errors(self):
        if self._clean_errors.keys():
            params = {
                key: ErrorList(
                    [ValidationError('Error in form', params=value)]
                )
                for key, value in self._clean_errors.items()
                if isinstance(key, int)
            }
            errors = {
                key: ValidationError(value)
                for key, value in self._clean_errors.items()
                if isinstance(key, str)
            }
            errors.update({
                'skip_logic': ErrorList([ValidationError(
                    'Skip Logic Error',
                    params=params,
                )])
            })
            return errors

    def add_form_field_error(self, field, message):
        if field not in self._clean_errors:
            self._clean_errors[field] = list()
        self._clean_errors[field].append(message)


class QuizForm(WagtailAdminPageForm):
    form_field_name = 'quiz_form_fields'
    _clean_errors = None

    def clean(self):
        cleaned_data = super().clean()

        question_data = {}
        for form in self.formsets[self.form_field_name]:
            form.is_valid()
            question_data[form.cleaned_data['ORDER']] = form

        for i, form in question_data.items():
            self._clean_errors = {}
            if form.is_valid():
                data = form.cleaned_data
                if self.data.get('multi_step', 'off') == 'off' and data['page_break']:
                    self.add_form_field_error(
                        'page_break',
                        _('Page break is only allowed with multi-step enabled.'),
                    )
                if data['field_type'] == 'checkbox':
                    if len(data['skip_logic']) != 2:
                        self.add_form_field_error(
                            'field_type',
                            _('Checkbox type questions must have 2 Answer '
                              'Options: a on and off'),
                        )
                elif data['field_type'] in VALID_SKIP_LOGIC:
                    for j, logic in enumerate(data['skip_logic']):
                        if not logic.value['choice']:
                            self.add_stream_field_error(
                                j,
                                'choice',
                                _('This field is required.'),
                            )
                        if logic.value['skip_logic'] == SkipState.QUESTION and logic.value['question']:
                            last_question_number = logic.value['question']
                            msg = _(f'Skip to question {question_data[last_question_number].cleaned_data["label"]} '
                                    f'with in-between required questions isn\'t allowed.')
                        elif logic.value['skip_logic'] == SkipState.END:
                            last_question_number = len(question_data)
                            msg = _(f'Skip to end of survey with in-between required questions isn\'t allowed.')
                        else:
                            continue
                        for k in range(i + 1, last_question_number + 1):
                            skip_to_question = question_data[k].cleaned_data
                            if skip_to_question['required']:
                                self.add_stream_field_error(j, 'question', msg)
                                break
                if data['field_type'] in ["checkbox", "checkboxes"]:
                    for i, logic in enumerate(data['skip_logic']):
                        if logic.value['skip_logic'] != SkipState.NEXT:
                            self.add_stream_field_error(
                                i,
                                'skip_logic',
                                _(f'Skipping to {logic.value["skip_logic"]} not allowed for checkbox, checkboxes.'),
                            )
                if self.clean_errors:
                    form._errors = self.clean_errors

        return cleaned_data

    def save(self, commit):
        # Tidy up the skip logic when field cant have skip logic
        for form in self.formsets[self.form_field_name]:
            form.instance.correct_answer = form.instance.correct_answer.replace(',', u'\u201A')
            field_type = form.instance.field_type
            # Copy choices values from skip logic to main choices property
            if field_type in VALID_SKIP_SELECTORS:
                choices_values = []
                for skip_logic in form.instance.skip_logic:
                    choices_values.append(skip_logic.value['choice'].replace(',', u'\u201A'))
                form.instance.choices = ",".join(choices_values)

            if field_type not in VALID_SKIP_SELECTORS:
                if field_type != 'checkboxes':
                    form.instance.skip_logic = []
                else:
                    for skip_logic in form.instance.skip_logic:
                        skip_logic.value['skip_logic'] = SkipState.NEXT
                        skip_logic.value['question'] = None
            elif field_type == 'checkbox':
                for skip_logic in form.instance.skip_logic:
                    skip_logic.value['choice'] = ''

        return super().save(commit)

    def add_stream_field_error(self, position, field, message):
        if position not in self._clean_errors:
            self._clean_errors[position] = defaultdict(list)
        self._clean_errors[position][field].append(message)

    @property
    def clean_errors(self):
        if self._clean_errors.keys():
            params = {
                key: ErrorList(
                    [ValidationError('Error in form', params=value)]
                )
                for key, value in self._clean_errors.items()
                if isinstance(key, int)
            }
            errors = {
                key: ValidationError(value)
                for key, value in self._clean_errors.items()
                if isinstance(key, str)
            }
            errors.update({
                'skip_logic': ErrorList([ValidationError(
                    'Skip Logic Error',
                    params=params,
                )])
            })
            return errors

    def add_form_field_error(self, field, message):
        if field not in self._clean_errors:
            self._clean_errors[field] = list()
        self._clean_errors[field].append(message)
