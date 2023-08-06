import { IRouter, } from '@jupyterlab/application';
import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { FetchHoc, Breadcrumbs } from '@quetz-frontend/apputils';
import { ILogInMenu } from '@quetz-frontend/menu';
import { last, capitalize } from 'lodash';
import { BrowserRouter as Router, Route, Switch, Redirect, NavLink, } from 'react-router-dom';
import ReactNotification from 'react-notifications-component';
import * as React from 'react';
import UserAPIKey from './api-key';
import UserProfile from './tab-profile';
import UserPackages from './tab-packages';
import UserChannels from './tab-channels';
/**
 * The command ids used by the main plugin.
 */
export var CommandIDs;
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
    requires: [IRouter, ILogInMenu],
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
export default plugin;
const getBreadcrumbText = () => {
    const currentSection = last(window.location.pathname.split('/'));
    if (currentSection === 'api-keys') {
        return 'API keys';
    }
    return capitalize(currentSection);
};
class UserRouter extends ReactWidget {
    constructor() {
        super();
        this.id = DOMUtils.createDomID();
        this.title.label = 'User main page';
    }
    render() {
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/me');
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
        return (React.createElement(Router, { basename: "/user" },
            React.createElement(ReactNotification, null),
            React.createElement("div", { className: "page-contents-width-limit" },
                React.createElement(Breadcrumbs, { items: breadcrumbItems }),
                React.createElement("h2", { className: "heading2" }, "User details"),
                React.createElement("div", { className: "left-right" },
                    React.createElement("div", { className: "leftbar" },
                        React.createElement(NavLink, { className: "leftbar-item", to: "/profile" }, "Profile"),
                        React.createElement(NavLink, { className: "leftbar-item", to: "/api-keys" }, "API key"),
                        React.createElement(NavLink, { className: "leftbar-item", to: "/channels" }, "Channels"),
                        React.createElement(NavLink, { className: "leftbar-item", to: "/packages" }, "Packages")),
                    React.createElement("div", { className: "right-section" },
                        React.createElement(FetchHoc, { url: url, loadingMessage: "Fetching user information", genericErrorMessage: "Error fetching user information" }, (userData) => (React.createElement(Switch, null,
                            React.createElement(Route, { path: "/profile" },
                                React.createElement(UserProfile, { userData: userData })),
                            React.createElement(Route, { path: "/api-keys" },
                                React.createElement(UserAPIKey, null)),
                            React.createElement(Route, { path: "/channels" },
                                React.createElement(UserChannels, { username: userData.user.username })),
                            React.createElement(Route, { path: "/packages" },
                                React.createElement(UserPackages, { username: userData.user.username })),
                            React.createElement(Route, { path: "/", exact: true },
                                React.createElement(Redirect, { to: "/profile" }))))))))));
    }
}
//# sourceMappingURL=index.js.map