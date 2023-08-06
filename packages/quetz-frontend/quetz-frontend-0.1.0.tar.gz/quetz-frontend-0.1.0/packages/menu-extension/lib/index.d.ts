import { JupyterFrontEndPlugin, IRouter } from '@jupyterlab/application';
import { ReactWidget } from '@jupyterlab/apputils';
import { Message } from '@lumino/messaging';
import { ILogInMenu, LogInItem } from '@quetz-frontend/menu';
import * as React from 'react';
export declare namespace CommandIDs {
    const title = "@quetz-frontend/menu-extension:topBar/title";
    const menu = "@quetz-frontend/menu-extension:topBar/menu";
    const login = "@quetz-frontend/menu-extension:topBar/login";
}
declare const plugins: JupyterFrontEndPlugin<any>[];
export default plugins;
/**
 * A concrete implementation of a help menu.
 */
export declare class LogInMenu extends ReactWidget implements ILogInMenu {
    constructor(router: IRouter);
    protected onAfterAttach(msg: Message): void;
    protected onBeforeDetach(msg: Message): void;
    addItem(item: LogInItem): void;
    private _onClickOutSide;
    private _onClick;
    private _logIn;
    private _route;
    render(): React.ReactElement;
    private _isActive;
    private _profile;
    private _router;
    private _items;
}
