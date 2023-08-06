import * as React from 'react';
interface IChannelsApiItem {
    name: string;
    description: string;
    private: boolean;
    size_limit: null | number;
    mirror_channel_url: null | string;
    mirror_mode: null | string;
    members_count: number;
    packages_count: number;
}
declare type ChannelsAppState = {
    channels: null | IChannelsApiItem[];
    searchText: string;
};
declare class ChannelsList extends React.Component<any, ChannelsAppState> {
    constructor(props: any);
    onSearch: (searchText: string) => void;
    render(): JSX.Element;
}
export default ChannelsList;
