import { JupyterFrontEndPlugin } from '@jupyterlab/application';
/**
 * The command ids used by the main plugin.
 */
export declare namespace CommandIDs {
    const plugin = "@quetz-frontend/user-extension:user";
    const open = "@quetz-frontend/user-extension:open";
}
/**
 * The main menu plugin.
 */
declare const plugin: JupyterFrontEndPlugin<void>;
export default plugin;
