import { JupyterFrontEnd, Router, IRouter, } from '@jupyterlab/application';
export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.plugin = '@quetz-frontend/application-extension:router';
})(CommandIDs || (CommandIDs = {}));
export const router = {
    id: CommandIDs.plugin,
    autoStart: true,
    requires: [JupyterFrontEnd.IPaths],
    provides: IRouter,
    activate: (app, paths) => {
        const { commands } = app;
        const router = new Router({ base: '/', commands });
        void app.started.then(() => {
            if (router.current.path === router.base) {
                router.navigate('/home', { skipRouting: true });
            }
            void router.route();
            // Route all pop state events.
            window.addEventListener('popstate', () => {
                void router.route();
            });
            router.routed.connect((router, loc) => {
                if (loc.path === router.base) {
                    router.navigate('/home');
                }
            });
            //@ts-ignore
            window.router = router;
        });
        return router;
    },
};
//# sourceMappingURL=router.js.map