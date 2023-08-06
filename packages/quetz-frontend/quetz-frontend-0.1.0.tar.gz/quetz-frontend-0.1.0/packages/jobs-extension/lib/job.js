import { ServerConnection } from '@jupyterlab/services';
import { URLExt } from '@jupyterlab/coreutils';
import { InlineLoader, Breadcrumbs, API_STATUSES, } from '@quetz-frontend/apputils';
import * as React from 'react';
import Table from './table';
/**
 *
 */
class Job extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: props.match.params.jobId,
            job: {
                id: 0,
                created: new Date(),
                manifest: '',
                owner: { id: '', profile: { name: '', avatar_url: '' }, username: '' },
                items_spec: '',
                status: '',
            },
            apiStatus: API_STATUSES.PENDING,
        };
    }
    async componentDidMount() {
        const settings = ServerConnection.makeSettings();
        const url = URLExt.join(settings.baseUrl, '/api/jobs', this.state.id.toString());
        const resp = await ServerConnection.makeRequest(url, {}, settings);
        const job = await resp.json();
        this.setState({
            job,
            apiStatus: API_STATUSES.SUCCESS,
        });
    }
    render() {
        const { apiStatus, job } = this.state;
        const breadcrumbItems = [
            {
                text: 'Home',
                link: '/',
            },
            {
                text: 'Jobs',
                link: '/jobs',
            },
            {
                text: 'Job ID',
            },
        ];
        const jobColumns = [
            {
                Header: 'Manifest',
                accessor: 'manifest',
                // Cell: ({ row }: { row: { values: IJob } }) => row.values.manifest
            },
            {
                Header: 'Created',
                accessor: 'created',
                // Cell: ({ row }: { row: { values: IJob } }) => row.values.created
            },
            {
                Header: 'Status',
                accessor: 'status',
                // Cell: ({ row }: { row: { values: IJob } }) => row.values.status
            },
            {
                Header: 'Owner',
                accessor: 'owner.username',
                // Cell: ({ row }: { row: { values: IJob } }) => row.values.owner.username
            },
        ];
        return (React.createElement("div", { className: "page-contents-width-limit" },
            React.createElement(Breadcrumbs, { items: breadcrumbItems }),
            React.createElement("h2", { className: "heading2" }, "Jobs"),
            apiStatus === API_STATUSES.PENDING && (React.createElement(InlineLoader, { text: "Fetching tasks" })),
            React.createElement(Table, { columns: jobColumns, data: job })));
    }
}
export default Job;
//# sourceMappingURL=job.js.map