import { JupyterFrontEndPlugin } from '@jupyterlab/application';
/**
 * The command ids used by the main plugin.
 */
export declare namespace CommandIDs {
    const plugin = "@quetz-frontend/channels-extension:channels";
    const open = "@quetz-frontend:channels/open";
}
/**
 * The main plugin.
 */
declare const plugin: JupyterFrontEndPlugin<void>;
export default plugin;
