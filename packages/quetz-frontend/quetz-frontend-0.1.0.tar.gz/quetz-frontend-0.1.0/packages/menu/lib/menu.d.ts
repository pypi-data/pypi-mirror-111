import { Widget, Panel } from '@lumino/widgets';
import { IMainMenu } from './tokens';
export declare type Profile = {
    name: string;
    avatar_url: string;
    user: {
        id: string;
        username: string;
    };
};
/**
 * The main menu.
 */
export declare class MainMenu extends Panel implements IMainMenu {
    /**
     * Construct the main menu bar.
     */
    constructor();
    addItem(widget: Widget, rank: number): void;
    /**
     * A message hook for child add/remove messages on the main area dock panel.
     *
     * @param handler
     * @param msg
     */
    private _panelChildHook;
    private _items;
}
