# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashSelectable(Component):
    """A DashSelectable component.
Contains a wrapper component which attaches an event that listens
for selection so children components that are selected

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    Child components.

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- selectedValue (string; optional):
    Selected value."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, selectedValue=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'selectedValue']
        self._type = 'DashSelectable'
        self._namespace = 'dash_selectable'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'selectedValue']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashSelectable, self).__init__(children=children, **args)
