(self["webpackChunk_quetz_frontend_app"] = self["webpackChunk_quetz_frontend_app"] || []).push([["packages_menu_lib_index_js"],{

/***/ "../../packages/menu/lib/index.js":
/*!****************************************!*\
  !*** ../../packages/menu/lib/index.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MainMenu": () => (/* reexport safe */ _menu__WEBPACK_IMPORTED_MODULE_0__.MainMenu),
/* harmony export */   "ILogInMenu": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_1__.ILogInMenu),
/* harmony export */   "IMainMenu": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_1__.IMainMenu)
/* harmony export */ });
/* harmony import */ var _menu__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./menu */ "../../packages/menu/lib/menu.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../../packages/menu/lib/tokens.js");


//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../../packages/menu/lib/menu.js":
/*!***************************************!*\
  !*** ../../packages/menu/lib/menu.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MainMenu": () => (/* binding */ MainMenu)
/* harmony export */ });
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging/@lumino/messaging");
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_messaging__WEBPACK_IMPORTED_MODULE_2__);



/**
 * The main menu.
 */
class MainMenu extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_1__.Panel {
    /**
     * Construct the main menu bar.
     */
    constructor() {
        super();
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
                        _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.removeFirstWhere(this._items, (v) => v.widget === widget);
                    }
                    break;
                default:
                    break;
            }
            return true;
        };
        this._items = new Array();
        this.id = 'main-menu';
        this.addClass('topbar-item');
        _lumino_messaging__WEBPACK_IMPORTED_MODULE_2__.MessageLoop.installMessageHook(this, this._panelChildHook);
    }
    addItem(widget, rank) {
        widget.parent = null;
        widget.addClass('topbar-item-content');
        const item = { widget, rank };
        const index = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.upperBound(this._items, item, Private.itemCmp);
        _lumino_algorithm__WEBPACK_IMPORTED_MODULE_0__.ArrayExt.insert(this._items, index, item);
        this.insertWidget(index, widget);
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
})(Private || (Private = {}));
//# sourceMappingURL=menu.js.map

/***/ }),

/***/ "../../packages/menu/lib/tokens.js":
/*!*****************************************!*\
  !*** ../../packages/menu/lib/tokens.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMainMenu": () => (/* binding */ IMainMenu),
/* harmony export */   "ILogInMenu": () => (/* binding */ ILogInMenu)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The main menu token.
 */
const IMainMenu = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('quetz/topBar:IMainMenu');
/**
 * The main menu token.
 */
const ILogInMenu = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('quetz/topBar:ILogInMenu');
//# sourceMappingURL=tokens.js.map

/***/ })

}]);
//# sourceMappingURL=packages_menu_lib_index_js.bundle.js.map