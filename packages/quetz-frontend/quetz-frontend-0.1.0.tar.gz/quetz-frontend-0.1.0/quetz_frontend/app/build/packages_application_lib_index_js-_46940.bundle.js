(self["webpackChunk_quetz_frontend_app"] = self["webpackChunk_quetz_frontend_app"] || []).push([["packages_application_lib_index_js-_46940"],{

/***/ "../../packages/application/lib/app.js":
/*!*********************************************!*\
  !*** ../../packages/application/lib/app.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "App": () => (/* binding */ App)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _shell__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./shell */ "../../packages/application/lib/shell.js");



/**
 * App is the main application class. It is instantiated once and shared.
 */
class App extends _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd {
    /**
     * Construct a new App object.
     *
     * @param options The instantiation options for an application.
     */
    constructor(options = { shell: new _shell__WEBPACK_IMPORTED_MODULE_2__.Shell() }) {
        super({
            shell: options.shell,
        });
        /**
         * The name of the application.
         */
        this.name = 'Quetz';
        /**
         * A namespace/prefix plugins may use to denote their provenance.
         */
        this.namespace = this.name;
        /**
         * The version of the application.
         */
        this.version = 'unknown';
    }
    /**
     * The JupyterLab application paths dictionary.
     */
    get paths() {
        return {
            urls: {
                base: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('baseUrl'),
                notFound: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('notFoundUrl'),
                app: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('appUrl'),
                static: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('staticUrl'),
                settings: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('settingsUrl'),
                themes: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('themesUrl'),
                doc: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('docUrl'),
                translations: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('translationsApiUrl'),
                hubHost: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('hubHost') || undefined,
                hubPrefix: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('hubPrefix') || undefined,
                hubUser: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('hubUser') || undefined,
                hubServerName: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('hubServerName') || undefined,
            },
            directories: {
                appSettings: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('appSettingsDir'),
                schemas: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('schemasDir'),
                static: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('staticDir'),
                templates: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('templatesDir'),
                themes: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('themesDir'),
                userSettings: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('userSettingsDir'),
                serverRoot: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('serverRoot'),
                workspaces: _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getOption('workspacesDir'),
            },
        };
    }
    /**
     * Register plugins from a plugin module.
     *
     * @param mod - The plugin module to register.
     */
    registerPluginModule(mod) {
        let data = mod.default;
        // Handle commonjs exports.
        if (!Object.prototype.hasOwnProperty.call(mod, '__esModule')) {
            data = mod;
        }
        if (!Array.isArray(data)) {
            data = [data];
        }
        data.forEach((item) => {
            try {
                this.registerPlugin(item);
            }
            catch (error) {
                console.error(error);
            }
        });
    }
    /**
     * Register the plugins from multiple plugin modules.
     *
     * @param mods - The plugin modules to register.
     */
    registerPluginModules(mods) {
        mods.forEach((mod) => {
            this.registerPluginModule(mod);
        });
    }
}
//# sourceMappingURL=app.js.map

/***/ }),

/***/ "../../packages/application/lib/index.js":
/*!***********************************************!*\
  !*** ../../packages/application/lib/index.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "App": () => (/* reexport safe */ _app__WEBPACK_IMPORTED_MODULE_0__.App),
/* harmony export */   "Shell": () => (/* reexport safe */ _shell__WEBPACK_IMPORTED_MODULE_1__.Shell)
/* harmony export */ });
/* harmony import */ var _app__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./app */ "../../packages/application/lib/app.js");
/* harmony import */ var _shell__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./shell */ "../../packages/application/lib/shell.js");


//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../../packages/application/lib/shell.js":
/*!***********************************************!*\
  !*** ../../packages/application/lib/shell.js ***!
  \***********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Shell": () => (/* binding */ Shell)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging/@lumino/messaging");
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_messaging__WEBPACK_IMPORTED_MODULE_3__);




/**
 * The default rank for ranked panels.
 */
const DEFAULT_RANK = 900;
/**
 * The application shell.
 */
class Shell extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor() {
        super();
        this.id = 'main';
        const rootLayout = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.BoxLayout();
        this._top = new Private.PanelHandler();
        this._main = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel();
        this._top.panel.id = 'top-panel';
        this._main.id = 'main-panel';
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.BoxLayout.setStretch(this._top.panel, 0);
        _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.BoxLayout.setStretch(this._main, 1);
        // this._main.spacing = 5;
        rootLayout.spacing = 0;
        rootLayout.addWidget(this._top.panel);
        rootLayout.addWidget(this._main);
        this.layout = rootLayout;
    }
    activateById(id) {
        // no-op
    }
    /**
     * Add a widget to the application shell.
     *
     * @param widget - The widget being added.
     * @param area - Optional region in the shell into which the widget should
     * be added.
     * @param options
     */
    add(widget, area, options) {
        var _a;
        const rank = (_a = options === null || options === void 0 ? void 0 : options.rank) !== null && _a !== void 0 ? _a : DEFAULT_RANK;
        if (area === 'top') {
            return this._top.addWidget(widget, rank);
        }
        if (area === 'main' || area === undefined) {
            // if (this._main.widgets.length > 0) {
            //   // do not add the widget if there is already one
            //   return;
            // }
            this._addToMainArea(widget);
        }
        return;
    }
    /**
     * The current widget in the shell's main area.
     */
    get currentWidget() {
        // TODO: use a focus tracker to return the current widget
        return this._main.widgets[0];
    }
    /**
     * Get the top area wrapper panel
     */
    get top() {
        return this._topWrapper;
    }
    widgets(area) {
        if (area === 'top') {
            return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.iter)(this._top.panel.widgets);
        }
        return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.iter)(this._main.widgets);
    }
    /**
     * Add a widget to the main content area.
     *
     * @param widget The widget to add.
     */
    _addToMainArea(widget) {
        if (!widget.id) {
            console.error('Widgets added to the app shell must have unique id property.');
            return;
        }
        const dock = this._main;
        const { title } = widget;
        title.dataset = Object.assign(Object.assign({}, title.dataset), { id: widget.id });
        if (title.icon instanceof _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon) {
            // bind an appropriate style to the icon
            title.icon = title.icon.bindprops({
                stylesheet: 'mainAreaTab',
            });
        }
        else if (typeof title.icon === 'string' || !title.icon) {
            // add some classes to help with displaying css background imgs
            title.iconClass = (0,_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.classes)(title.iconClass, 'jp-Icon');
        }
        if (dock.widgets.length) {
            dock.widgets[0].dispose();
        }
        dock.addWidget(widget);
    }
}
var Private;
(function (Private) {
    /**
     * A less-than comparison function for side bar rank items.
     *
     * @param first
     * @param second
     */
    function itemCmp(first, second) {
        return first.rank - second.rank;
    }
    Private.itemCmp = itemCmp;
    /**
     * A class which manages a panel and sorts its widgets by rank.
     */
    class PanelHandler {
        constructor() {
            /**
             * A message hook for child add/remove messages on the main area dock panel.
             *
             * @param handler
             * @param msg
             */
            this._panelChildHook = (handler, msg) => {
                switch (msg.type) {
                    case 'child-added':
                        {
                            const widget = msg.child;
                            // If we already know about this widget, we're done
                            if (this._items.find((v) => v.widget === widget)) {
                                break;
                            }
                            // Otherwise, add to the end by default
                            const rank = this._items[this._items.length - 1].rank;
                            this._items.push({ widget, rank });
                        }
                        break;
                    case 'child-removed':
                        {
                            const widget = msg.child;
                            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.removeFirstWhere(this._items, (v) => v.widget === widget);
                        }
                        break;
                    default:
                        break;
                }
                return true;
            };
            this._items = new Array();
            this._panel = new _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Panel();
            _lumino_messaging__WEBPACK_IMPORTED_MODULE_3__.MessageLoop.installMessageHook(this._panel, this._panelChildHook);
        }
        /**
         * Get the panel managed by the handler.
         */
        get panel() {
            return this._panel;
        }
        /**
         * Add a widget to the panel.
         *
         * If the widget is already added, it will be moved.
         *
         * @param widget
         * @param rank
         */
        addWidget(widget, rank) {
            widget.parent = null;
            const item = { widget, rank };
            const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.upperBound(this._items, item, Private.itemCmp);
            _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.insert(this._items, index, item);
            this._panel.insertWidget(index, widget);
        }
    }
    Private.PanelHandler = PanelHandler;
})(Private || (Private = {}));
//# sourceMappingURL=shell.js.map

/***/ })

}]);
//# sourceMappingURL=packages_application_lib_index_js-_46940.bundle.js.map