(self["webpackChunk_quetz_frontend_app"] = self["webpackChunk_quetz_frontend_app"] || []).push([["packages_table_lib_index_js"],{

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

/***/ "../../packages/table/lib/index.js":
/*!*****************************************!*\
  !*** ../../packages/table/lib/index.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "List": () => (/* reexport safe */ _list__WEBPACK_IMPORTED_MODULE_0__.List),
/* harmony export */   "PaginatedList": () => (/* reexport safe */ _list__WEBPACK_IMPORTED_MODULE_0__.PaginatedList),
/* harmony export */   "Pagination": () => (/* reexport safe */ _pagination__WEBPACK_IMPORTED_MODULE_1__.Pagination),
/* harmony export */   "PaginatedTable": () => (/* reexport safe */ _table__WEBPACK_IMPORTED_MODULE_2__.PaginatedTable),
/* harmony export */   "Table": () => (/* reexport safe */ _table__WEBPACK_IMPORTED_MODULE_2__.Table)
/* harmony export */ });
/* harmony import */ var _list__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./list */ "../../packages/table/lib/list.js");
/* harmony import */ var _pagination__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./pagination */ "../../packages/table/lib/pagination.js");
/* harmony import */ var _table__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./table */ "../../packages/table/lib/table.js");



//# sourceMappingURL=index.js.map

/***/ }),

/***/ "../../packages/table/lib/list.js":
/*!****************************************!*\
  !*** ../../packages/table/lib/list.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "List": () => (/* binding */ List),
/* harmony export */   "PaginatedList": () => (/* binding */ PaginatedList)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_table__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-table */ "webpack/sharing/consume/default/react-table/react-table");
/* harmony import */ var react_table__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_table__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var clsx__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! clsx */ "../../node_modules/clsx/dist/clsx.m.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _pagination__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./pagination */ "../../packages/table/lib/pagination.js");





const headerProps = (props, { column }) => getStyles(props, column.align);
const cellProps = (props, { cell }) => getStyles(props, cell.column.align);
const getStyles = (props, align = 'left') => [
    props,
    {
        style: {
            justifyContent: align === 'right' ? 'flex-end' : 'flex-start',
            alignItems: 'flex-start',
            display: 'flex',
        },
    },
];
const List = ({ columns: userColumns, data, to, paginated, fetchData, loading, pageCount: controlledPageCount, dataSize, }) => {
    const defaultColumn = {
        width: 150, // width is used for both the flex-basis and flex-grow
    };
    const { getTableProps, headerGroups, prepareRow, 
    // Non-paginated table
    rows, 
    // Paginated table
    page, canPreviousPage, canNextPage, pageOptions, pageCount, gotoPage, nextPage, previousPage, setPageSize, state: { pageIndex, pageSize }, } = (0,react_table__WEBPACK_IMPORTED_MODULE_1__.useTable)({
        columns: userColumns,
        data,
        defaultColumn,
        initialState: { pageIndex: 0 },
        manualPagination: paginated,
        pageCount: controlledPageCount,
    }, react_table__WEBPACK_IMPORTED_MODULE_1__.useFlexLayout, (hooks) => {
        hooks.allColumns.push((columns) => [...columns]);
    }, ...(paginated ? [react_table__WEBPACK_IMPORTED_MODULE_1__.usePagination] : []));
    if (paginated) {
        react__WEBPACK_IMPORTED_MODULE_3__.useEffect(() => {
            fetchData({ pageIndex, pageSize });
        }, [fetchData, pageIndex, pageSize]);
    }
    // Only show the "Showing 1 to x of y results and arrows if there's more than one page"
    const showPaginationInformation = dataSize > pageSize;
    const route = (path) => {
        if (path) {
            //@ts-ignore
            window.router.navigate(path);
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_3__.createElement(react__WEBPACK_IMPORTED_MODULE_3__.Fragment, null,
        react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", Object.assign({}, getTableProps(), { className: "table" }),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", null, headerGroups.map((headerGroup, key) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", Object.assign({}, headerGroup.getHeaderGroupProps({
            // style: { paddingRight: '15px' },
            }), { className: "tr", key: key }), headerGroup.headers.map((column) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", Object.assign({}, column.getHeaderProps(headerProps), { className: "th", key: column.id }), column.render('Header')))))))),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "tbody" },
                ((paginated ? page : rows) || []).map((row) => {
                    prepareRow(row);
                    return (react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", Object.assign({}, row.getRowProps(), { key: row.id, className: (0,clsx__WEBPACK_IMPORTED_MODULE_2__.default)('tr', 'list-row', {
                            clickable: !!to,
                        }), onClick: () => route(to ? to(row.original) : null) }), row.cells.map((cell) => {
                        return (react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", Object.assign({}, cell.getCellProps(cellProps), { className: "td", key: cell.column.id }), cell.render('Cell')));
                    })));
                }),
                react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "tr" }, !loading && data.length === 0 && (react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "padding-bottom padding-top" }, "No data available"))))),
        paginated && showPaginationInformation && (react__WEBPACK_IMPORTED_MODULE_3__.createElement(_pagination__WEBPACK_IMPORTED_MODULE_4__.Pagination, { pageSize: pageSize, pageCount: pageCount, gotoPage: gotoPage, canPreviousPage: canPreviousPage, previousPage: previousPage, nextPage: nextPage, canNextPage: canNextPage, pageIndex: pageIndex, pageOptions: pageOptions, setPageSize: setPageSize, loading: loading }))));
};
const PaginatedList = ({ url, columns, to, q }) => {
    const [data, setData] = react__WEBPACK_IMPORTED_MODULE_3__.useState([]);
    const [loading, setLoading] = react__WEBPACK_IMPORTED_MODULE_3__.useState(false);
    const [pageCount, setPageCount] = react__WEBPACK_IMPORTED_MODULE_3__.useState(0);
    const [dataSize, setDataSize] = react__WEBPACK_IMPORTED_MODULE_3__.useState(0);
    const fetchIdRef = react__WEBPACK_IMPORTED_MODULE_3__.useRef(0);
    const fetchData = react__WEBPACK_IMPORTED_MODULE_3__.useCallback(async ({ pageSize, pageIndex }) => {
        const fetchId = ++fetchIdRef.current;
        setLoading(true);
        const params = JSON.stringify(Object.assign(Object.assign({}, q), { skip: pageIndex * pageSize, limit: pageSize }));
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
        const resp = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(`${url}?${params}`, {}, settings);
        const data = await resp.json();
        if (data && fetchId === fetchIdRef.current) {
            setData(data.result);
            setDataSize(data.pagination.all_records_count);
            setPageCount(Math.ceil(data.pagination.all_records_count / pageSize));
            setLoading(false);
        }
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_3__.createElement(List, { columns: columns, data: data, to: to, paginated: true, fetchData: fetchData, loading: loading, pageCount: pageCount, dataSize: dataSize }));
};
//# sourceMappingURL=list.js.map

/***/ }),

/***/ "../../packages/table/lib/pagination.js":
/*!**********************************************!*\
  !*** ../../packages/table/lib/pagination.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Pagination": () => (/* binding */ Pagination)
/* harmony export */ });
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @quetz-frontend/apputils */ "webpack/sharing/consume/default/@quetz-frontend/apputils/@quetz-frontend/apputils");
/* harmony import */ var _quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @fortawesome/react-fontawesome */ "webpack/sharing/consume/default/@fortawesome/react-fontawesome/@fortawesome/react-fontawesome");
/* harmony import */ var _fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @fortawesome/free-solid-svg-icons */ "webpack/sharing/consume/default/@fortawesome/free-solid-svg-icons/@fortawesome/free-solid-svg-icons");
/* harmony import */ var _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_3__);




const Pagination = ({ pageSize, pageCount, gotoPage, canPreviousPage, previousPage, nextPage, canNextPage, pageIndex, pageOptions, setPageSize, loading, }) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "jp-table-controls" },
    react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "jp-table-controls-left" },
        react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "btn-group" },
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("button", { className: "btn btn-default", onClick: () => gotoPage(0), disabled: !canPreviousPage },
                react__WEBPACK_IMPORTED_MODULE_3__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_1__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_2__.faAngleDoubleLeft })),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("button", { className: "btn btn-default", onClick: () => previousPage(), disabled: !canPreviousPage },
                react__WEBPACK_IMPORTED_MODULE_3__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_1__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_2__.faAngleLeft })),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("button", { className: "btn btn-default", onClick: () => nextPage(), disabled: !canNextPage },
                react__WEBPACK_IMPORTED_MODULE_3__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_1__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_2__.faAngleRight })),
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("button", { className: "btn btn-default", onClick: () => gotoPage(pageCount - 1), disabled: !canNextPage },
                react__WEBPACK_IMPORTED_MODULE_3__.createElement(_fortawesome_react_fontawesome__WEBPACK_IMPORTED_MODULE_1__.FontAwesomeIcon, { icon: _fortawesome_free_solid_svg_icons__WEBPACK_IMPORTED_MODULE_2__.faAngleDoubleRight }))),
        react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "jp-table-controls-text" }, loading ? (react__WEBPACK_IMPORTED_MODULE_3__.createElement(_quetz_frontend_apputils__WEBPACK_IMPORTED_MODULE_0__.InlineLoader, null)) : (react__WEBPACK_IMPORTED_MODULE_3__.createElement("p", { className: "paragraph padding-text" },
            "Page",
            ' ',
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("strong", null,
                pageIndex + 1,
                " of ",
                pageOptions.length))))),
    react__WEBPACK_IMPORTED_MODULE_3__.createElement("div", { className: "jp-table-controls-right jp-table-controls-text" },
        react__WEBPACK_IMPORTED_MODULE_3__.createElement("p", { className: "paragraph padding-side" },
            "Go to page: \u2003",
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("input", { className: "input", type: "number", value: pageIndex + 1, onChange: (e) => {
                    const page = e.target.value ? Number(e.target.value) - 1 : 0;
                    gotoPage(page);
                }, style: { width: '100px' } })),
        react__WEBPACK_IMPORTED_MODULE_3__.createElement("p", { className: "paragraph padding-side" },
            react__WEBPACK_IMPORTED_MODULE_3__.createElement("select", { className: "btn btn-default", value: pageSize, onChange: (e) => {
                    setPageSize(Number(e.target.value));
                } }, [25, 50, 100].map((pageSize) => (react__WEBPACK_IMPORTED_MODULE_3__.createElement("option", { key: pageSize, value: pageSize, defaultValue: "25" },
                "Show ",
                pageSize))))))));
//# sourceMappingURL=pagination.js.map

/***/ }),

/***/ "../../packages/table/lib/table.js":
/*!*****************************************!*\
  !*** ../../packages/table/lib/table.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Table": () => (/* binding */ Table),
/* harmony export */   "PaginatedTable": () => (/* binding */ PaginatedTable)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_table__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-table */ "webpack/sharing/consume/default/react-table/react-table");
/* harmony import */ var react_table__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_table__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var clsx__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! clsx */ "../../node_modules/clsx/dist/clsx.m.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! prop-types */ "webpack/sharing/consume/default/prop-types/prop-types");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _pagination__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./pagination */ "../../packages/table/lib/pagination.js");






const recordPaginationHistory = ({ pageSize, pageIndex, query }) => {
    const search_params = new URLSearchParams(window.location.search);
    const prev_index = search_params.get('index');
    const prev_size = search_params.get('size');
    const prev_query = search_params.get('query') || '';
    if (!prev_index && pageIndex === 0 && !query) {
        return;
    }
    if (prev_index != pageIndex || prev_size != pageSize || prev_query != query) {
        search_params.delete('size');
        search_params.append('size', pageSize);
        search_params.delete('index');
        search_params.append('index', pageIndex);
        if (query) {
            search_params.delete('query');
            search_params.append('query', query);
        }
        window.history.pushState(null, '', '?' + search_params.toString());
    }
};
const Table = ({ columns: userColumns, data, dataSize, fetchData, renderRowSubComponent, loading, paginated, pageIndex: controlledPageIndex, pageSize: controlledPageSize, pageCount: controlledPageCount, enableSearch, query: controlledQuery, }) => {
    const searching = react__WEBPACK_IMPORTED_MODULE_4__.useRef(false);
    const { getTableProps, getTableBodyProps, headerGroups, prepareRow, 
    // Non-paginated table
    rows, 
    // Paginated table
    page, canPreviousPage, canNextPage, pageOptions, pageCount, gotoPage, nextPage, previousPage, setPageSize, setGlobalFilter, state: { pageIndex, pageSize, globalFilter }, } = (0,react_table__WEBPACK_IMPORTED_MODULE_1__.useTable)({
        columns: userColumns,
        data,
        initialState: {
            pageIndex: controlledPageIndex,
            pageSize: controlledPageSize,
            globalFilter: controlledQuery,
        },
        manualPagination: paginated,
        autoResetPage: true,
        pageCount: controlledPageCount,
        manualGlobalFilter: enableSearch,
        autoResetGlobalFilter: true,
    }, ...(enableSearch ? [react_table__WEBPACK_IMPORTED_MODULE_1__.useGlobalFilter] : []), react_table__WEBPACK_IMPORTED_MODULE_1__.useExpanded, ...(paginated ? [react_table__WEBPACK_IMPORTED_MODULE_1__.usePagination] : []));
    // Debounce our onFetchData call for 100ms
    const fetchDataDebounced = (0,react_table__WEBPACK_IMPORTED_MODULE_1__.useAsyncDebounce)(fetchData, 100);
    // When these table states change, fetch new data!
    react__WEBPACK_IMPORTED_MODULE_4__.useEffect(() => {
        if (searching.current) {
            gotoPage(0);
        }
        searching.current = false;
        fetchDataDebounced({
            pageIndex: pageIndex,
            pageSize: pageSize,
            query: globalFilter,
        });
    }, [fetchDataDebounced, pageIndex, pageSize, globalFilter]);
    // Only show the "Showing 1 to x of y results and arrows if there's more than one page"
    const showPaginationInformation = dataSize > pageSize;
    return (react__WEBPACK_IMPORTED_MODULE_4__.createElement(react__WEBPACK_IMPORTED_MODULE_4__.Fragment, null,
        enableSearch && (react__WEBPACK_IMPORTED_MODULE_4__.createElement("input", { className: "input search-input table-search-input", placeholder: "Search", type: "text", value: globalFilter || '', onChange: (e) => {
                searching.current = true;
                setGlobalFilter(e.target.value);
            } })),
        react__WEBPACK_IMPORTED_MODULE_4__.createElement("table", Object.assign({}, getTableProps(), { className: "jp-table" }),
            react__WEBPACK_IMPORTED_MODULE_4__.createElement("thead", null, headerGroups.map((headerGroup, key) => (react__WEBPACK_IMPORTED_MODULE_4__.createElement("tr", Object.assign({}, headerGroup.getHeaderGroupProps(), { key: key }), headerGroup.headers.map((column) => (react__WEBPACK_IMPORTED_MODULE_4__.createElement("th", Object.assign({}, column.getHeaderProps(), { key: column.id }), column.render('Header')))))))),
            react__WEBPACK_IMPORTED_MODULE_4__.createElement("tbody", Object.assign({}, getTableBodyProps()),
                ((paginated ? page : rows) || []).map((row) => {
                    prepareRow(row);
                    return (react__WEBPACK_IMPORTED_MODULE_4__.createElement(react__WEBPACK_IMPORTED_MODULE_4__.Fragment, { key: row.id },
                        react__WEBPACK_IMPORTED_MODULE_4__.createElement("tr", Object.assign({ key: row.id }, row.getRowProps(), { className: (0,clsx__WEBPACK_IMPORTED_MODULE_2__.default)({ expanded: row.isExpanded }) }), row.cells.map((cell) => (react__WEBPACK_IMPORTED_MODULE_4__.createElement("td", Object.assign({}, cell.getCellProps(), { key: cell.column.id }), cell.render('Cell'))))),
                        row.isExpanded ? (react__WEBPACK_IMPORTED_MODULE_4__.createElement("tr", null,
                            react__WEBPACK_IMPORTED_MODULE_4__.createElement("td", { colSpan: 5, className: "jp-table-expanded-contents" }, renderRowSubComponent({ row })))) : null));
                }),
                react__WEBPACK_IMPORTED_MODULE_4__.createElement("tr", null, !loading && data.length === 0 && (react__WEBPACK_IMPORTED_MODULE_4__.createElement("td", { colSpan: 10000 }, "No data available"))))),
        paginated && showPaginationInformation && (react__WEBPACK_IMPORTED_MODULE_4__.createElement(_pagination__WEBPACK_IMPORTED_MODULE_5__.Pagination, { pageSize: pageSize, pageCount: pageCount, gotoPage: gotoPage, canPreviousPage: canPreviousPage, previousPage: previousPage, nextPage: nextPage, canNextPage: canNextPage, pageIndex: pageIndex, pageOptions: pageOptions, setPageSize: setPageSize, loading: loading }))));
};
const PaginatedTable = ({ url, columns, renderRowSubComponent, enableSearch, }) => {
    // get initial state from URL params
    const search_params = new URLSearchParams(window.location.search);
    const initialPageIndex = parseInt(search_params.get('index') || '0');
    const initialPageSize = parseInt(search_params.get('size') || '25');
    const initialQuery = search_params.get('query') || '';
    const [state, setState] = react__WEBPACK_IMPORTED_MODULE_4__.useState({
        data: [],
        dataSize: 0,
        loading: false,
        pageIndex: initialPageIndex,
        pageSize: initialPageSize,
        pageCount: 0,
        query: initialQuery,
    });
    const fetchIdRef = react__WEBPACK_IMPORTED_MODULE_4__.useRef(0);
    const fetchData = react__WEBPACK_IMPORTED_MODULE_4__.useCallback(async ({ pageSize, pageIndex, query }) => {
        const fetchId = ++fetchIdRef.current;
        setState(Object.assign(Object.assign({}, state), { loading: true }));
        const params = {
            skip: pageIndex * pageSize,
            limit: pageSize,
            q: query,
        };
        let queryString = '';
        for (const key of Object.keys(params)) {
            if (params[key]) {
                if (queryString.length) {
                    queryString += '&';
                }
                queryString += key + '=' + encodeURIComponent(params[key]);
            }
        }
        const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
        const resp = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeRequest(`${url}?${queryString}`, {}, settings);
        const data = await resp.json();
        if (data && fetchId === fetchIdRef.current) {
            recordPaginationHistory({ pageIndex, pageSize, query });
            setState({
                data: data.result,
                dataSize: data.pagination.all_records_count,
                loading: false,
                pageIndex: pageIndex,
                pageSize: pageSize,
                pageCount: Math.ceil(data.pagination.all_records_count / pageSize),
                query: query,
            });
        }
    }, []);
    return (react__WEBPACK_IMPORTED_MODULE_4__.createElement(Table, { columns: columns, data: state.data, dataSize: state.dataSize, fetchData: fetchData, renderRowSubComponent: renderRowSubComponent, loading: state.loading, paginated: true, pageIndex: state.pageIndex, pageSize: state.pageSize, pageCount: state.pageCount, enableSearch: enableSearch, query: state.query }));
};
Table.propTypes = {
    columns: (prop_types__WEBPACK_IMPORTED_MODULE_3___default().any),
    data: (prop_types__WEBPACK_IMPORTED_MODULE_3___default().any),
    renderRowSubComponent: (prop_types__WEBPACK_IMPORTED_MODULE_3___default().any),
    enableSearch: (prop_types__WEBPACK_IMPORTED_MODULE_3___default().any),
};
//# sourceMappingURL=table.js.map

/***/ })

}]);
//# sourceMappingURL=packages_table_lib_index_js.bundle.js.map