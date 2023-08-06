import { Token } from '@lumino/coreutils';
import { Widget } from '@lumino/widgets';
export declare type LogInItem = {
    id: string;
    label: string;
    icon: string;
    api: string;
    loggedIn: boolean;
};
/**
 * The main menu token.
 */
export declare const IMainMenu: Token<IMainMenu>;
/**
 * The main menu interface.
 */
export interface IMainMenu {
    /**
     * Add a new menu to the main menu bar.
     */
    addItem(menu: Widget, rank: number): void;
}
/**
 * The main menu token.
 */
export declare const ILogInMenu: Token<ILogInMenu>;
/**
 * The login menu interface.
 */
export interface ILogInMenu {
    /**
     * Add a new menu to the main menu bar.
     */
    addItem(item: LogInItem): void;
}
