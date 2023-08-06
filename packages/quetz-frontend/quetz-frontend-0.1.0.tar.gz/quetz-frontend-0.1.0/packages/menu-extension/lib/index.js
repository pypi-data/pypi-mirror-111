import { IRouter, } from '@jupyterlab/application';
import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { LabIcon } from '@jupyterlab/ui-components';
import { Widget } from '@lumino/widgets';
import { MainMenu, IMainMenu, ILogInMenu, } from '@quetz-frontend/menu';
import { SearchBox } from '@quetz-frontend/apputils';
import * as React from 'react';
import * as quetz_logo from '../style/img/quetz-logo.svg';
import * as avatar_icon from '../style/img/avatar-icon.svg';
export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.title = '@quetz-frontend/menu-extension:topBar/title';
    CommandIDs.menu = '@quetz-frontend/menu-extension:topBar/menu';
    CommandIDs.login = '@quetz-frontend/menu-extension:topBar/login';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main title plugin.
 */
const title = {
    id: CommandIDs.title,
    autoStart: true,
    requires: [IRouter],
    activate: quetzTitle,
};
/**
 * The main menu plugin.
 */
const menu = {
    id: CommandIDs.menu,
    autoStart: true,
    provides: IMainMenu,
    activate: toolbar,
};
/**
 * The Login menu plugin.
 */
const login = {
    id: CommandIDs.login,
    autoStart: true,
    requires: [IRouter],
    provides: ILogInMenu,
    activate: logInMenu,
};
const plugins = [title, menu, login];
export default plugins;
/**
 * A concrete implementation of a help menu.
 */
export class LogInMenu extends ReactWidget {
    constructor(router) {
        super();
        this._onClickOutSide = (e) => {
            if (!this.node.contains(e.target) && this._isActive) {
                this._isActive = false;
                this.update();
            }
        };
        this._onClick = () => {
            this._isActive = !this._isActive;
            this.update();
        };
        this._logIn = (api) => {
            window.location.href = api;
            this._isActive = !this._isActive;
            this.update();
        };
        this._route = (route) => {
            this._router.navigate(route);
            this._isActive = !this._isActive;
            this.update();
        };
        this._isActive = false;
        this._items = new Array();
        // TODO logout, show google login
        this.id = 'login-menu';
        this.addClass('topbar-item');
        this._router = router;
    }
    onAfterAttach(msg) {
        super.onAfterAttach(msg);
        window.addEventListener('click', this._onClickOutSide);
        const config_data = document.getElementById('jupyter-config-data');
        if (config_data) {
            try {
                const data = JSON.parse(config_data.innerHTML);
                if (data.detail) {
                    return console.error(data.detail);
                }
                if (data.logged_in_user_profile) {
                    this._profile = JSON.parse(data.logged_in_user_profile);
                }
                else {
                    fetch('/api/me')
                        .then((resp) => {
                        return resp.json();
                    })
                        .then(async (data) => {
                        if (data.detail) {
                            return console.error(data.detail);
                        }
                        this._profile = data;
                        this.update();
                    });
                }
                this.update();
            }
            catch (e) {
                console.log("Couldn't parse JSON from template.");
            }
        }
        this.update();
    }
    onBeforeDetach(msg) {
        super.onBeforeDetach(msg);
        window.removeEventListener('click', this._onClickOutSide);
    }
    addItem(item) {
        this._items.push(item);
        this.update();
    }
    render() {
        if (this._profile) {
            return (React.createElement("div", null,
                React.createElement("a", { onClick: this._onClick },
                    React.createElement("img", { className: "user-img", src: this._profile.avatar_url, alt: "avatar" })),
                React.createElement("div", { className: `login-menu ${this._isActive ? 'active' : 'inactive'}` },
                    React.createElement("ul", null,
                        React.createElement("li", { key: this._profile.name },
                            React.createElement("a", null,
                                React.createElement("span", null,
                                    "Signed in as ",
                                    this._profile.user.username))),
                        React.createElement("hr", null),
                        this._items.map((value) => {
                            if (value.loggedIn) {
                                return (React.createElement("li", { key: value.id },
                                    React.createElement("a", { onClick: () => this._route(value.api) },
                                        React.createElement("span", null, value.label))));
                            }
                        }),
                        React.createElement("hr", null),
                        React.createElement("li", { key: "signout" },
                            React.createElement("a", { onClick: () => this._logIn('/auth/logout') },
                                React.createElement("span", null, "Sign out")))))));
        }
        else {
            const avatar = new LabIcon({
                name: 'avatar_icon',
                svgstr: avatar_icon.default,
            });
            return (React.createElement("div", null,
                React.createElement("a", { onClick: this._onClick },
                    React.createElement(avatar.react, { className: "user-img", tag: "span", width: "28px", height: "28px" })),
                React.createElement("div", { className: `login-menu ${this._isActive ? 'active' : 'inactive'}` },
                    React.createElement("ul", null, this._items.map((value) => {
                        if (!value.loggedIn) {
                            return (React.createElement("li", { key: value.id },
                                React.createElement("a", { onClick: () => this._logIn(value.api) },
                                    React.createElement("span", null, value.label))));
                        }
                    })))));
        }
    }
}
class SearchWidget extends ReactWidget {
    constructor(router) {
        super();
        this.onSearch = (searchText) => {
            this._router.navigate(`/search?q=${searchText}`);
        };
        this.id = DOMUtils.createDomID();
        this.addClass('topbar-spacer');
        this._router = router;
    }
    render() {
        return (React.createElement("div", { className: "topbar-search-wrapper" },
            React.createElement(SearchBox, { onSubmit: this.onSearch })));
    }
}
/**
 * @param app
 * @param router
 */
function quetzTitle(app, router) {
    const link = document.createElement('a');
    const logo = new Widget({ node: link });
    const logo_icon = new LabIcon({
        name: 'quetz_logo',
        svgstr: quetz_logo.default,
    });
    logo_icon.element({
        container: logo.node,
        elementPosition: 'center',
        margin: '2px 2px 2px 8px',
        height: 'auto',
        width: '80px',
    });
    logo.id = 'jupyter-logo';
    logo.addClass('topbar-item');
    logo.title.label = 'Downloads';
    logo.title.caption = 'Open Downloads page';
    logo.node.onclick = () => {
        router.navigate('/home');
    };
    app.shell.add(logo, 'top', { rank: 0 });
    app.shell.add(new SearchWidget(router), 'top', { rank: 10000 });
}
/**
 * @param app
 */
function toolbar(app) {
    const menu = new MainMenu();
    app.shell.add(menu, 'top', { rank: 10001 });
    return menu;
}
/**
 * @param app
 * @param router
 */
function logInMenu(app, router) {
    const login = new LogInMenu(router);
    app.shell.add(login, 'top', { rank: 19999 });
    return login;
}
//# sourceMappingURL=index.js.map