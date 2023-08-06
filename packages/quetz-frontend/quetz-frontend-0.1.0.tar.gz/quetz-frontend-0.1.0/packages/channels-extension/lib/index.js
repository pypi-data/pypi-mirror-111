import { IRouter, } from '@jupyterlab/application';
import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { fileIcon } from '@jupyterlab/ui-components';
import { ILogInMenu } from '@quetz-frontend/menu';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import * as React from 'react';
import ChannelsList from './channels/list';
import ChannelDetails from './channels/details';
import PackageDetails from './package';
/**
 * The command ids used by the main plugin.
 */
export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/channels-extension:channels';
    CommandIDs.open = '@quetz-frontend:channels/open';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main plugin.
 */
const plugin = {
    id: CommandIDs.plugin,
    autoStart: true,
    requires: [IRouter, ILogInMenu],
    activate: (app, router, menu) => {
        const { commands, shell } = app;
        commands.addCommand(CommandIDs.open, {
            execute: () => {
                shell.add(new RouterWidget(), 'main');
            },
        });
        router.register({
            pattern: /channels.*/,
            command: CommandIDs.open,
        });
        menu.addItem({
            id: CommandIDs.open,
            label: 'Channels',
            icon: 'empty',
            api: '/channels',
            loggedIn: true,
        });
    },
};
export default plugin;
class RouterWidget extends ReactWidget {
    constructor() {
        super();
        this.id = DOMUtils.createDomID();
        this.title.label = 'Channels main page';
        this.title.icon = fileIcon;
        this.addClass('jp-ReactWidget');
    }
    render() {
        return (React.createElement("div", { className: "page-contents-width-limit" },
            React.createElement(Router, { basename: "/channels" },
                React.createElement(Switch, null,
                    React.createElement(Route, { path: "/:channelId/packages/:packageId" },
                        React.createElement(PackageDetails, null)),
                    React.createElement(Route, { path: "/:channelId" },
                        React.createElement(ChannelDetails, null)),
                    React.createElement(Route, { path: "", exact: true },
                        React.createElement(ChannelsList, null))))));
    }
}
//# sourceMappingURL=index.js.map