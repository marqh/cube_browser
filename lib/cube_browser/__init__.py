"""
Configuration and preset for Holoviews and Geoviews for Iris Cube Browsing.

"""
import holoviews as hv
import geoviews as gv
import iris

from .phenomenon_presets import phenomena


class DimensionPresets(hv.AttrTree):
    """
    Sets dir_mode on the holoviews AttTree so that onlyb user entires are
    tab completed and allows lower case throughout.

    This class may migrate to holoviews in time.
    """

    _sanitizer = hv.core.util.sanitize_identifier_fn.instance(capitalize=False)

    def __init__(self, items=None, identifier=None, parent=None,
                 dir_mode='user'):
        super(DimensionPresets, self).__init__(items=items,
                                               identifier=identifier,
                                               parent=parent,
                                               dir_mode=dir_mode)
    def __setattr__(self, identifier, val):
        # Getattr is skipped for root and first set of children
        shallow = (self.parent is None or self.parent.parent is None)
        if identifier[0].isupper() and self.fixed and shallow:
            raise AttributeError(self._fixed_error % identifier)

        super(hv.AttrTree, self).__setattr__(identifier, val)

        if not identifier in self.children:
            self.children.append(identifier)
        self._propagate((identifier,), val)

        
def register_dimensions(phenomena, options,
                        element_classes=None):
    """
    
    """
    if element_classes is None:
        element_classes = [hv.Image, hv.Points, hv.Contours,
                           gv.FilledContours, gv.LineContours]
    else:
        element_classes = []
    dims = DimensionPresets()
    for name, definition in phenomena.items():
        (cmap, units) = definition
        for cls in element_classes:
            options[cls.__name__][name] = hv.Options('style', cmap=cmap)
        for unit_info in units:
            (unit_name, unit_range) = unit_info
            dim = hv.Dimension(name, unit=unit_name, range=unit_range)
            dims.set_path('%s.%s' % (name, unit_name), dim)
    return dims

def set_mpl_presets():
    # set default colours and ranges for matplotlib
    phenoms = register_dimensions(phenomena,
                                  hv.Store.options(backend='matplotlib'))
    hv.notebook_extension()
    #get_ipython().magic(u"output size=300 backend='matplotlib:nbagg'")
    get_ipython().magic(u"output size=300")
    
    # set colourmap and range for phenomena.  This is applied per Dataset.
    # Once a Dataset instance is created, that instance has it's own copy of
    # these choices, so changing the values in the cube_browser dictionary
    # or the hv.Dimension.preset has no effect on already created Datasets.
    hv.Dimension.presets = phenoms

    # set plotting settings
    gv.plotting.GeoImagePlot.colorbar=True
    return phenoms

phenoms = set_mpl_presets()

iris.FUTURE.netcdf_promote = True
iris.FUTURE.strict_grib_load = True


