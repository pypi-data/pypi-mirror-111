import { API_STATUSES } from '@quetz-frontend/apputils';
import * as React from 'react';
interface IOwner {
    id: string;
    username: string;
    profile: {
        name: string;
        avatar_url: string;
    };
}
interface IJob {
    id: number;
    items_spec: string;
    owner: IOwner;
    created: Date;
    status: string;
    manifest: string;
}
declare type JobState = {
    id: number;
    job: IJob;
    apiStatus: API_STATUSES;
};
/**
 *
 */
declare class Job extends React.Component<any, JobState> {
    constructor(props: any);
    componentDidMount(): Promise<void>;
    render(): JSX.Element;
}
export default Job;
