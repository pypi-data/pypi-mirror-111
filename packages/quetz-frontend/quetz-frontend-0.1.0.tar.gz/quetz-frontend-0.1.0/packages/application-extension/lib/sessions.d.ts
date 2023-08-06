import { JupyterFrontEndPlugin } from '@jupyterlab/application';
export declare namespace CommandIDs {
    const plugin = "@quetz-frontend/application-extension:sessions";
}
/**
 * A plugin to stop the kernels, sessions and terminals polling
 */
export declare const sessions: JupyterFrontEndPlugin<void>;
