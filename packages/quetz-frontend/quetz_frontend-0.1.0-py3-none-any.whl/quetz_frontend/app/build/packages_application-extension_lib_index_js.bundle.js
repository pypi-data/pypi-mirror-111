(self["webpackChunk_quetz_frontend_app"] = self["webpackChunk_quetz_frontend_app"] || []).push([["packages_application-extension_lib_index_js"],{

/***/ "../../packages/application-extension/lib/index.js":
/*!*********************************************************!*\
  !*** ../../packages/application-extension/lib/index.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _paths__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./paths */ "../../packages/application-extension/lib/paths.js");
/* harmony import */ var _router__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./router */ "../../packages/application-extension/lib/router.js");
/* harmony import */ var _sessions__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./sessions */ "../../packages/application-extension/lib/sessions.js");
/* harmony import */ var _translator__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./translator */ "../../packages/application-extension/lib/translator.js");




const ros = [_paths__WEBPACK_IMPORTED_MODULE_0__.paths, _router__WEBPACK_IMPORTED_MODULE_1__.router, _sessions__WEBPACK_IMPORTED_MODULE_2__.sessions, _translator__WEBPACK_IMPORTED_MODULE_3__.translator];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ros);
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../../packages/application-extension/lib/paths.js":
/*!*********************************************************!*\
  !*** ../../packages/application-extension/lib/paths.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "paths": () => (/* binding */ paths)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);

var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/application-extension:paths';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default paths.
 */
const paths = {
    id: CommandIDs.plugin,
    autoStart: true,
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths,
    activate: (app) => {
        return app.paths;
    },
};
//# sourceMappingURL=paths.js.map

/***/ }),

/***/ "../../packages/application-extension/lib/router.js":
/*!**********************************************************!*\
  !*** ../../packages/application-extension/lib/router.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "router": () => (/* binding */ router)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);

var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/application-extension:router';
})(CommandIDs || (CommandIDs = {}));
const router = {
    id: CommandIDs.plugin,
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.JupyterFrontEnd.IPaths],
    provides: _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter,
    activate: (app, paths) => {
        const { commands } = app;
        const router = new _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.Router({ base: '/', commands });
        void app.started.then(() => {
            if (router.current.path === router.base) {
                router.navigate('/home', { skipRouting: true });
            }
            void router.route();
            // Route all pop state events.
            window.addEventListener('popstate', () => {
                void router.route();
            });
            router.routed.connect((router, loc) => {
                if (loc.path === router.base) {
                    router.navigate('/home');
                }
            });
            //@ts-ignore
            window.router = router;
        });
        return router;
    },
};
//# sourceMappingURL=router.js.map

/***/ }),

/***/ "../../packages/application-extension/lib/sessions.js":
/*!************************************************************!*\
  !*** ../../packages/application-extension/lib/sessions.js ***!
  \************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "sessions": () => (/* binding */ sessions)
/* harmony export */ });
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/application-extension:sessions';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin to stop the kernels, sessions and terminals polling
 */
const sessions = {
    id: CommandIDs.plugin,
    autoStart: true,
    activate: (app) => {
        var _a, _b;
        (_a = app.serviceManager.sessions) === null || _a === void 0 ? void 0 : _a.ready.then((value) => {
            var _a;
            // stop polling the kernel sessions
            (_a = app.serviceManager.sessions['_kernelManager']['_pollModels']) === null || _a === void 0 ? void 0 : _a.stop();
            // stop polling the sessions
            void app.serviceManager.sessions['_pollModels'].stop();
        });
        (_b = app.serviceManager.kernelspecs) === null || _b === void 0 ? void 0 : _b.ready.then((value) => {
            // stop polling the kernelspecs
            void app.serviceManager.kernelspecs.dispose();
        });
        /*
        app.serviceManager.terminals?.ready.then( value => {
          console.debug("Stopping terminals:");
          // stop polling the terminals
          void app.serviceManager.terminals['_pollModels'].stop();
        });
        */
    },
};
//# sourceMappingURL=sessions.js.map

/***/ }),

/***/ "../../packages/application-extension/lib/translator.js":
/*!**************************************************************!*\
  !*** ../../packages/application-extension/lib/translator.js ***!
  \**************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "translator": () => (/* binding */ translator)
/* harmony export */ });
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__);

var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/application-extension:translator';
})(CommandIDs || (CommandIDs = {}));
/**
 * A simplified Translator
 */
const translator = {
    id: CommandIDs.plugin,
    autoStart: true,
    provides: _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.ITranslator,
    activate: (app) => {
        const translationManager = new _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_0__.TranslationManager();
        return translationManager;
    },
};
//# sourceMappingURL=translator.js.map

/***/ })

}]);
//# sourceMappingURL=packages_application-extension_lib_index_js.bundle.js.map