import { IRouter, } from '@jupyterlab/application';
//import { DOMUtils, ReactWidget } from '@jupyterlab/apputils';
import { ILogInMenu } from '@quetz-frontend/menu';
//import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
//import * as React from 'react';
import { Jobs } from './jobs';
//import Job from './job';
/**
 * The command ids used by the main plugin.
 */
export var CommandIDs;
(function (CommandIDs) {
    CommandIDs.jobs = '@quetz-frontend:jobs';
})(CommandIDs || (CommandIDs = {}));
/**
 * The main menu plugin.
 */
const plugin = {
    id: CommandIDs.jobs,
    autoStart: true,
    requires: [IRouter, ILogInMenu],
    activate: (app, router, menu) => {
        const { shell, commands } = app;
        commands.addCommand(CommandIDs.jobs, {
            execute: () => {
                shell.add(new Jobs(), 'main');
            },
        });
        router.register({
            pattern: /jobs.*/,
            command: CommandIDs.jobs,
        });
        menu.addItem({
            id: CommandIDs.jobs,
            label: 'Jobs',
            icon: 'empty',
            api: '/jobs',
            loggedIn: true,
        });
    },
};
export default plugin;
/*class JobsRouter extends ReactWidget {
  
  constructor() {
    super();
    this.id = DOMUtils.createDomID();;
    this.title.label = 'Jobs main page';
  }

  render(): React.ReactElement {
    return (
      <Router basename="/jobs">
        <Switch>
          <Route path="/:jobId" render={(props) => <Job {...props} />} />
          <Route path="" component={Jobs} />
          <Route path="*" component={Jobs} />
        </Switch>
      </Router>
    );
  }
} */
//# sourceMappingURL=index.js.map