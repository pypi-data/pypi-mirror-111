import { IRouter, } from '@jupyterlab/application';
import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc, formatPlural } from '@quetz-frontend/apputils';
import { List } from '@quetz-frontend/table';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faGlobeAmericas, faUnlockAlt, } from '@fortawesome/free-solid-svg-icons';
import ReactTooltip from 'react-tooltip';
import * as React from 'react';
export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/home-extension:home';
    CommandIDs.open = '@quetz-frontend/home-extension:home/open';
})(CommandIDs || (CommandIDs = {}));
const plugin = {
    id: CommandIDs.plugin,
    autoStart: true,
    requires: [IRouter],
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
export default plugin;
class Homepage extends ReactWidget {
    constructor(router) {
        super();
        this.id = DOMUtils.createDomID();
        this.title.label = 'Home page';
        this._router = router;
    }
    _route(route) {
        this._router.navigate(route);
    }
    render() {
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/channels');
        return (React.createElement("div", { className: "page-contents-width-limit" },
            React.createElement("h2", { className: "heading2" }, "Home"),
            React.createElement("div", { className: "flex" },
                React.createElement("h3", { className: "section-heading" }, "Recently updated channels"),
                "\u2003",
                React.createElement("p", { className: "minor-paragraph" },
                    React.createElement("a", { className: "link", onClick: () => this._route('/channels') }, "View all"))),
            React.createElement("div", { className: "padding-side" },
                React.createElement(FetchHoc, { url: url, loadingMessage: "Fetching list of channels", genericErrorMessage: "Error fetching list of channels" }, (channels) => {
                    return channels.length > 0 ? (React.createElement(List, { data: channels.slice(0, 5), columns: getChannelsListColumns(), to: (rowData) => this._route(`/channels/${rowData.name}`) })) : (React.createElement("p", { className: "paragraph" }, "No channels available"));
                }))));
    }
}
const getChannelsListColumns = () => [
    {
        Header: '',
        accessor: 'name',
        Cell: ({ row }) => (React.createElement(React.Fragment, null,
            React.createElement("span", { "data-for": `tooltip-${row.original.name}`, "data-tip": row.original.private ? 'Private' : 'Public' },
                React.createElement(FontAwesomeIcon, { icon: row.original.private ? faUnlockAlt : faGlobeAmericas })),
            React.createElement(ReactTooltip, { id: `tooltip-${row.original.name}`, place: "right", type: "dark", effect: "solid" }))),
        width: 5,
    },
    {
        Header: '',
        accessor: 'user.profile.name',
        Cell: ({ row }) => (React.createElement("div", null,
            React.createElement("p", { className: "text" }, row.original.name),
            React.createElement("p", { className: "minor-paragraph channel-list-description" }, row.original.description))),
        width: 45,
    },
    {
        Header: '',
        accessor: 'user.username',
        Cell: ({ row }) => formatPlural(row.original.packages_count, 'package'),
        width: 35,
    },
    {
        Header: '',
        accessor: 'role',
        Cell: ({ row }) => formatPlural(row.original.packages_count, 'member'),
        width: 20,
    },
];
//# sourceMappingURL=index.js.map