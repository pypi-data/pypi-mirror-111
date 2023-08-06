(self["webpackChunk_quetz_frontend_app"] = self["webpackChunk_quetz_frontend_app"] || []).push([["packages_search-extension_lib_index_js-_93170"],{

/***/ "../../packages/search-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../../packages/search-extension/lib/index.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CommandIDs": () => (/* binding */ CommandIDs),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @quetz-frontend/apputils */ "webpack/sharing/consume/default/@quetz-frontend/apputils/@quetz-frontend/apputils");
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _quetz_frontend_table__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @quetz-frontend/table */ "webpack/sharing/consume/default/@quetz-frontend/table/@quetz-frontend/table");
/* harmony import */ var _quetz_frontend_table__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_table__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_6__);







/**
 * The command ids used by the main plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/search-extension:search';
    CommandIDs.open = '@quetz-frontend/search-extension:search/open';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main menu plugin.
 */
const plugin = {
    id: CommandIDs.plugin,
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter],
    activate: (app, router) => {
        const { shell, commands } = app;
        commands.addCommand(CommandIDs.open, {
            execute: () => {
                shell.add(new SearchPage(router), 'main');
            },
        });
        router.register({
            pattern: /search.*/,
            command: CommandIDs.open,
        });
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
class SearchPage extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(router) {
        super();
        this.id = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.DOMUtils.createDomID();
        this.title.label = 'Search page';
        this._router = router;
    }
    _route(route) {
        this._router.navigate(route);
    }
    render() {
        const searchText = new URLSearchParams(window.location.search).get('q');
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.URLExt.join(settings.baseUrl, `/api/packages/search/?q=${searchText}`);
        const breadcrumbItems = [
            {
                text: 'Home',
                link: '/',
            },
            {
                text: `Search for "${searchText}"`,
            },
        ];
        const columns = [
            {
                Header: 'Name',
                accessor: 'name',
                Cell: ({ row }) => (react__WEBPACK_IMPORTED_MODULE_6__.createElement(react__WEBPACK_IMPORTED_MODULE_6__.Fragment, null,
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("a", { className: "link", onClick: () => this._route(`/channels/${row.original.channel_name}`) }, row.original.channel_name),
                    "\u2003/\u2003",
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("a", { className: "link", onClick: () => this._route(`/channels/${row.original.channel_name}/packages/${row.values.name}`) }, row.values.name))),
            },
            {
                Header: 'Summary',
                accessor: 'summary',
            },
            {
                Header: 'Version',
                accessor: 'current_version',
                Cell: ({ row }) => (row.values.current_version || react__WEBPACK_IMPORTED_MODULE_6__.createElement("i", null, "n/a")),
            },
        ];
        return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "page-contents-width-limit" },
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("h2", { className: "heading2" }, "Packages"),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "flex" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.Breadcrumbs, { items: breadcrumbItems })),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "padding-side" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.FetchHoc, { url: url, loadingMessage: "Searching for packages", genericErrorMessage: "Error fetching API keys" }, (data) => {
                    return react__WEBPACK_IMPORTED_MODULE_6__.createElement(_quetz_frontend_table__WEBPACK_IMPORTED_MODULE_5__.Table, { columns: columns, data: data || [] });
                }))));
    }
}
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=packages_search-extension_lib_index_js-_93170.bundle.js.map