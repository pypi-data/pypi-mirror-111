import { JupyterFrontEndPlugin } from '@jupyterlab/application';
/**
 * The command ids used by the main plugin.
 */
export declare namespace CommandIDs {
    const jobs = "@quetz-frontend:jobs";
}
/**
 * The main menu plugin.
 */
declare const plugin: JupyterFrontEndPlugin<void>;
export default plugin;
