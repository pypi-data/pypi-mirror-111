# -*- Mode: python; tab-width: 4; indent-tabs-mode:nil; coding:utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
# layz_import --- https://github.com/mnmelo/layz_import
# Copyright (C) 2017-2018 Manuel Nuno Melo
#
# This file is part of layz_import.
#
#  layz_import is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  layz_import is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with layz_import.  If not, see <http://www.gnu.org/licenses/>.
#
# layz_import was based on code from the importing module from the PEAK
# package (see <http://peak.telecommunity.com/DevCenter/Importing>). The PEAK
# package is released under the following license, reproduced here:
#
#  Copyright (C) 1996-2004 by Phillip J. Eby and Tyler C. Sarna.
#  All rights reserved.  This software may be used under the same terms
#  as Zope or Python.  THERE ARE ABSOLUTELY NO WARRANTIES OF ANY KIND.
#  Code quality varies between modules, from "beta" to "experimental
#  pre-alpha".  :)
#
# Code pertaining to layz loading from PEAK importing was included in
# layz_import, modified in a number of ways. These are detailed in the
# CHANGELOG file of layz_import. Changes mainly involved Python 3
# compatibility, extension to allow customizable behavior, and added
# functionality (layz importing of callable objects).
# 

"""
layz module loading
===================

Functions and classes for layz module loading that also delay import errors.
Heavily borrowed from the `importing`_ module.

.. _`importing`: http://peak.telecommunity.com/DevCenter/Importing

Files and directories
---------------------

.. autofunction:: module
.. autofunction:: callable

"""

__all__ = ['layz_module', 'layz_callable', 'layz_function', 'layz_class',
           'layzModule', 'layzCallable', 'module_basename', '_MSG',
           '_MSG_CALLABLE']

from types import ModuleType
import sys
try:
    from importlib._bootstrap import _ImportLockContext
except ImportError:
    # Python 2 doesn't have the context manager. Roll it ourselves (copied from
    # Python 3's importlib/_bootstrap.py)
    import imp
    class _ImportLockContext:
        """Context manager for the import lock."""
        def __enter__(self):
            imp.acquire_lock()
        def __exit__(self, exc_type, exc_value, exc_traceback):
            imp.release_lock()


# Adding a __spec__ doesn't really help. I'll leave the code here in case
# future python implementations start relying on it.
#try:
#    from importlib.machinery import ModuleSpec
#except ImportError:
#    ModuleSpec = None

import six
from six import raise_from
from six.moves import reload_module
# It is sometime useful to have access to the version number of a library.
# This is usually done through the __version__ special attribute.
# To make sure the version number is consistent between setup.py and the
# library, we read the version number from the file called VERSION that stays
# in the module directory.
import os
VERSION_FILE = os.path.join(os.path.dirname(__file__), 'VERSION')
with open(VERSION_FILE) as infile:
    __version__ = infile.read().strip()

# Logging
import logging
# adding a TRACE level for stack debugging
_layz_TRACE = 1
logging.addLevelName(1, "layz_TRACE")
logging.basicConfig(level=logging.WARNING)
# Logs a formatted stack (takes no message or args/kwargs)
def _layz_trace(self):
    if self.isEnabledFor(_layz_TRACE):
        import traceback
        self._log(_layz_TRACE, " ### STACK TRACE ###", ())
        for line in traceback.format_stack(sys._getframe(2)):
            for subline in line.split("\n"):
                self._log(_layz_TRACE, subline.rstrip(), ())
logging.Logger.layz_trace = _layz_trace
logger = logging.getLogger(__name__)

################################
# Module/function registration #
################################

#### layz classes ####

class layzModule(ModuleType):
    """Class for lazily-loaded modules that triggers proper loading on access.

    Instantiation should be made from a subclass of :class:`layzModule`, with
    one subclass per instantiated module. Regular attribute set/access can then
    be recovered by setting the subclass's :meth:`__getattribute__` and
    :meth:`__setattribute__` to those of :class:`types.ModuleType`.
    """
    # peak.util.imports sets __slots__ to (), but it seems pointless because
    # the base ModuleType doesn't itself set __slots__.
    def __getattribute__(self, attr):
        logger.debug("Getting attr {} of layzModule instance of {}"
                     .format(attr, super(layzModule, self)
                             .__getattribute__("__name__")))
        logger.layz_trace()
        # IPython tries to be too clever and constantly inspects, asking for
        #  modules' attrs, which causes premature module loading and unesthetic
        #  internal errors if the lazily-loaded module doesn't exist.
        if (run_from_ipython()
            and (attr.startswith(("__", "_ipython"))
                 or attr == "_repr_mimebundle_")
            and module_basename(_caller_name()) in ('inspect', 'IPython')):
                logger.debug("Ignoring request for {}, deemed from IPython's "
                             "inspection.".format(super(layzModule, self)
                                     .__getattribute__("__name__"), attr))
                raise AttributeError
        if not attr in ('__name__','__class__','__spec__'):
            # __name__ and __class__ yield their values from the layzModule;
            # __spec__ causes an AttributeError. Maybe in the future it will be
            # necessary to return an actual ModuleSpec object, but it works as
            # it is without that now.

            # If it's an already-loaded submodule, we return it without
            # triggering a full loading
            try:
                return sys.modules[self.__name__+"."+attr]
            except KeyError:
                pass
            # Check if it's one of the layz callables
            try:
                _callable = type(self)._layz_import_callables[attr]
                logger.debug("Returning layz-callable '{}'.".format(attr))
                return _callable
            except (AttributeError, KeyError) as err:
                logger.debug("Proceeding to load module {}, "
                             "from requested value {}"
                             .format(super(layzModule, self)
                                     .__getattribute__("__name__"), attr))
                _load_module(self)
        logger.debug("Returning value '{}'.".format(super(layzModule, self)
                                     .__getattribute__(attr)))
        return super(layzModule, self).__getattribute__(attr)

    def __setattr__(self, attr, value):
        logger.debug("Setting attr {} to value {}, in layzModule instance "
                     "of {}".format(attr, value, super(layzModule, self)
                                    .__getattribute__("__name__")))
        _load_module(self)
        return super(layzModule, self).__setattr__(attr, value)


class layzCallable(object):
    """Class for lazily-loaded callables that triggers module loading on access

    """
    def __init__(self, *args):
        if len(args) != 2:
            # Maybe the user tried to base a class off this layz callable?
            try:
                logger.debug("Got wrong number of args when init'ing "
                             "layzCallable. args is '{}'".format(args))
                base = args[1][0]
                if isinstance(base, layzCallable) and len(args) == 3:
                    raise NotImplementedError("It seems you are trying to use "
                                              "a layz callable as a class "
                                              "base. This is not supported.")
            except (IndexError, TypeError):
                raise_from(TypeError("layzCallable takes exactly 2 arguments: "
                                "a module/layz module object and the name of "
                                "a callable to be lazily loaded."), None)
        self.module, self.cname = args
        self.modclass = type(self.module)
        self.callable = None
        # Need to save these, since the module-loading gets rid of them
        self.error_msgs = self.modclass._layz_import_error_msgs
        self.error_strings = self.modclass._layz_import_error_strings

    def __call__(self, *args, **kwargs):
        # No need to go through all the reloading more than once.
        if self.callable:
            return self.callable(*args, **kwargs)
        try:
            del self.modclass._layz_import_callables[self.cname]
        except (AttributeError, KeyError):
            pass
        try:
            self.callable = getattr(self.module, self.cname)
        except AttributeError:
            msg = self.error_msgs['msg_callable']
            raise_from(AttributeError(
                msg.format(callable=self.cname, **self.error_strings)), None)
        except ImportError as err:
            # Import failed. We reset the dict and re-raise the ImportError.
            try:
                self.modclass._layz_import_callables[self.cname] = self
            except AttributeError:
                self.modclass._layz_import_callables = {self.cname: self}
            raise_from(err, None)
        else:
            return self.callable(*args, **kwargs)


### Functions ###

def layz_module(modname, error_strings=None, layz_mod_class=layzModule,
                  level='leaf'):
    """Function allowing layz importing of a module into the namespace.

    A layz module object is created, registered in `sys.modules`, and
    returned. This is a hollow module; actual loading, and `ImportErrors` if
    not found, are delayed until an attempt is made to access attributes of the
    layz module.

    A handy application is to use :func:`layz_module` early in your own code
    (say, in `__init__.py`) to register all modulenames you want to be layz.
    Because of registration in `sys.modules` later invocations of
    `import modulename` will also return the layz object. This means that after
    initial registration the rest of your code can use regular pyhon import
    statements and retain the layzness of the modules.

    Parameters
    ----------
    modname : str
         The module to import.
    error_strings : dict, optional
         A dictionary of strings to use when module-loading fails. Key 'msg'
         sets the message to use (defaults to :attr:`layz_import._MSG`). The
         message is formatted using the remaining dictionary keys. The default
         message informs the user of which module is missing (key 'module'),
         what code loaded the module as layz (key 'caller'), and which package
         should be installed to solve the dependency (key 'install_name').
         None of the keys is mandatory and all are given smart names by default.
    layz_mod_class: type, optional
         Which class to use when instantiating the layz module, to allow
         deep customization. The default is :class:`layzModule` and custom
         alternatives **must** be a subclass thereof.
    level : str, optional
         Which submodule reference to return. Either a reference to the 'leaf'
         module (the default) or to the 'base' module. This is useful if you'll
         be using the module functionality in the same place you're calling
         :func:`layz_module` from, since then you don't need to run `import`
         again. Setting *level* does not affect which names/modules get
         registered in `sys.modules`.
         For *level* set to 'base' and *modulename* 'aaa.bbb.ccc'::

            aaa = layz_import.layz_module("aaa.bbb.ccc", level='base')
            # 'aaa' becomes defined in the current namespace, with
            #  (sub)attributes 'aaa.bbb' and 'aaa.bbb.ccc'.
            # It's the layz equivalent to:
            import aaa.bbb.ccc

        For *level* set to 'leaf'::

            ccc = layz_import.layz_module("aaa.bbb.ccc", level='leaf')
            # Only 'ccc' becomes set in the current namespace.
            # layz equivalent to:
            from aaa.bbb import ccc

    Returns
    -------
    module
        The module specified by *modname*, or its base, depending on *level*.
        The module isn't immediately imported. Instead, an instance of
        *layz_mod_class* is returned. Upon access to any of its attributes, the
        module is finally loaded.

    Examples
    --------
    >>> import layz_import, sys
    >>> np = layz_import.layz_module("numpy")
    >>> np
    Lazily-loaded module numpy
    >>> np is sys.modules['numpy']
    True
    >>> np.pi # This causes the full loading of the module ...
    3.141592653589793
    >>> np # ... and the module is changed in place. 
    <module 'numpy' from '/usr/local/lib/python/site-packages/numpy/__init__.py'>

    >>> import layz_import, sys
    >>> # The following succeeds even when asking for a module that's not available
    >>> missing = layz_import.layz_module("missing_module")
    >>> missing
    Lazily-loaded module missing_module
    >>> missing is sys.modules['missing_module']
    True
    >>> missing.some_attr # This causes the full loading of the module, which now fails.
    ImportError: __main__ attempted to use a functionality that requires module missing_module, but it couldn't be loaded. Please install missing_module and retry.

    See Also
    --------
    :func:`layz_callable`
    :class:`layzModule`

    """
    if error_strings is None:
        error_strings = {}
    _set_default_errornames(modname, error_strings)

    mod = _layz_module(modname, error_strings, layz_mod_class)
    if level == 'base':
        return sys.modules[module_basename(modname)]
    elif level == 'leaf':
        return mod
    else:
        raise ValueError("Parameter 'level' must be one of ('base', 'leaf')")


def _layz_module(modname, error_strings, layz_mod_class):
    with _ImportLockContext():
        fullmodname = modname
        fullsubmodname = None
        # ensure parent module/package is in sys.modules
        # and parent.modname=module, as soon as the parent is imported   
        while modname:
            try:
                mod = sys.modules[modname]
                # We reached a (base) module that's already loaded. Let's stop
                # the cycle. Can't use 'break' because we still want to go 
                # through the fullsubmodname check below.
                modname = ''
            except KeyError:
                err_s = error_strings.copy()
                err_s.setdefault('module', modname)

                class _layzModule(layz_mod_class):
                    _layz_import_error_msgs = {'msg': err_s.pop('msg')}
                    try:
                        _layz_import_error_msgs['msg_callable'] = \
                                err_s.pop('msg_callable')
                    except KeyError:
                        pass
                    _layz_import_error_strings = err_s
                    _layz_import_callables = {}
                    _layz_import_submodules = {}

                    def __repr__(self):
                        return "Lazily-loaded module {}".format(self.__name__)
                # A bit of cosmetic, to make AttributeErrors read more natural  
                _layzModule.__name__ = 'module'
                # Actual module instantiation
                mod = sys.modules[modname] = _layzModule(modname)
                # No need for __spec__. Maybe in the future.
                #if ModuleSpec:
                #    ModuleType.__setattr__(mod, '__spec__',
                #            ModuleSpec(modname, None))
            if fullsubmodname:
                submod = sys.modules[fullsubmodname]
                ModuleType.__setattr__(mod, submodname, submod)
                _layzModule._layz_import_submodules[submodname] = submod
            fullsubmodname = modname
            modname, _, submodname = modname.rpartition('.')
        return sys.modules[fullmodname]


def layz_callable(modname, *names, **kwargs):
    """Performs layz importing of one or more callables.

    :func:`layz_callable` creates functions that are thin wrappers that pass
    any and all arguments straight to the target module's callables. These can
    be functions or classes. The full loading of that module is only actually
    triggered when the returned layz function itself is called. This layz
    import of the target module uses the same mechanism as
    :func:`layz_module`.
    
    If, however, the target module has already been fully imported prior
    to invocation of :func:`layz_callable`, then the target callables
    themselves are returned and no layz imports are made.

    :func:`layz_function` and :func:`layz_function` are aliases of
    :func:`layz_callable`.

    Parameters
    ----------
    modname : str
         The base module from where to import the callable(s) in *names*,
         or a full 'module_name.callable_name' string.
    names : str (optional)
         The callable name(s) to import from the module specified by *modname*.
         If left empty, *modname* is assumed to also include the callable name
         to import.
    error_strings : dict, optional
         A dictionary of strings to use when reporting loading errors (either a
         missing module, or a missing callable name in the loaded module).
         *error_string* follows the same usage as described under
         :func:`layz_module`, with the exceptions that 1) a further key,
         'msg_callable', can be supplied to be used as the error when a module
         is successfully loaded but the target callable can't be found therein
         (defaulting to :attr:`layz_import._MSG_CALLABLE`); 2) a key 'callable'
         is always added with the callable name being loaded.
    layz_mod_class : type, optional
         See definition under :func:`layz_module`.
    layz_call_class : type, optional
         Analogously to *layz_mod_class*, allows setting a custom class to
         handle layz callables, other than the default :class:`layzCallable`.

    Returns
    -------
    wrapper function or tuple of wrapper functions
        If *names* is passed, returns a tuple of wrapper functions, one for
        each element in *names*.
        If only *modname* is passed it is assumed to be a full
        'module_name.callable_name' string, in which case the wrapper for the
        imported callable is returned directly, and not in a tuple.
        
    Notes
    -----
    Unlike :func:`layz_module`, which returns a layz module that eventually
    mutates into the fully-functional version, :func:`layz_callable` only
    returns thin wrappers that never change. This means that the returned
    wrapper object never truly becomes the one under the module's namespace,
    even after successful loading of the module in *modname*. This is fine for
    most practical use cases, but may break code that relies on the usage of
    the returned objects oter than calling them. One such example is the layz
    import of a class: it's fine to use the returned wrapper to instantiate an
    object, but it can't be used, for instance, to subclass from.

    Examples
    --------
    >>> import layz_import, sys
    >>> fn = layz_import.layz_callable("numpy.arange")
    >>> sys.modules['numpy']
    Lazily-loaded module numpy
    >>> fn(10)
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> sys.modules['numpy']
    <module 'numpy' from '/usr/local/lib/python3.5/site-packages/numpy/__init__.py'>

    >>> import layz_import, sys
    >>> cl = layz_import.layz_callable("numpy.ndarray") # a class
    >>> obj = cl([1, 2]) # This works OK (and also triggers the loading of numpy)
    >>> class MySubclass(cl): # This fails because cls is just a wrapper,
    >>>     pass              #  not an actual class.

    See Also
    --------
    :func:`layz_module`
    :class:`layzCallable`
    :class:`layzModule`

    """
    if not names:
        modname, _, name = modname.rpartition(".")
    layz_mod_class = _setdef(kwargs, 'layz_mod_class', layzModule)
    layz_call_class = _setdef(kwargs, 'layz_call_class', layzCallable)
    error_strings = _setdef(kwargs, 'error_strings', {})
    _set_default_errornames(modname, error_strings, call=True)

    if not names:
        # We allow passing a single string as 'modname.callable_name',
        # in which case the wrapper is returned directly and not as a list.
        return _layz_callable(modname, name, error_strings.copy(),
                                layz_mod_class, layz_call_class)
    return tuple(_layz_callable(modname, cname, error_strings.copy(),
                        layz_mod_class, layz_call_class) for cname in names)

layz_function = layz_class = layz_callable

def _layz_callable(modname, cname, error_strings,
                     layz_mod_class, layz_call_class):
    # We could do most of this in the layzCallable __init__, but here we can
    # pre-check whether to actually be layz or not.
    module = _layz_module(modname, error_strings, layz_mod_class)
    modclass = type(module)
    if (issubclass(modclass, layzModule) and
        hasattr(modclass, '_layz_import_callables')):
        modclass._layz_import_callables.setdefault(
            cname, layz_call_class(module, cname))
    return getattr(module, cname)


#######################
# Real module loading #
#######################

def _load_module(module):
    """Ensures that a module, and its parents, are properly loaded

    """
    modclass = type(module)
    # We only take care of our own layzModule instances
    if not issubclass(modclass, layzModule):
        raise TypeError("Passed module is not a layzModule instance.")
    with _ImportLockContext():
        parent, _, modname = module.__name__.rpartition('.')
        logger.debug("loading module {}".format(modname))
        # We first identify whether this is a loadable layzModule, then we
        # strip as much of layz_import behavior as possible (keeping it cached,
        # in case loading fails and we need to reset the layz state).
        if not hasattr(modclass, '_layz_import_error_msgs'):
            # Alreay loaded (no _layz_import_error_msgs attr). Not reloading.
            return
        # First, ensure the parent is loaded (using recursion; *very* unlikely
        # we'll ever hit a stack limit in this case).
        modclass._LOADING = True
        try:
            if parent:
                logger.debug("first loading parent module {}".format(parent))
                setattr(sys.modules[parent], modname, module)
            if not hasattr(modclass, '_LOADING'):
                logger.debug("Module {} already loaded by the parent"
                             .format(modname))
                # We've been loaded by the parent. Let's bail.
                return
            cached_data = _clean_layzmodule(module)
            try:
                # Get Python to do the real import!
                reload_module(module)           
            except:
                # Loading failed. We reset our layz state.
                logger.debug("Failed to load module {}. Resetting..."
                             .format(modname))
                _reset_layzmodule(module, cached_data)
                raise
            else:
                # Successful load
                logger.debug("Successfully loaded module {}".format(modname))
                delattr(modclass, '_LOADING')
                _reset_layz_submod_refs(module)

        except (AttributeError, ImportError) as err:
            logger.debug("Failed to load {}.\n{}: {}"
                         .format(modname, err.__class__.__name__, err))
            logger.layz_trace()
            # Under Python 3 reloading our dummy layzModule instances causes an
            # AttributeError if the module can't be found. Would be preferrable
            # if we could always rely on an ImportError. As it is we vet the
            # AttributeError as thoroughly as possible.
            if ((six.PY3 and isinstance(err, AttributeError)) and not
                err.args[0] == "'NoneType' object has no attribute 'name'"):
                # Not the AttributeError we were looking for.
                raise
            msg = modclass._layz_import_error_msgs['msg']
            raise_from(ImportError(
                msg.format(**modclass._layz_import_error_strings)), None)


##############################
# Helper functions/constants #
##############################

_MSG = ("{caller} attempted to use a functionality that requires module "
        "{module}, but it couldn't be loaded. Please install {install_name} "
        "and retry.")

_MSG_CALLABLE = ("{caller} attempted to use a functionality that requires "
           "{callable}, of module {module}, but it couldn't be found in that "
           "module. Please install a version of {install_name} that has "
           "{module}.{callable} and retry.")

_CLS_ATTRS = ("_layz_import_error_strings", "_layz_import_error_msgs",
              "_layz_import_callables", "_layz_import_submodules", "__repr__")

_DELETION_DICT = ("_layz_import_submodules",)

def _setdef(argdict, name, defaultvalue):
    """Like dict.setdefault but sets the default value also if None is present.

    """
    if not name in argdict or argdict[name] is None:
        argdict[name] = defaultvalue
    return argdict[name]


def module_basename(modname):
    return modname.partition('.')[0]


def _set_default_errornames(modname, error_strings, call=False):
    # We don't set the modulename default here because it will change for
    # parents of lazily imported submodules.
    error_strings.setdefault('caller', _caller_name(3, default='Python'))
    error_strings.setdefault('install_name', module_basename(modname))
    error_strings.setdefault('msg', _MSG)
    if call:
        error_strings.setdefault('msg_callable', _MSG_CALLABLE)


def _caller_name(depth=2, default=''):
    """Returns the name of the calling namespace.

    """
    # the presence of sys._getframe might be implementation-dependent.
    # It isn't that serious if we can't get the caller's name.
    try:
        return sys._getframe(depth).f_globals['__name__']
    except AttributeError:
        return default


def _clean_layzmodule(module):
    """Removes all layz behavior from a module's class, for loading.

    Also removes all module attributes listed under the module's class deletion
    dictionaries. Deletion dictionaries are class attributes with names
    specified in `_DELETION_DICT`.

    Parameters
    ----------
    module: layzModule 

    Returns
    -------
    dict
        A dictionary of deleted class attributes, that can be used to reset the
        layz state using :func:`_reset_layzmodule`.
    """
    modclass = type(module)
    _clean_layz_submod_refs(module)

    modclass.__getattribute__ = ModuleType.__getattribute__
    modclass.__setattr__ = ModuleType.__setattr__
    cls_attrs = {}
    for cls_attr in _CLS_ATTRS:
        try:
            cls_attrs[cls_attr] = getattr(modclass, cls_attr)
            delattr(modclass, cls_attr)
        except AttributeError:
            pass
    return cls_attrs


def _clean_layz_submod_refs(module):
    modclass = type(module)
    for deldict in _DELETION_DICT:
        try:
            delnames = getattr(modclass, deldict)
        except AttributeError:
            continue
        for delname in delnames:
            try:
                super(layzModule, module).__delattr__(delname)
            except AttributeError:
                # Maybe raise a warning?
                pass


def _reset_layzmodule(module, cls_attrs):
    """Resets a module's layz state from cached data.

    """
    modclass = type(module)
    del modclass.__getattribute__
    del modclass.__setattr__
    try:
        del modclass._LOADING
    except AttributeError:
        pass
    for cls_attr in _CLS_ATTRS:
        try:
            setattr(modclass, cls_attr, cls_attrs[cls_attr])
        except KeyError:
            pass
    _reset_layz_submod_refs(module)


def _reset_layz_submod_refs(module):
    modclass = type(module)
    for deldict in _DELETION_DICT:
        try:
            resetnames = getattr(modclass, deldict)
        except AttributeError:
            continue
        for name, submod in resetnames.items(): 
            super(layzModule, module).__setattr__(name, submod)


def run_from_ipython():
    # Taken from https://stackoverflow.com/questions/5376837
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

