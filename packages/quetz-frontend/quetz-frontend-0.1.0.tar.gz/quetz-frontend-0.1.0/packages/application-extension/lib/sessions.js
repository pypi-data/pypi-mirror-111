export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/application-extension:sessions';
})(CommandIDs || (CommandIDs = {}));
/**
 * A plugin to stop the kernels, sessions and terminals polling
 */
export const sessions = {
    id: CommandIDs.plugin,
    autoStart: true,
    activate: (app) => {
        var _a, _b;
        (_a = app.serviceManager.sessions) === null || _a === void 0 ? void 0 : _a.ready.then((value) => {
            var _a;
            // stop polling the kernel sessions
            (_a = app.serviceManager.sessions['_kernelManager']['_pollModels']) === null || _a === void 0 ? void 0 : _a.stop();
            // stop polling the sessions
            void app.serviceManager.sessions['_pollModels'].stop();
        });
        (_b = app.serviceManager.kernelspecs) === null || _b === void 0 ? void 0 : _b.ready.then((value) => {
            // stop polling the kernelspecs
            void app.serviceManager.kernelspecs.dispose();
        });
        /*
        app.serviceManager.terminals?.ready.then( value => {
          console.debug("Stopping terminals:");
          // stop polling the terminals
          void app.serviceManager.terminals['_pollModels'].stop();
        });
        */
    },
};
//# sourceMappingURL=sessions.js.map