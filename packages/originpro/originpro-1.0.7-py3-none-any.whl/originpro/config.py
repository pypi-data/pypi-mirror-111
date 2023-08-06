"""
originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation
"""
# pylint: disable=C0103,W0611
oext = False
_EXIT = [False]
_OBJS_COUNT = [0]
try:
    import PyOrigin as po
except ImportError:
    import OriginExt
    import atexit
    class APP:
        'OriginExt.Application() wrapper'
        def __init__(self):
            self._app = None
            self._first= True
        def __getattr__(self, name):
            if self._app is None:
                self._app = OriginExt.Application()
            return getattr(self._app, name)
        def Exit(self, releaseonly=False):
            'Exit if Application exists'
            if self._app is not None:
                self._app.Exit(releaseonly)
                self._app = None
        def Attach(self):
            'Attach to exising Origin instance'
            releaseonly = True
            if self._first:
                releaseonly = False
                self._first = False
            self.Exit(releaseonly)
            self._app = OriginExt.ApplicationSI()
    po = APP()
    oext = True
    def exit_handler():
        global _EXIT, _OBJS_COUNT
        _EXIT[0] = True
        if not _OBJS_COUNT[0]:
            po.Exit(True)
    atexit.register(exit_handler)
