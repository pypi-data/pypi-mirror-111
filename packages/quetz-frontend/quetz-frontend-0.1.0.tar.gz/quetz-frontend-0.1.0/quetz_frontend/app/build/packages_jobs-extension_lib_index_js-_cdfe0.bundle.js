(self["webpackChunk_quetz_frontend_app"] = self["webpackChunk_quetz_frontend_app"] || []).push([["packages_jobs-extension_lib_index_js-_cdfe0"],{

/***/ "../../packages/jobs-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../../packages/jobs-extension/lib/index.js ***!
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
/* harmony import */ var _quetz_frontend_menu__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @quetz-frontend/menu */ "webpack/sharing/consume/default/@quetz-frontend/menu/@quetz-frontend/menu");
/* harmony import */ var _quetz_frontend_menu__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_menu__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jobs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./jobs */ "../../packages/jobs-extension/lib/jobs.js");

//import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';

//import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
//import * as React from 'react';

//import Job from './job';
/**
 * The command ids used by the main plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.jobs = '@quetz-frontend:jobs';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main menu plugin.
 */
const plugin = {
    id: CommandIDs.jobs,
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _quetz_frontend_menu__WEBPACK_IMPORTED_MODULE_1__.ILogInMenu],
    activate: (app, router, menu) => {
        const { shell, commands } = app;
        commands.addCommand(CommandIDs.jobs, {
            execute: () => {
                shell.add(new _jobs__WEBPACK_IMPORTED_MODULE_2__.Jobs(), 'main');
            },
        });
        router.register({
            pattern: /jobs.*/,
            command: CommandIDs.jobs,
        });
        menu.addItem({
            id: CommandIDs.jobs,
            label: 'Jobs',
            icon: 'empty',
            api: '/jobs',
            loggedIn: true,
        });
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/*class JobsRouter extends ReactWidget {
  
  constructor() {
    super();
    this.id = DOMUtils.createDomID();;
    this.title.label = 'Jobs main page';
  }

  render(): React.ReactElement {
    return (
      <Router basename="/jobs">
        <Switch>
          <Route path="/:jobId" render={(props) => <Job {...props} />} />
          <Route path="" component={Jobs} />
          <Route path="*" component={Jobs} />
        </Switch>
      </Router>
    );
  }
} */
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../../packages/jobs-extension/lib/jobs.js":
/*!*************************************************!*\
  !*** ../../packages/jobs-extension/lib/jobs.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Jobs": () => (/* binding */ Jobs)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @quetz-frontend/apputils */ "webpack/sharing/consume/default/@quetz-frontend/apputils/@quetz-frontend/apputils");
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _quetz_frontend_table__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @quetz-frontend/table */ "webpack/sharing/consume/default/@quetz-frontend/table/@quetz-frontend/table");
/* harmony import */ var _quetz_frontend_table__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_table__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_5__);






/**
 *
 */
class Jobs extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor() {
        super();
        this.id = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.DOMUtils.createDomID();
        this.title.label = 'Jobs main page';
        this._data = new Array();
        this._status = _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.API_STATUSES.PENDING;
        this._loadData();
    }
    _loadData() {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, '/api/jobs');
        _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(url, {}, settings).then(async (resp) => {
            resp.json().then((data) => {
                /* TODO: Support pagination */
                this._data = data.result;
                this._status = _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.API_STATUSES.SUCCESS;
                this.update();
            });
        });
    }
    render() {
        const breadcrumbItems = [
            {
                text: 'Home',
                link: '/',
            },
            {
                text: 'Jobs',
            },
        ];
        return (react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { className: "page-contents-width-limit" },
            react__WEBPACK_IMPORTED_MODULE_5__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.Breadcrumbs, { items: breadcrumbItems }),
            react__WEBPACK_IMPORTED_MODULE_5__.createElement("h2", { className: "heading2" }, "Jobs"),
            this._status === _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.API_STATUSES.PENDING ? (react__WEBPACK_IMPORTED_MODULE_5__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.InlineLoader, { text: "Fetching jobs" })) : (react__WEBPACK_IMPORTED_MODULE_5__.createElement(_quetz_frontend_table__WEBPACK_IMPORTED_MODULE_4__.Table, { data: this._data, columns: getColumns(), enableSearch: true }))));
    }
}
const getColumns = () => [
    {
        Header: 'Manifest',
        accessor: 'manifest',
        disableFilters: true,
        Cell: ({ row }) => (
        //@ts-ignore
        react__WEBPACK_IMPORTED_MODULE_5__.createElement("div", { onClick: () => window.route.navigate(`/jobs/:${row.original.id}`) }, row.values.manifest)),
    },
    {
        Header: 'Created',
        accessor: 'created',
        Cell: ({ row }) => row.values.created,
    },
    {
        Header: 'Status',
        accessor: 'status',
        Cell: ({ row }) => row.values.status,
    },
    {
        Header: 'Owner',
        accessor: 'owner',
        Cell: ({ row }) => row.values.owner.username,
    },
];
//# sourceMappingURL=jobs.js.map

/***/ })

}]);
//# sourceMappingURL=packages_jobs-extension_lib_index_js-_cdfe0.bundle.js.map