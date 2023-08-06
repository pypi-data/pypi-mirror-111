(self["webpackChunk_quetz_frontend_app"] = self["webpackChunk_quetz_frontend_app"] || []).push([["packages_home-extension_lib_index_js-_24b00"],{

/***/ "../../packages/home-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../../packages/home-extension/lib/index.js ***!
  \**************************************************/
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
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @fortawesome/react-fontawesome */ "webpack/sharing/consume/default/@fortawesome/react-fontawesome/@fortawesome/react-fontawesome");
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @fortawesome/free-solid-svg-icons */ "webpack/sharing/consume/default/@fortawesome/free-solid-svg-icons/@fortawesome/free-solid-svg-icons");
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! react-tooltip */ "webpack/sharing/consume/default/react-tooltip/react-tooltip");
/* harmony import */ var react_tooltip__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(react_tooltip__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_9__);










var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/home-extension:home';
    CommandIDs.open = '@quetz-frontend/home-extension:home/open';
})(CommandIDs || (CommandIDs = {}));
const plugin = {
    id: CommandIDs.plugin,
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter],
    activate: (app, router) => {
        const { shell, commands } = app;
        commands.addCommand(CommandIDs.open, {
            execute: () => {
                shell.add(new Homepage(router), 'main');
            },
        });
        router.register({
            pattern: /home.*/,
            command: CommandIDs.open,
        });
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
class Homepage extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(router) {
        super();
        this.id = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.DOMUtils.createDomID();
        this.title.label = 'Home page';
        this._router = router;
    }
    _route(route) {
        this._router.navigate(route);
    }
    render() {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.URLExt.join(settings.baseUrl, '/api/channels');
        return (react__WEBPACK_IMPORTED_MODULE_9__.createElement("div", { className: "page-contents-width-limit" },
            react__WEBPACK_IMPORTED_MODULE_9__.createElement("h2", { className: "heading2" }, "Home"),
            react__WEBPACK_IMPORTED_MODULE_9__.createElement("div", { className: "flex" },
                react__WEBPACK_IMPORTED_MODULE_9__.createElement("h3", { className: "section-heading" }, "Recently updated channels"),
                "\u2003",
                react__WEBPACK_IMPORTED_MODULE_9__.createElement("p", { className: "minor-paragraph" },
                    react__WEBPACK_IMPORTED_MODULE_9__.createElement("a", { className: "link", onClick: () => this._route('/channels') }, "View all"))),
            react__WEBPACK_IMPORTED_MODULE_9__.createElement("div", { className: "padding-side" },
                react__WEBPACK_IMPORTED_MODULE_9__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.FetchHoc, { url: url, loadingMessage: "Fetching list of channels", genericErrorMessage: "Error fetching list of channels" }, (channels) => {
                    return channels.length > 0 ? (react__WEBPACK_IMPORTED_MODULE_9__.createElement(_quetz_frontend_table__WEBPACK_IMPORTED_MODULE_5__.List, { data: channels.slice(0, 5), columns: getChannelsListColumns(), to: (rowData) => this._route(`/channels/${rowData.name}`) })) : (react__WEBPACK_IMPORTED_MODULE_9__.createElement("p", { className: "paragraph" }, "No channels available"));
                }))));
    }
}
const getChannelsListColumns = () => [
    {
        Header: '',
        accessor: 'name',
        Cell: ({ row }) => (react__WEBPACK_IMPORTED_MODULE_9__.createElement(react__WEBPACK_IMPORTED_MODULE_9__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_9__.createElement("span", { "data-for": `tooltip-${row.original.name}`, "data-tip": row.original.private ? 'Private' : 'Public' },
                react__WEBPACK_IMPORTED_MODULE_9__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_6__.FontAwesomeIcon, { icon: row.original.private ? _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_7__.faUnlockAlt : _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_7__.faGlobeAmericas })),
            react__WEBPACK_IMPORTED_MODULE_9__.createElement((react_tooltip__WEBPACK_IMPORTED_MODULE_8___default()), { id: `tooltip-${row.original.name}`, place: "right", type: "dark", effect: "solid" }))),
        width: 5,
    },
    {
        Header: '',
        accessor: 'user.profile.name',
        Cell: ({ row }) => (react__WEBPACK_IMPORTED_MODULE_9__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_9__.createElement("p", { className: "text" }, row.original.name),
            react__WEBPACK_IMPORTED_MODULE_9__.createElement("p", { className: "minor-paragraph channel-list-description" }, row.original.description))),
        width: 45,
    },
    {
        Header: '',
        accessor: 'user.username',
        Cell: ({ row }) => (0,_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.formatPlural)(row.original.packages_count, 'package'),
        width: 35,
    },
    {
        Header: '',
        accessor: 'role',
        Cell: ({ row }) => (0,_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.formatPlural)(row.original.packages_count, 'member'),
        width: 20,
    },
];
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=packages_home-extension_lib_index_js-_24b00.bundle.js.map