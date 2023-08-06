(self["webpackChunk_quetz_frontend_app"] = self["webpackChunk_quetz_frontend_app"] || []).push([["packages_user-extension_lib_index_js"],{

/***/ "../../packages/user-extension/lib/api-key.js":
/*!****************************************************!*\
  !*** ../../packages/user-extension/lib/api-key.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @quetz-frontend/apputils */ "webpack/sharing/consume/default/@quetz-frontend/apputils/@quetz-frontend/apputils");
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @fortawesome/react-fontawesome */ "webpack/sharing/consume/default/@fortawesome/react-fontawesome/@fortawesome/react-fontawesome");
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @fortawesome/free-solid-svg-icons */ "webpack/sharing/consume/default/@fortawesome/free-solid-svg-icons/@fortawesome/free-solid-svg-icons");
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _apiKeyDialog__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./apiKeyDialog */ "../../packages/user-extension/lib/apiKeyDialog.js");








class UserAPIKey extends react__WEBPACK_IMPORTED_MODULE_6__.PureComponent {
    constructor(props) {
        super(props);
        this._requestApiKey = async () => {
            const body = new _apiKeyDialog__WEBPACK_IMPORTED_MODULE_7__.RequestAPIKeyDialog();
            const value = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({ title: 'Keys', body });
            if (value.button.accept) {
                const data = body.info;
                if (!data.user && data.key.roles.length === 0) {
                    (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                        title: 'Format error',
                        body: 'Add roles',
                        buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()],
                    });
                    return;
                }
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
                const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, '/api/api-keys');
                const request = {
                    method: 'POST',
                    redirect: 'follow',
                    body: JSON.stringify(data.key),
                    headers: { 'Content-Type': 'application/json' },
                };
                const resp = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(url, request, settings);
                const response = await resp.json();
                if (response.detail) {
                    return console.error(response.detail);
                }
                const apiKeys = [...this.state.apiKeys, response];
                this.setState({ apiKeys });
            }
        };
        this._showRoles = async (roles) => {
            const body = new _apiKeyDialog__WEBPACK_IMPORTED_MODULE_7__.APIKeyDialog(roles);
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Roles',
                body,
                buttons: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton()],
            });
        };
        this._removeAPIKey = async (key) => {
            const body = (react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", null,
                "Do you want to delete the API key:",
                ' ',
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", { className: "qs-Label-Caption" }, key),
                "."));
            const value = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Delete API key',
                body,
            });
            if (value.button.accept) {
                const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
                const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, '/api/api-keys', key);
                const request = {
                    method: 'DELETE',
                    redirect: 'follow',
                };
                const resp = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(url, request, settings);
                if (!resp.ok) {
                    return console.error(resp.statusText);
                }
                const apiKeys = this.state.apiKeys.filter((api) => api.key !== key);
                this.setState({ apiKeys });
            }
        };
        this.state = {
            apiKeys: [],
            apiStatus: _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.API_STATUSES.PENDING,
        };
    }
    async componentDidMount() {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, '/api/api-keys');
        const resp = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(url, {}, settings);
        const data = await resp.json();
        if (data.detail) {
            return console.error(data.detail);
        }
        this.setState({
            apiKeys: data,
            apiStatus: _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.API_STATUSES.SUCCESS,
        });
    }
    render() {
        const { apiStatus, apiKeys } = this.state;
        const renderUserKey = () => {
            return apiKeys.map((item) => {
                if (item.roles === null) {
                    return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("tr", { key: item.key },
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, item.key),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null,
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", { className: "qs-Label-Caption" }, item.description)),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, item.time_created),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, item.expire_at),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", { onClick: () => (0,_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.copyToClipboard)(item.key, 'API key') },
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_4__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_5__.faCopy })),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", { onClick: () => this._removeAPIKey(item.key) },
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_4__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_5__.faTrash }))));
                }
            });
        };
        const renderKeys = () => {
            return apiKeys.map((item) => {
                if (item.roles !== null) {
                    return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("tr", { key: item.key, className: "qs-clickable-Row" },
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", { onClick: () => this._showRoles(item.roles) }, item.key),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", { onClick: () => this._showRoles(item.roles) }, item.description),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, item.time_created),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, item.expire_at),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", { onClick: () => (0,_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.copyToClipboard)(item.key, 'API key') },
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_4__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_5__.faCopy })),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", { onClick: () => this._removeAPIKey(item.key) },
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_4__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_5__.faTrash }))));
                }
            });
        };
        return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "padding-bottom" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("button", { className: "btn btn-default", onClick: this._requestApiKey }, "Request API key")),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("h3", { className: "heading3" }, "API keys"),
            apiStatus === _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.API_STATUSES.PENDING && (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_3__.InlineLoader, { text: "Fetching APIKeys" })),
            apiKeys.length !== 0 && (react__WEBPACK_IMPORTED_MODULE_6__.createElement("table", { className: "jp-table table-small" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("thead", null,
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("tr", null,
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Key"),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Description"),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Created"),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Expires"),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null))),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("tbody", null,
                    renderUserKey(),
                    renderKeys())))));
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (UserAPIKey);
//# sourceMappingURL=api-key.js.map

/***/ }),

/***/ "../../packages/user-extension/lib/apiKeyDialog.js":
/*!*********************************************************!*\
  !*** ../../packages/user-extension/lib/apiKeyDialog.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "RequestAPIKeyDialog": () => (/* binding */ RequestAPIKeyDialog),
/* harmony export */   "APIKeyDialog": () => (/* binding */ APIKeyDialog)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @quetz-frontend/apputils */ "webpack/sharing/consume/default/@quetz-frontend/apputils/@quetz-frontend/apputils");
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var moment__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! moment */ "webpack/sharing/consume/default/moment/moment");
/* harmony import */ var moment__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(moment__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_6__);







/**
 * A ReactWidget to edit the dashboard notebook metadata.
 */
class RequestAPIKeyDialog extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    /**
     * Construct a `DashboardMetadataEditor`.
     *
     */
    constructor() {
        super();
        /**
         * Handler for description input changes
         *
         * @param event
         */
        this._handleDescription = (event) => {
            this._api_key_info.description = event.target.value;
            this.update();
        };
        this._handleExpire = (event) => {
            this._api_key_info.expire_at = event.target.value;
            this.update();
        };
        this._handleUserCheck = (event) => {
            this._user_api_key = event.target.checked;
            this.update();
        };
        this._handleChannel = (event) => {
            this._role.channel = event.target.value;
            const channel = this._channels.find((channel) => channel.name === this._role.channel);
            if (channel) {
                switch (channel.role) {
                    case 'owner':
                        this._roles = ['member', 'maintainer', 'owner'];
                        break;
                    case 'maintainer':
                        this._roles = ['member', 'maintainer'];
                        break;
                    case 'member':
                        this._roles = ['member'];
                        break;
                    default:
                        this._roles = [];
                        break;
                }
            }
            else {
                this._roles = [];
            }
            this._packages_channel = this._packages.filter((value) => value.channel_name === this._role.channel);
            this.update();
        };
        this._handlePackage = (event) => {
            this._role.package = event.target.value;
            const pkg = this._packages.find((pkg) => pkg.name === this._role.package);
            if (pkg) {
                switch (pkg.role) {
                    case 'owner':
                        this._roles = ['member', 'maintainer', 'owner'];
                        break;
                    case 'maintainer':
                        this._roles = ['member', 'maintainer'];
                        break;
                    case 'member':
                        this._roles = ['member'];
                        break;
                }
            }
            this.update();
        };
        this._handleRole = (event) => {
            this._role.role = event.target.value;
            this.update();
        };
        /**
         * Handler for adding role to list of roles
         */
        this._addRole = () => {
            this._api_key_info.roles.push(this._role);
            this._role = {
                channel: '',
                package: '',
                role: 'member',
            };
            this._packages_channel = [];
            this.update();
        };
        /**
         * Handler for removing role from list of roles
         *
         * @param index
         */
        this._removeRole = (index) => {
            this._api_key_info.roles.splice(index, 1);
            this.update();
        };
        const expire_at = moment__WEBPACK_IMPORTED_MODULE_5___default()().add(1, 'months').format((moment__WEBPACK_IMPORTED_MODULE_5___default().HTML5_FMT.DATE));
        this._api_key_info = {
            description: '',
            expire_at,
            roles: [],
        };
        this._username = '';
        this._apiStatus = _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.API_STATUSES.PENDING;
        this._user_api_key = true;
        this._role = {
            channel: '',
            package: '',
            role: 'member',
        };
        this._channels = [];
        this._packages = [];
        this._roles = [];
        this._packages_channel = [];
    }
    get info() {
        if (this._user_api_key) {
            return {
                user: true,
                key: {
                    description: this._api_key_info.description,
                    expire_at: this._api_key_info.expire_at,
                    roles: [],
                },
            };
        }
        else {
            return { user: false, key: this._api_key_info };
        }
    }
    onAfterAttach(message) {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, '/api/me');
        _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(url, {}, settings)
            .then((resp) => {
            return resp.json();
        })
            .then(async (data) => {
            if (data.detail) {
                return console.error(data.detail);
            }
            this._username = data.user.username;
            const urlChannels = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, `/api/users/${this._username}/channels`);
            const respChannels = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(urlChannels, {}, settings);
            const channels = await respChannels.json();
            if (channels.detail) {
                console.error(channels.detail);
                this._channels = [];
            }
            else {
                this._channels = channels;
            }
            const urlPackages = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, `/api/users/${this._username}/packages`);
            const respPackage = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(urlPackages, {}, settings);
            const packages = await respPackage.json();
            if (packages.detail) {
                console.error(packages.detail);
                this._packages = [];
            }
            else {
                this._packages = packages;
            }
            this._apiStatus = _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.API_STATUSES.SUCCESS;
            this.update();
        });
    }
    render() {
        const renderChannels = () => {
            return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "qs-Form-Section" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", { className: "qs-Input-Label" }, "Channel:"),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("input", { name: "channels", type: "search", className: "jp-mod-styled", list: "channels", value: this._role.channel, onChange: this._handleChannel, placeholder: "Select a channel" }),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("datalist", { id: "channels" }, this._channels.map((channel, i) => (react__WEBPACK_IMPORTED_MODULE_6__.createElement("option", { key: i, value: channel.name }, channel.name))))));
        };
        const renderPackages = () => {
            return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "qs-Form-Section" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", { className: "qs-Input-Label" }, "Package"),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("input", { name: "package", type: "search", className: "jp-mod-styled", list: "packages", value: this._role.package, onChange: this._handlePackage, placeholder: "Leave blank for all packages", disabled: this._role.channel.length === 0 }),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("datalist", { id: "packages" }, this._packages_channel.map((value, i) => (react__WEBPACK_IMPORTED_MODULE_6__.createElement("option", { key: i, value: value.name }, value.name))))));
        };
        const renderRoles = () => {
            return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "qs-Form-Section" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", { className: "qs-Input-Label" }, "Role"),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("select", { name: "role", className: "jp-mod-styled", value: this._role.role, onChange: this._handleRole }, this._roles.map((role, i) => (react__WEBPACK_IMPORTED_MODULE_6__.createElement("option", { key: i, value: role }, role))))));
        };
        const renderTable = () => {
            return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "qs-Form-Section" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("table", { className: "jp-table table-small" },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("thead", null,
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("tr", null,
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Channel"),
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Package"),
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Role"))),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("tbody", null, this._api_key_info.roles.map((role, i) => {
                        return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("tr", { key: i, className: "qs-clickable-Row", onClick: () => this._removeRole(i) },
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, role.channel.length !== 0 ? role.channel : '*'),
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, role.package.length !== 0 ? role.package : '*'),
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, role.role)));
                    })))));
        };
        return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("form", { className: "jp-Input-Dialog" },
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "qs-Form-Section" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", { className: "qs-Form-Section-Label" }, "Description"),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("input", { type: "textarea", name: "description", className: "jp-mod-styled", value: this._api_key_info.description, onChange: this._handleDescription })),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "qs-Form-Section" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", { className: "qs-Form-Section-Label" }, "Expiration date"),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("input", { type: "date", name: "expire_at", className: "jp-mod-styled", min: moment__WEBPACK_IMPORTED_MODULE_5___default()().format((moment__WEBPACK_IMPORTED_MODULE_5___default().HTML5_FMT.DATE)), value: this._api_key_info.expire_at, onChange: this._handleExpire })),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "qs-Form-Section-Row" },
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("input", { id: "user-apiKey", type: "checkbox", name: "user-apiKey", defaultChecked: this._user_api_key, onChange: this._handleUserCheck }),
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", null,
                    "API key with same roles as",
                    ' ',
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", { className: "qs-Label-Caption" }, this._username))),
            !this._user_api_key && (react__WEBPACK_IMPORTED_MODULE_6__.createElement(react__WEBPACK_IMPORTED_MODULE_6__.Fragment, null,
                this._apiStatus === _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.API_STATUSES.PENDING && (react__WEBPACK_IMPORTED_MODULE_6__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.InlineLoader, { text: "Fetching user channels and packages" })),
                this._channels.length !== 0 ? (react__WEBPACK_IMPORTED_MODULE_6__.createElement(react__WEBPACK_IMPORTED_MODULE_6__.Fragment, null,
                    renderChannels(),
                    this._role.channel.length !== 0 ? (react__WEBPACK_IMPORTED_MODULE_6__.createElement(react__WEBPACK_IMPORTED_MODULE_6__.Fragment, null,
                        this._packages_channel.length !== 0 && renderPackages(),
                        renderRoles(),
                        react__WEBPACK_IMPORTED_MODULE_6__.createElement("div", { className: "qs-Form-Section" },
                            react__WEBPACK_IMPORTED_MODULE_6__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.Button, { onClick: this._addRole, minimal: true }, "Add role")))) : (react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", null, "No packages available")))) : (react__WEBPACK_IMPORTED_MODULE_6__.createElement("label", null, "No channels available")),
                this._api_key_info.roles.length !== 0 && renderTable()))));
    }
}
/**
 * A ReactWidget to render a table for APIKeys' roles.
 */
class APIKeyDialog extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    /**
     * Construct a `APIKeyDialog`.
     *
     * @param roles
     */
    constructor(roles) {
        super();
        this._roles = roles;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("table", { className: "jp-table table-small" },
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("thead", null,
                react__WEBPACK_IMPORTED_MODULE_6__.createElement("tr", null,
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Channel"),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Package"),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("th", null, "Role"))),
            react__WEBPACK_IMPORTED_MODULE_6__.createElement("tbody", { className: "qs-scrollable-Table" }, this._roles.map((role, i) => {
                return (react__WEBPACK_IMPORTED_MODULE_6__.createElement("tr", { key: i },
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, role.channel ? role.channel : '*'),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, role.package ? role.package : '*'),
                    react__WEBPACK_IMPORTED_MODULE_6__.createElement("td", null, role.role ? role.role : '*')));
            }))));
    }
}
//# sourceMappingURL=apiKeyDialog.js.map

/***/ }),

/***/ "../../packages/user-extension/lib/index.js":
/*!**************************************************!*\
  !*** ../../packages/user-extension/lib/index.js ***!
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
/* harmony import */ var _quetz_frontend_menu__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @quetz-frontend/menu */ "webpack/sharing/consume/default/@quetz-frontend/menu/@quetz-frontend/menu");
/* harmony import */ var _quetz_frontend_menu__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_menu__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! lodash */ "webpack/sharing/consume/default/lodash/lodash");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var react_notifications_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! react-notifications-component */ "webpack/sharing/consume/default/react-notifications-component/react-notifications-component");
/* harmony import */ var react_notifications_component__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(react_notifications_component__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _api_key__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./api-key */ "../../packages/user-extension/lib/api-key.js");
/* harmony import */ var _tab_profile__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./tab-profile */ "../../packages/user-extension/lib/tab-profile.js");
/* harmony import */ var _tab_packages__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./tab-packages */ "../../packages/user-extension/lib/tab-packages.js");
/* harmony import */ var _tab_channels__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./tab-channels */ "../../packages/user-extension/lib/tab-channels.js");














/**
 * The command ids used by the main plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/user-extension:user';
    CommandIDs.open = '@quetz-frontend/user-extension:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main menu plugin.
 */
const plugin = {
    id: CommandIDs.plugin,
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.IRouter, _quetz_frontend_menu__WEBPACK_IMPORTED_MODULE_5__.ILogInMenu],
    activate: (app, router, menu) => {
        const { shell, commands } = app;
        commands.addCommand(CommandIDs.open, {
            execute: () => {
                shell.add(new UserRouter(), 'main');
            },
        });
        router.register({
            pattern: /user.*/,
            command: CommandIDs.open,
        });
        menu.addItem({
            id: CommandIDs.open,
            label: 'Profile',
            icon: 'empty',
            api: '/user',
            loggedIn: true,
        });
    },
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
const getBreadcrumbText = () => {
    const currentSection = (0,lodash__WEBPACK_IMPORTED_MODULE_6__.last)(window.location.pathname.split('/'));
    if (currentSection === 'api-keys') {
        return 'API keys';
    }
    return (0,lodash__WEBPACK_IMPORTED_MODULE_6__.capitalize)(currentSection);
};
class UserRouter extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor() {
        super();
        this.id = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.DOMUtils.createDomID();
        this.title.label = 'User main page';
    }
    render() {
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_2__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_3__.URLExt.join(settings.baseUrl, '/api/me');
        const breadcrumbItems = [
            {
                text: 'Home',
                href: '/',
            },
            {
                text: 'User details',
                link: '/',
            },
            {
                text: getBreadcrumbText(),
            },
        ];
        return (react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.BrowserRouter, { basename: "/user" },
            react__WEBPACK_IMPORTED_MODULE_9__.createElement((react_notifications_component__WEBPACK_IMPORTED_MODULE_8___default()), null),
            react__WEBPACK_IMPORTED_MODULE_9__.createElement("div", { className: "page-contents-width-limit" },
                react__WEBPACK_IMPORTED_MODULE_9__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.Breadcrumbs, { items: breadcrumbItems }),
                react__WEBPACK_IMPORTED_MODULE_9__.createElement("h2", { className: "heading2" }, "User details"),
                react__WEBPACK_IMPORTED_MODULE_9__.createElement("div", { className: "left-right" },
                    react__WEBPACK_IMPORTED_MODULE_9__.createElement("div", { className: "leftbar" },
                        react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.NavLink, { className: "leftbar-item", to: "/profile" }, "Profile"),
                        react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.NavLink, { className: "leftbar-item", to: "/api-keys" }, "API key"),
                        react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.NavLink, { className: "leftbar-item", to: "/channels" }, "Channels"),
                        react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.NavLink, { className: "leftbar-item", to: "/packages" }, "Packages")),
                    react__WEBPACK_IMPORTED_MODULE_9__.createElement("div", { className: "right-section" },
                        react__WEBPACK_IMPORTED_MODULE_9__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_4__.FetchHoc, { url: url, loadingMessage: "Fetching user information", genericErrorMessage: "Error fetching user information" }, (userData) => (react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.Switch, null,
                            react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.Route, { path: "/profile" },
                                react__WEBPACK_IMPORTED_MODULE_9__.createElement(_tab_profile__WEBPACK_IMPORTED_MODULE_10__.default, { userData: userData })),
                            react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.Route, { path: "/api-keys" },
                                react__WEBPACK_IMPORTED_MODULE_9__.createElement(_api_key__WEBPACK_IMPORTED_MODULE_11__.default, null)),
                            react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.Route, { path: "/channels" },
                                react__WEBPACK_IMPORTED_MODULE_9__.createElement(_tab_channels__WEBPACK_IMPORTED_MODULE_12__.default, { username: userData.user.username })),
                            react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.Route, { path: "/packages" },
                                react__WEBPACK_IMPORTED_MODULE_9__.createElement(_tab_packages__WEBPACK_IMPORTED_MODULE_13__.default, { username: userData.user.username })),
                            react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.Route, { path: "/", exact: true },
                                react__WEBPACK_IMPORTED_MODULE_9__.createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_7__.Redirect, { to: "/profile" }))))))))));
    }
}
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../../packages/user-extension/lib/tab-channels.js":
/*!*********************************************************!*\
  !*** ../../packages/user-extension/lib/tab-channels.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "getUserChannelsTableColumns": () => (/* binding */ getUserChannelsTableColumns)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _quetz_frontend_table__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @quetz-frontend/table */ "webpack/sharing/consume/default/@quetz-frontend/table/@quetz-frontend/table");
/* harmony import */ var _quetz_frontend_table__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_table__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);




class UserChannels extends react__WEBPACK_IMPORTED_MODULE_3__.PureComponent {
    render() {
        const { username } = this.props;
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, '/api/paginated/users', username, '/channels');
        return (react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("h3", { className: "heading3" }, "Channels"),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement(_quetz_frontend_table__WEBPACK_IMPORTED_MODULE_2__.PaginatedTable, { url: url, columns: getUserChannelsTableColumns(), to: (rowData) => `/${rowData.name}` })));
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (UserChannels);
const getUserChannelsTableColumns = () => [
    {
        Header: 'Name',
        accessor: 'name',
        Cell: ({ row }) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement("a", { href: `/channels/${row.original.name}` }, row.original.name)),
    },
    {
        Header: 'Role',
        accessor: 'role',
    },
];
//# sourceMappingURL=tab-channels.js.map

/***/ }),

/***/ "../../packages/user-extension/lib/tab-packages.js":
/*!*********************************************************!*\
  !*** ../../packages/user-extension/lib/tab-packages.js ***!
  \*********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "getUserChannelsTableColumns": () => (/* binding */ getUserChannelsTableColumns)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _quetz_frontend_table__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @quetz-frontend/table */ "webpack/sharing/consume/default/@quetz-frontend/table/@quetz-frontend/table");
/* harmony import */ var _quetz_frontend_table__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_table__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);




class UserPackages extends react__WEBPACK_IMPORTED_MODULE_3__.PureComponent {
    render() {
        const { username } = this.props;
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
        const url = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.URLExt.join(settings.baseUrl, '/api/paginated/users', username, '/packages');
        return (react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("h3", { className: "heading3" }, "Packages"),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement(_quetz_frontend_table__WEBPACK_IMPORTED_MODULE_2__.PaginatedTable, { url: url, columns: getUserChannelsTableColumns(), to: (rowData) => `/${rowData.name}` })));
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (UserPackages);
const getUserChannelsTableColumns = () => [
    {
        Header: 'Name',
        accessor: 'name',
        Cell: ({ row }) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement("a", { href: `/channels/${row.original.name}` }, row.original.name)),
    },
    {
        Header: 'Role',
        accessor: 'role',
    },
];
//# sourceMappingURL=tab-packages.js.map

/***/ }),

/***/ "../../packages/user-extension/lib/tab-profile.js":
/*!********************************************************!*\
  !*** ../../packages/user-extension/lib/tab-profile.js ***!
  \********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

class UserProfile extends react__WEBPACK_IMPORTED_MODULE_0__.PureComponent {
    render() {
        const { userData } = this.props;
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(react__WEBPACK_IMPORTED_MODULE_0__.Fragment, null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("h3", { className: "heading3" }, "Profile"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: "caption-inline" }, "Name"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: "paragraph" }, userData.name),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: "caption-inline" }, "Username"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: "paragraph" }, userData.user.username),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: "caption-inline" }, "Avatar"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("img", { className: "user-avatar", src: userData.avatar_url, alt: "" })));
    }
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (UserProfile);
//# sourceMappingURL=tab-profile.js.map

/***/ })

}]);
//# sourceMappingURL=packages_user-extension_lib_index_js.bundle.js.map