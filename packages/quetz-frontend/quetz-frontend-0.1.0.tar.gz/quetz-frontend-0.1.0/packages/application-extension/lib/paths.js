import { JupyterFrontEnd, } from '@jupyterlab/application';
export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/application-extension:paths';
})(CommandIDs || (CommandIDs = {}));
/**
 * The default paths.
 */
export const paths = {
    id: CommandIDs.plugin,
    autoStart: true,
    provides: JupyterFrontEnd.IPaths,
    activate: (app) => {
        return app.paths;
    },
};
//# sourceMappingURL=paths.js.map