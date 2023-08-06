import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

export namespace CommandIDs {
  export const plugin = '@quetz-frontend/application-extension:sessions';
}

/**
 * A plugin to stop the kernels, sessions and terminals polling
 */
export const sessions: JupyterFrontEndPlugin<void> = {
  id: CommandIDs.plugin,
  autoStart: true,
  activate: (app: JupyterFrontEnd): void => {
    app.serviceManager.sessions?.ready.then((value) => {
      // stop polling the kernel sessions
      app.serviceManager.sessions['_kernelManager']['_pollModels']?.stop();
      // stop polling the sessions
      void app.serviceManager.sessions['_pollModels'].stop();
    });

    app.serviceManager.kernelspecs?.ready.then((value) => {
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
