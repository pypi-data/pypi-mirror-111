import { IRouter, } from '@jupyterlab/application';
import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc, Breadcrumbs } from '@quetz-frontend/apputils';
import { Table } from '@quetz-frontend/table';
import * as React from 'react';
/**
 * The command ids used by the main plugin.
 */
export var CommandIDs;
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
    requires: [IRouter],
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
export default plugin;
class SearchPage extends ReactWidget {
    constructor(router) {
        super();
        this.id = DOMUtils.createDomID();
        this.title.label = 'Search page';
        this._router = router;
    }
    _route(route) {
        this._router.navigate(route);
    }
    render() {
        const searchText = new URLSearchParams(window.location.search).get('q');
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, `/api/packages/search/?q=${searchText}`);
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
                Cell: ({ row }) => (React.createElement(React.Fragment, null,
                    React.createElement("a", { className: "link", onClick: () => this._route(`/channels/${row.original.channel_name}`) }, row.original.channel_name),
                    "\u2003/\u2003",
                    React.createElement("a", { className: "link", onClick: () => this._route(`/channels/${row.original.channel_name}/packages/${row.values.name}`) }, row.values.name))),
            },
            {
                Header: 'Summary',
                accessor: 'summary',
            },
            {
                Header: 'Version',
                accessor: 'current_version',
                Cell: ({ row }) => (row.values.current_version || React.createElement("i", null, "n/a")),
            },
        ];
        return (React.createElement("div", { className: "page-contents-width-limit" },
            React.createElement("h2", { className: "heading2" }, "Packages"),
            React.createElement("div", { className: "flex" },
                React.createElement(Breadcrumbs, { items: breadcrumbItems })),
            React.createElement("div", { className: "padding-side" },
                React.createElement(FetchHoc, { url: url, loadingMessage: "Searching for packages", genericErrorMessage: "Error fetching API keys" }, (data) => {
                    return React.createElement(Table, { columns: columns, data: data || [] });
                }))));
    }
}
//# sourceMappingURL=index.js.map