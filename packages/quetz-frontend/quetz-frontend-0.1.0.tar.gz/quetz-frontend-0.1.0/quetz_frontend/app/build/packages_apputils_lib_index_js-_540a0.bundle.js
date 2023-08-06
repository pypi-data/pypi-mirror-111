(self["webpackChunk_quetz_frontend_app"] = self["webpackChunk_quetz_frontend_app"] || []).push([["packages_apputils_lib_index_js-_540a0"],{

/***/ "../../node_modules/clsx/dist/clsx.m.js":
/*!**********************************************!*\
  !*** ../../node_modules/clsx/dist/clsx.m.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* export default binding */ __WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
function toVal(mix) {
	var k, y, str='';

	if (typeof mix === 'string' || typeof mix === 'number') {
		str += mix;
	} else if (typeof mix === 'object') {
		if (Array.isArray(mix)) {
			for (k=0; k < mix.length; k++) {
				if (mix[k]) {
					if (y = toVal(mix[k])) {
						str && (str += ' ');
						str += y;
					}
				}
			}
		} else {
			for (k in mix) {
				if (mix[k]) {
					str && (str += ' ');
					str += k;
				}
			}
		}
	}

	return str;
}

/* harmony default export */ function __WEBPACK_DEFAULT_EXPORT__() {
	var i=0, tmp, x, str='';
	while (i < arguments.length) {
		if (tmp = arguments[i++]) {
			if (x = toVal(tmp)) {
				str && (str += ' ');
				str += x
			}
		}
	}
	return str;
}


/***/ }),

/***/ "../../packages/apputils/lib/breadcrumbs.js":
/*!**************************************************!*\
  !*** ../../packages/apputils/lib/breadcrumbs.js ***!
  \**************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Breadcrumbs": () => (/* binding */ Breadcrumbs)
/* harmony export */ });
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! lodash */ "webpack/sharing/consume/default/lodash/lodash");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


const BreadcrumbChild = ({ data }) => {
    if (data.link) {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "breadcrumb-link", 
            //@ts-ignore
            onClick: () => window.router.navigate(data.link) }, data.text));
    }
    if (data.href) {
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("a", { href: data.href, className: "breadcrumb-link" }, data.text));
    }
    return data.text;
};
class Breadcrumbs extends react__WEBPACK_IMPORTED_MODULE_1__.PureComponent {
    render() {
        const { items } = this.props;
        return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "breadcrumbs" }, (0,lodash__WEBPACK_IMPORTED_MODULE_0__.reduce)(items, (unionArray, item) => (0,lodash__WEBPACK_IMPORTED_MODULE_0__.union)(unionArray, [
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "breadcrumb-item", key: item.text },
                react__WEBPACK_IMPORTED_MODULE_1__.createElement(BreadcrumbChild, { data: item })),
            react__WEBPACK_IMPORTED_MODULE_1__.createElement("div", { className: "breadcrumb-separator", key: `${item.text}-separator` }, "\u2003/\u2003"),
        ]), []).slice(0, -1)));
    }
}
//# sourceMappingURL=breadcrumbs.js.map

/***/ }),

/***/ "../../packages/apputils/lib/constants.js":
/*!************************************************!*\
  !*** ../../packages/apputils/lib/constants.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "API_STATUSES": () => (/* binding */ API_STATUSES),
/* harmony export */   "KB_SIZE": () => (/* binding */ KB_SIZE),
/* harmony export */   "MB_SIZE": () => (/* binding */ MB_SIZE),
/* harmony export */   "GB_SIZE": () => (/* binding */ GB_SIZE)
/* harmony export */ });
var API_STATUSES;
(function (API_STATUSES) {
    API_STATUSES["PENDING"] = "PENDING";
    API_STATUSES["SUCCESS"] = "SUCCESS";
    API_STATUSES["FAILED"] = "FAILED";
})(API_STATUSES || (API_STATUSES = {}));
const KB_SIZE = 1024;
const MB_SIZE = 1024 * KB_SIZE;
const GB_SIZE = 1024 * MB_SIZE;
//# sourceMappingURL=constants.js.map

/***/ }),

/***/ "../../packages/apputils/lib/fetch-hoc.js":
/*!************************************************!*\
  !*** ../../packages/apputils/lib/fetch-hoc.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "FetchHoc": () => (/* binding */ FetchHoc)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./constants */ "../../packages/apputils/lib/constants.js");
/* harmony import */ var _loader__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./loader */ "../../packages/apputils/lib/loader.js");




class FetchHoc extends react__WEBPACK_IMPORTED_MODULE_1__.PureComponent {
    constructor(props) {
        super(props);
        this.componentDidMount = () => {
            this.tryFetch();
        };
        this.tryFetch = async () => {
            const { url } = this.props;
            this.setState({
                apiStatus: _constants__WEBPACK_IMPORTED_MODULE_2__.API_STATUSES.PENDING,
            });
            const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
            const resp = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(url, {}, settings);
            if (!resp.ok) {
                this.setState({
                    error: resp.statusText,
                    apiStatus: _constants__WEBPACK_IMPORTED_MODULE_2__.API_STATUSES.FAILED,
                });
            }
            else {
                this.setState({
                    data: await resp.json(),
                    apiStatus: _constants__WEBPACK_IMPORTED_MODULE_2__.API_STATUSES.SUCCESS,
                });
            }
        };
        this.state = {
            data: null,
            apiStatus: _constants__WEBPACK_IMPORTED_MODULE_2__.API_STATUSES.PENDING,
            error: '',
        };
    }
    render() {
        const { apiStatus, data, error } = this.state;
        const { children, loadingMessage, genericErrorMessage } = this.props;
        if (apiStatus === _constants__WEBPACK_IMPORTED_MODULE_2__.API_STATUSES.PENDING) {
            return react__WEBPACK_IMPORTED_MODULE_1__.createElement(_loader__WEBPACK_IMPORTED_MODULE_3__.InlineLoader, { text: loadingMessage });
        }
        if (apiStatus === _constants__WEBPACK_IMPORTED_MODULE_2__.API_STATUSES.FAILED) {
            return (react__WEBPACK_IMPORTED_MODULE_1__.createElement("p", { className: "paragraph padding" },
                error || genericErrorMessage || 'Error occured while fetching data',
                "\u2003",
                react__WEBPACK_IMPORTED_MODULE_1__.createElement("button", { className: "btn btn-inline", onClick: this.tryFetch }, "Try again")));
        }
        return react__WEBPACK_IMPORTED_MODULE_1__.createElement(react__WEBPACK_IMPORTED_MODULE_1__.Fragment, null, children(data));
    }
}
//# sourceMappingURL=fetch-hoc.js.map

/***/ }),

/***/ "../../packages/apputils/lib/index.js":
/*!********************************************!*\
  !*** ../../packages/apputils/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Breadcrumbs": () => (/* reexport safe */ _breadcrumbs__WEBPACK_IMPORTED_MODULE_0__.Breadcrumbs),
/* harmony export */   "API_STATUSES": () => (/* reexport safe */ _constants__WEBPACK_IMPORTED_MODULE_1__.API_STATUSES),
/* harmony export */   "GB_SIZE": () => (/* reexport safe */ _constants__WEBPACK_IMPORTED_MODULE_1__.GB_SIZE),
/* harmony export */   "KB_SIZE": () => (/* reexport safe */ _constants__WEBPACK_IMPORTED_MODULE_1__.KB_SIZE),
/* harmony export */   "MB_SIZE": () => (/* reexport safe */ _constants__WEBPACK_IMPORTED_MODULE_1__.MB_SIZE),
/* harmony export */   "FetchHoc": () => (/* reexport safe */ _fetch_hoc__WEBPACK_IMPORTED_MODULE_2__.FetchHoc),
/* harmony export */   "InlineLoader": () => (/* reexport safe */ _loader__WEBPACK_IMPORTED_MODULE_3__.InlineLoader),
/* harmony export */   "NOTIFICATION_TYPES": () => (/* reexport safe */ _notification__WEBPACK_IMPORTED_MODULE_4__.NOTIFICATION_TYPES),
/* harmony export */   "sendNotification": () => (/* reexport safe */ _notification__WEBPACK_IMPORTED_MODULE_4__.sendNotification),
/* harmony export */   "SearchBox": () => (/* reexport safe */ _search__WEBPACK_IMPORTED_MODULE_5__.SearchBox),
/* harmony export */   "copyToClipboard": () => (/* reexport safe */ _utils__WEBPACK_IMPORTED_MODULE_6__.copyToClipboard),
/* harmony export */   "formatPlural": () => (/* reexport safe */ _utils__WEBPACK_IMPORTED_MODULE_6__.formatPlural),
/* harmony export */   "formatSize": () => (/* reexport safe */ _utils__WEBPACK_IMPORTED_MODULE_6__.formatSize)
/* harmony export */ });
/* harmony import */ var _breadcrumbs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./breadcrumbs */ "../../packages/apputils/lib/breadcrumbs.js");
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./constants */ "../../packages/apputils/lib/constants.js");
/* harmony import */ var _fetch_hoc__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./fetch-hoc */ "../../packages/apputils/lib/fetch-hoc.js");
/* harmony import */ var _loader__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./loader */ "../../packages/apputils/lib/loader.js");
/* harmony import */ var _notification__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./notification */ "../../packages/apputils/lib/notification.js");
/* harmony import */ var _search__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./search */ "../../packages/apputils/lib/search.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./utils */ "../../packages/apputils/lib/utils.js");







//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../../packages/apputils/lib/loader.js":
/*!*********************************************!*\
  !*** ../../packages/apputils/lib/loader.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "InlineLoader": () => (/* binding */ InlineLoader)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

class InlineLoader extends react__WEBPACK_IMPORTED_MODULE_0__.PureComponent {
    render() {
        const { text } = this.props;
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "loader-wrapper padding" },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: "loader" }),
            text && react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", { className: "text loader-text" }, text)));
    }
}
//# sourceMappingURL=loader.js.map

/***/ }),

/***/ "../../packages/apputils/lib/notification.js":
/*!***************************************************!*\
  !*** ../../packages/apputils/lib/notification.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NOTIFICATION_TYPES": () => (/* binding */ NOTIFICATION_TYPES),
/* harmony export */   "sendNotification": () => (/* binding */ sendNotification)
/* harmony export */ });
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @fortawesome/react-fontawesome */ "webpack/sharing/consume/default/@fortawesome/react-fontawesome/@fortawesome/react-fontawesome");
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @fortawesome/free-solid-svg-icons */ "webpack/sharing/consume/default/@fortawesome/free-solid-svg-icons/@fortawesome/free-solid-svg-icons");
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var clsx__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! clsx */ "../../node_modules/clsx/dist/clsx.m.js");
/* harmony import */ var react_notifications_component__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-notifications-component */ "webpack/sharing/consume/default/react-notifications-component/react-notifications-component");
/* harmony import */ var react_notifications_component__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react_notifications_component__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);





const NOTIFICATION_TYPES = {
    SUCCESS: 'success',
    DANGER: 'danger',
    INFO: 'info',
    DEFAULT: 'default',
    WARNING: 'warning',
};
const NOTIFICATION_ICONS = {
    [NOTIFICATION_TYPES.SUCCESS]: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__.faCheckCircle,
    [NOTIFICATION_TYPES.DANGER]: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__.faTimesCircle,
    [NOTIFICATION_TYPES.INFO]: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__.faInfoCircle,
    [NOTIFICATION_TYPES.DEFAULT]: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__.faInfoCircle,
    [NOTIFICATION_TYPES.WARNING]: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__.faExclamationCircle,
};
class NotificationComponent extends react__WEBPACK_IMPORTED_MODULE_4__.PureComponent {
    render() {
        const { id, type, title, message } = this.props;
        return (react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", { className: "notification-item" },
            react__WEBPACK_IMPORTED_MODULE_4__.createElement("p", { className: (0,clsx__WEBPACK_IMPORTED_MODULE_2__.default)('notification-icon', type) },
                react__WEBPACK_IMPORTED_MODULE_4__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_0__.FontAwesomeIcon, { icon: NOTIFICATION_ICONS[type] })),
            react__WEBPACK_IMPORTED_MODULE_4__.createElement("div", { className: "notification-content" },
                title && react__WEBPACK_IMPORTED_MODULE_4__.createElement("p", { className: (0,clsx__WEBPACK_IMPORTED_MODULE_2__.default)('notification-title', type) }, title),
                message && react__WEBPACK_IMPORTED_MODULE_4__.createElement("p", { className: "notification-message" }, message)),
            react__WEBPACK_IMPORTED_MODULE_4__.createElement("button", { className: "notification-close" },
                react__WEBPACK_IMPORTED_MODULE_4__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_0__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__.faTimes, onClick: () => react_notifications_component__WEBPACK_IMPORTED_MODULE_3__.store.removeNotification(id) }))));
    }
}
const sendNotification = ({ type = NOTIFICATION_TYPES.DEFAULT, title, message, duration, }) => {
    const notifId = react_notifications_component__WEBPACK_IMPORTED_MODULE_3__.store.addNotification({
        content: ({ id }) => (react__WEBPACK_IMPORTED_MODULE_4__.createElement(NotificationComponent, { id: id, title: title, type: type, message: message })),
        insert: 'top',
        container: 'top-right',
        animationIn: ['animate__animated', 'animate__fadeIn'],
        animationOut: ['animate__animated', 'animate__fadeOut'],
        dismiss: {
            duration,
        },
    });
    // TODO: Find out why the notifiaction is not automatically disappearing
    if (duration) {
        setTimeout(() => {
            react_notifications_component__WEBPACK_IMPORTED_MODULE_3__.store.removeNotification(notifId);
        }, duration);
    }
};
//# sourceMappingURL=notification.js.map

/***/ }),

/***/ "../../packages/apputils/lib/search.js":
/*!*********************************************!*\
  !*** ../../packages/apputils/lib/search.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SearchBox": () => (/* binding */ SearchBox)
/* harmony export */ });
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @fortawesome/react-fontawesome */ "webpack/sharing/consume/default/@fortawesome/react-fontawesome/@fortawesome/react-fontawesome");
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @fortawesome/free-solid-svg-icons */ "webpack/sharing/consume/default/@fortawesome/free-solid-svg-icons/@fortawesome/free-solid-svg-icons");
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);



class SearchBox extends react__WEBPACK_IMPORTED_MODULE_2__.PureComponent {
    constructor(props) {
        super(props);
        this.updateInput = (e) => {
            const { onTextUpdate } = this.props;
            this.setState({
                input: e.target.value,
            });
            if (onTextUpdate) {
                onTextUpdate(e.target.value);
            }
        };
        this.onSubmit = (e) => {
            const { onSubmit } = this.props;
            const { input } = this.state;
            e.preventDefault();
            if (onSubmit) {
                onSubmit(input);
            }
        };
        this.state = {
            input: '',
        };
    }
    render() {
        const { input } = this.state;
        const { onSubmit } = this.props;
        return (react__WEBPACK_IMPORTED_MODULE_2__.createElement("form", { onSubmit: this.onSubmit },
            react__WEBPACK_IMPORTED_MODULE_2__.createElement("div", { className: "btn-group" },
                react__WEBPACK_IMPORTED_MODULE_2__.createElement("input", { className: "input search-input", value: input, type: "text", onChange: this.updateInput, placeholder: "Search" }),
                onSubmit && (react__WEBPACK_IMPORTED_MODULE_2__.createElement("button", { className: "btn btn-default", type: "submit" },
                    react__WEBPACK_IMPORTED_MODULE_2__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_0__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_1__.faSearch }))))));
    }
}
//# sourceMappingURL=search.js.map

/***/ }),

/***/ "../../packages/apputils/lib/utils.js":
/*!********************************************!*\
  !*** ../../packages/apputils/lib/utils.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "formatPlural": () => (/* binding */ formatPlural),
/* harmony export */   "formatSize": () => (/* binding */ formatSize),
/* harmony export */   "copyToClipboard": () => (/* binding */ copyToClipboard)
/* harmony export */ });
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! lodash */ "webpack/sharing/consume/default/lodash/lodash");
/* harmony import */ var lodash__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _constants__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./constants */ "../../packages/apputils/lib/constants.js");
/* harmony import */ var _notification__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./notification */ "../../packages/apputils/lib/notification.js");



const formatPlural = (count, text) => `${count} ${text}${count > 1 ? 's' : ''}`;
const formatSize = (sizeInBytes) => {
    if (sizeInBytes > _constants__WEBPACK_IMPORTED_MODULE_1__.GB_SIZE) {
        return `${(0,lodash__WEBPACK_IMPORTED_MODULE_0__.round)(sizeInBytes / _constants__WEBPACK_IMPORTED_MODULE_1__.GB_SIZE, 2)} GB`;
    }
    if (sizeInBytes > _constants__WEBPACK_IMPORTED_MODULE_1__.MB_SIZE) {
        return `${(0,lodash__WEBPACK_IMPORTED_MODULE_0__.round)(sizeInBytes / _constants__WEBPACK_IMPORTED_MODULE_1__.MB_SIZE, 2)} MB`;
    }
    if (sizeInBytes > _constants__WEBPACK_IMPORTED_MODULE_1__.KB_SIZE) {
        return `${(0,lodash__WEBPACK_IMPORTED_MODULE_0__.round)(sizeInBytes / _constants__WEBPACK_IMPORTED_MODULE_1__.KB_SIZE, 2)} KB`;
    }
    return `${sizeInBytes} bytes`;
};
const copyToClipboard = (text, textType) => {
    navigator.clipboard
        .writeText(text)
        .then(() => {
        (0,_notification__WEBPACK_IMPORTED_MODULE_2__.sendNotification)({
            type: _notification__WEBPACK_IMPORTED_MODULE_2__.NOTIFICATION_TYPES.INFO,
            message: `Copied ${textType && `${textType} `}to clipboard`,
            duration: 3000,
        });
    })
        .catch((e) => console.error(e));
};
//# sourceMappingURL=utils.js.map

/***/ })

}]);
//# sourceMappingURL=packages_apputils_lib_index_js-_540a0.bundle.js.map