import { JupyterFrontEndPlugin } from '@jupyterlab/application';
/**
 * The command ids used by the main plugin.
 */
export declare namespace CommandIDs {
    const plugin = "@quetz-frontend/search-extension:search";
    const open = "@quetz-frontend/search-extension:search/open";
}
/**
 * The main menu plugin.
 */
declare const plugin: JupyterFrontEndPlugin<void>;
export default plugin;
